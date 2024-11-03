from django.shortcuts import render, redirect
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
    if category:
        topics = Topic.objects.filter(category=category)
    else:
        topics = Topic.objects.all()

    for topic in topics:
        color, name = CATEGORY_COLORS.get(topic.category, ('bg-default', 'Категория'))
        topic.category_color = color
        topic.category_name = name

    categories = CATEGORY_COLORS
    return render(request, 'forum/index.html', {'topics': topics, 'categories': categories})

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