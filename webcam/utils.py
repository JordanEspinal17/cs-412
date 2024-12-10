from .models import Achievement
from .models import Ranking
from django.db.models import Sum

def get_top_5_users():
    """
    Retrieves the usernames of the top 5 users based on total scores in the leaderboard.
    """
    leaderboard = (
        Ranking.objects.values('username')
        .annotate(total_score=Sum('score'))
        .order_by('-total_score')[:5]
    )
    return [entry['username'] for entry in leaderboard]

def get_top_1_user():
    """
    Retrieves the username of the top user in the leaderboard.
    """
    leaderboard = (
        Ranking.objects.values('username')
        .annotate(total_score=Sum('score'))
        .order_by('-total_score')
    )
    if leaderboard.exists():
        return leaderboard.first()['username']
    return None

def check_and_award_achievements(profile):
    achievements = {
        "uploaded_1_video": profile.videos_uploaded >= 1,
        "uploaded_5_videos": profile.videos_uploaded >= 5,
        "uploaded_10_videos": profile.videos_uploaded >= 10,
        "top_5_leaderboard": profile.user.username in get_top_5_users(),
        "top_1_leaderboard": profile.user.username == get_top_1_user(),
    }

    for key, condition in achievements.items():
        if condition:
            achievement = Achievement.objects.filter(condition=key).first()
            if achievement and achievement not in profile.achievements.all():
                profile.achievements.add(achievement)
