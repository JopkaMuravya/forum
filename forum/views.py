from django.shortcuts import render, redirect
from .forms import TopicForm


def main_str(request):
    return render(request, 'forum/index.html', {})

def create_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main_str')
    else:
        form = TopicForm()
    return render(request, 'forum/create-topic.html', {'form': form})

def signup(request):
    return render(request, 'forum/simple-signup.html', {})

def signin(request):
    return render(request, 'forum/signin.html', {})

def topic(request):
    return render(request, 'forum/single-topic.html', {})
