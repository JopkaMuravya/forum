from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .forms import TopicForm
from .models import Topic, Tag

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

def single_topic(request, id):
    topic = get_object_or_404(Topic, id=id)
    color, name = CATEGORY_COLORS.get(topic.category, ('bg-default', 'Категория'))
    topic.category_color = color
    topic.category_name = name
    return render(request, 'forum/single-topic.html', {'topic': topic})