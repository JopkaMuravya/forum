from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm, TopicForm, CommentForm
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Topic, Tag, Comment

def user_login(request):
    logout(request)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('main_str')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'forum/signin.html', {'form': form})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect('main_str')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'forum/simple-signup.html', {'user_form': user_form})

CATEGORY_COLORS = {
    'hobby': ('bg-f9bc64', 'Хобби'),
    'video': ('bg-4436f8', 'Видео'),
    'art': ('bg-ff755a', 'Искусство'),
    'games': ('bg-83253f', 'Игры'),
    'health': ('bg-3ebafa', 'Здоровье'),
    'entertainment': ('bg-a7cdbd', 'Развлечения'),
    'qa': ('bg-777da7', 'Q&A'),
    'society': ('bg-348aa7', 'Общество'),
    'random': ('bg-5dd39e', 'Случайное'),
    'tech': ('bg-bce784', 'Технологии'),
    'science': ('bg-c49bbb', 'Наука'),
    'animals': ('bg-c6b38e', 'Животные'),
    'education': ('bg-525252', 'Образование'),
    'politics': ('bg-368f8b', 'Политика'),
}

def main_str(request, category=None):
    search_query = request.GET.get('q', '')
    selected_tags = request.GET.getlist('tags')
    tags = Tag.objects.all()
    topics = Topic.objects.all()

    if category:
        topics = topics.filter(category=category)

    if selected_tags:
        for tag_id in selected_tags:
            topics = topics.filter(tags__id=tag_id)

    if search_query:
        topics = topics.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    for topic in topics:
        color, name = CATEGORY_COLORS.get(topic.category, ('bg-default', 'Категория'))
        topic.category_color = color
        topic.category_name = name

    categories = CATEGORY_COLORS
    return render(request, 'forum/index.html', {
        'topics': topics,
        'categories': categories,
        'tags': tags,
        'selected_tags': list(map(int, selected_tags)),
        'search_query': search_query,
    })

def create_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST, request.FILES)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
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

def single_topic(request, id):
    topic = get_object_or_404(Topic, id=id)
    color, name = CATEGORY_COLORS.get(topic.category, ('bg-default', 'Категория'))
    topic.category_color = color
    topic.category_name = name
    comments = Comment.objects.filter(topic=topic)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.topic = topic
            comment.author = request.user
            comment.save()
            return redirect('single_topic', id=topic.id)
    else:
        comment_form = CommentForm()

    return render(request, 'forum/single-topic.html', {
        'topic': topic,
        'comments': comments,
        'comment_form': comment_form,
    })
