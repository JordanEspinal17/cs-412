from django.shortcuts import render

# base your views here.
def base(request):
    return render(request, 'webcam/base.html')

