from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'post/index.html')


def detail(request):
    return render(request, 'post/detail.html')