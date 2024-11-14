from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
import cv2
import numpy as np

def process_frame(request):
    if request.method == 'POST':
        file = request.FILES.get('frame')
        if file:
            # Convert file to a numpy array for OpenCV
            np_array = np.frombuffer(file.read(), np.uint8)
            frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

            # (Optional) Apply OpenCV operations here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Just for testing: Return the shape of the processed frame
            return JsonResponse({'shape': gray.shape})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def index(request):
    return render(request, 'webcam/index.html')

