# Standard Library Imports
import os
import random
import numpy as np
import matplotlib.pyplot as plt
from django.db.models import Sum

# Third-Party Library Imports
import cv2
import mediapipe as mp
from moviepy.editor import VideoFileClip
import openai

# Django Imports
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.views.generic import FormView

# Local Application Imports
from .forms import VideoUploadForm, UserRegisterForm
from .models import UploadedVideo, Profile, CoachFeedback, Ranking, ChatMessage
from .utils import check_and_award_achievements




class UserRegisterView(FormView):
    template_name = 'webcam/register.html'  # Update path to match new location
    form_class = UserRegisterForm
    success_url = reverse_lazy('webcam/base')  # Redirect to home after registration

    def form_valid(self, form):
        user = form.save(commit=False)
        # Save additional fields
        user.email = form.cleaned_data['email']
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()

        # Log the user in
        login(self.request, user)

        # Create the Profile object
        Profile.objects.create(
            user=user,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email
        )
        return super().form_valid(form)


def login_view(request):
    return render(request, 'webcam/login.html')

def base(request):
    return render(request, 'webcam/base.html')

def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the video upload
            video_instance = form.save(commit=False)
            video_instance.user = request.user
            video_instance.save()

            # Update profile stats
            profile = Profile.objects.get(user=request.user)
            profile.videos_uploaded += 1
            profile.save()

            # Check for achievements
            check_and_award_achievements(profile)

            # Redirect to the analyze video page
            return redirect('analyze_video', video_id=video_instance.id)
    else:
        form = VideoUploadForm()

    return render(request, 'webcam/upload_video.html', {'form': form})


def analyze_video(request, video_id):
    video_instance = UploadedVideo.objects.get(id=video_id)
    client_video_path = video_instance.client_video.path
    reference_video_path = video_instance.reference_video.path

    # Extract landmarks from both videos
    client_data = process_video(client_video_path)
    reference_data = process_video(reference_video_path)

    # Compare client video to reference video
    comparison_results = compare_videos(client_data, reference_data)

    # Generate feedback using ChatGPT API
    feedback, graph_path = generate_feedback(comparison_results)

    # Split areas_of_improvement into a list
    feedback['areas_of_improvement'] = feedback['areas_of_improvement'].split('\n')

    # Ensure the ranking is updated
    average_similarity = comparison_results['average_similarity']
    user = request.user

    ranking, created = Ranking.objects.get_or_create(
        username=user.username,
        video=video_instance,
        defaults={'score': average_similarity}
    )
    if not created:
        ranking.score = average_similarity
        ranking.save()

    rankings = video_instance.rankings.all().order_by('-score')

    return render(request, 'webcam/analysis_results.html', {
        'feedback': feedback,
        'comparison_results': comparison_results,
        'graph_path': graph_path,
        'video': video_instance,
        'rankings': rankings,
    })


def compare_videos(client_data, reference_data):
    client_keypoints = client_data['keypoints_list']
    reference_keypoints = reference_data['keypoints_list']

    # Handle mismatched frame counts by analyzing overlapping frames only
    min_frame_count = min(len(client_keypoints), len(reference_keypoints))
    frame_scores = []

    for i in range(min_frame_count):
        client_frame = client_keypoints[i]
        reference_frame = reference_keypoints[i]
        score = calculate_frame_similarity(client_frame, reference_frame)
        frame_scores.append(score)

    # Reflect skipped frames in the results
    skipped_client_frames = len(client_keypoints) - min_frame_count
    skipped_reference_frames = len(reference_keypoints) - min_frame_count

    average_score = sum(frame_scores) / len(frame_scores) if frame_scores else 0

    return {
        'frame_scores': frame_scores,
        'average_similarity': average_score,
        'skipped_client_frames': skipped_client_frames,
        'skipped_reference_frames': skipped_reference_frames,
    }


def calculate_frame_similarity(client_frame, reference_frame):
    # Calculate Euclidean distance for each landmark
    distances = [
        np.sqrt((c['x'] - r['x'])**2 + (c['y'] - r['y'])**2)
        for c, r in zip(client_frame, reference_frame)
    ]
    return 1 - np.mean(distances)  # Invert distance for similarity (1 is perfect)

def process_video(video_path):
    keypoints_list = []
    cap = cv2.VideoCapture(video_path)
    pose = mp.solutions.pose.Pose(static_image_mode=False, min_detection_confidence=0.5)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        if results.pose_landmarks:
            keypoints = [
                {'x': lm.x, 'y': lm.y, 'z': lm.z, 'visibility': lm.visibility}
                for lm in results.pose_landmarks.landmark
            ]
            keypoints_list.append(keypoints)

    cap.release()
    pose.close()

    if not keypoints_list:
        print(f"No keypoints found in video: {video_path}")
    
    return {'keypoints_list': keypoints_list}

def calculate_average_confidence(keypoints_list):
    total_confidence = 0
    total_points = 0
    for keypoints in keypoints_list:
        for kp in keypoints:
            total_confidence += kp['visibility']
            total_points += 1
    if total_points == 0:
        return 0
    return total_confidence / total_points

def generate_feedback(comparison_results):
    openai.api_key = settings.OPENAI_API_KEY

    # Construct the prompt
    prompt = f"""You are a professional dance coach. Analyze the videos given and give feedback in the following outline.
    Based on the following performance data, generate structured feedback divided into three sections: 
    (1) Introduction: Highlight the overall performance.
    (2) Areas of Improvement: List specific points for improvement with details.
    (3) Conclusion: Provide encouragement and summarize suggestions.

    Performance data:
    - Average similarity to reference video: {comparison_results['average_similarity']:.2f}
    - Skipped Client Frames: {comparison_results['skipped_client_frames']}
    - Skipped Reference Frames: {comparison_results['skipped_reference_frames']}
    - Frame-by-frame scores: {comparison_results['frame_scores']}
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.7,
    )

    feedback_text = response['choices'][0]['message']['content']

    # Clean the feedback to remove unnecessary symbols
    feedback_text = feedback_text.replace("*", "").replace("#", "").strip()

    # Split the feedback into structured sections
    sections = feedback_text.split("\n\n")  # Assuming GPT provides paragraph breaks
    introduction = sections[0] if len(sections) > 0 else "No introduction provided."
    areas_of_improvement = sections[1] if len(sections) > 1 else "No areas of improvement provided."
    conclusion = sections[2] if len(sections) > 2 else "No conclusion provided."

    # Return structured feedback
    feedback = {
        "introduction": introduction.strip(),
        "areas_of_improvement": areas_of_improvement.strip(),
        "conclusion": conclusion.strip(),
    }

    # Generate graph path for the similarity scores
    frame_numbers = list(range(1, len(comparison_results['frame_scores']) + 1))
    similarity_scores = comparison_results['frame_scores']
    plt.figure(figsize=(10, 6))
    plt.plot(frame_numbers, similarity_scores, label='Frame Similarity', color='blue')
    plt.axhline(y=comparison_results['average_similarity'], color='red', linestyle='--', label='Average Similarity')
    plt.title("Frame-by-Frame Similarity")
    plt.xlabel("Frame Number")
    plt.ylabel("Similarity Score (0 to 1)")
    plt.legend()
    plt.grid(True)
    graph_filename = 'similarity_graph.png'
    graph_path = os.path.join(settings.MEDIA_ROOT, graph_filename)
    plt.savefig(graph_path)
    plt.close()

    return feedback, f'{settings.MEDIA_URL}{graph_filename}'


def logout_success(request):
    return redirect('login') 

@login_required
def global_leaderboard(request):
    # Fetch leaderboard data
    leaderboard = (
        Ranking.objects.values('username')
        .annotate(total_score=Sum('score'))
        .order_by('-total_score')
    )

    # Fetch chat messages
    chat_messages = ChatMessage.objects.order_by('-timestamp')[:50]  # Show last 50 messages

    # Handle new message submission
    if request.method == "POST":
        message = request.POST.get('message')
        if message:
            ChatMessage.objects.create(user=request.user, message=message)

    return render(request, 'webcam/global_leaderboard.html', {
        'leaderboard': leaderboard,
        'chat_messages': chat_messages,
    })

# Predefined songs and themes
SONGS = [
    "Shape of You - Ed Sheeran",
    "Blinding Lights - The Weeknd",
    "Uptown Funk - Mark Ronson ft. Bruno Mars",
    "Bad Guy - Billie Eilish",
    "Can't Stop the Feeling - Justin Timberlake"
]

THEMES = [
    "Hip Hop",
    "Ballet",
    "Jazz",
    "Contemporary",
    "Salsa",
    "Breakdance"
]

def parse_choreography(choreography_text):
    sections = {}
    current_section = None
    lines = choreography_text.splitlines()
    for line in lines:
        if line.endswith(':'):  # Assume it's a section header
            current_section = line[:-1]
            sections[current_section] = []
        elif current_section and line.strip():  # Add steps to the current section
            sections[current_section].append(line.strip())
    return sections

def generate_dance_routine(request):
    # Randomly pick a song and theme
    song = random.choice(SONGS)
    theme = random.choice(THEMES)

    # Use OpenAI API to generate choreography
    openai.api_key = settings.OPENAI_API_KEY  # Replace with your API key
    prompt = f"Generate a {theme} dance routine for the song '{song}'. Provide detailed steps for each section of the song."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.7,
    )
    choreography_text = response['choices'][0]['message']['content']
    choreography = parse_choreography(choreography_text)

    return render(request, 'webcam/dance_routine.html', {
        'song': song,
        'theme': theme,
        'choreography': choreography,
    })

@login_required
def profile_page(request):
    # Ensure the Profile exists for the user
    profile, created = Profile.objects.get_or_create(user=request.user)

    return render(request, 'webcam/profile.html', {
        'profile': profile,
        'achievements': profile.achievements.all(),
    })

