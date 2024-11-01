from django.shortcuts import render


def main_str(request):
    return render(request, 'forum/index.html', {})

def create_topic(request):
    return render(request, 'forum/create-topic.html', {})

def signup(request):
    return render(request, 'forum/simple-signup.html', {})

def signin(request):
    return render(request, 'forum/signin.html', {})

def topic(request):
    return render(request, 'forum/single-topic.html', {})
