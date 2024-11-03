from django.shortcuts import render, redirect
from .forms import TopicForm
from .models import Topic, Tag

def main_str(request):
    topics = Topic.objects.all()
    return render(request, 'forum/index.html', {'topics': topics})

def create_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST, request.FILES)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.save()

            tags_input = form.cleaned_data['tags']
            tag_names = [name.strip() for name in tags_input.split(',')]

            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                topic.tags.add(tag)

            topic.save()
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
