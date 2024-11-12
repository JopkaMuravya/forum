from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm, TopicForm, CommentForm, CustomUser_ChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.mail import send_mail
import uuid
from .models import Topic, Tag, Comment, Like, Notification, CustomUser
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


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
            new_user.verification_token = str(uuid.uuid4())
            new_user.save()
            send_verification_email(new_user)
            login(request, new_user)
            return redirect('main_str')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'forum/simple-signup.html', {'user_form': user_form})


def send_verification_email(user):
    verification_link = f"http://localhost:8000/verify_email/{user.verification_token}/"
    send_mail(
        'Подтверждение электронной почты',
        f'Перейдите по ссылке для подтверждения: {verification_link}',
        'from@example.com',
        [user.email],
        fail_silently=False,
    )


def verify_email(request, token):
    try:
        user = CustomUser.objects.get(verification_token=token)
        user.email_verified = True
        user.verification_token = ''
        user.save()
        return redirect('main_str')
    except CustomUser.DoesNotExist:
        return render(request, 'forum/invalid_token.html')



@login_required
def user_account(request):
    user = request.user

    if request.method == 'POST':
        user_form = CustomUser_ChangeForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            user_form.save()
            return redirect('main_str')
    else:
        user_form = CustomUser_ChangeForm(instance=user)

    avatar_url = user.avatar.url if hasattr(user, 'avatar') and user.avatar else None

    return render(request, 'forum/acaunt.html', {'user_form': user_form, 'avatar_url': avatar_url})

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

    if request.GET.get('my_topics') == 'true' and request.user.is_authenticated:
        topics = topics.filter(author=request.user)

    if request.GET.get('liked_topics') == 'true' and request.user.is_authenticated:
        topics = topics.filter(likes__user=request.user)

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
        topic.comment_count = topic.comments.count()
    unread_notifications_count = 0
    notifications = []
    if request.user.is_authenticated:
        unread_notifications_count = request.user.notification_set.filter(is_read=False).count()
        notifications = request.user.notification_set.order_by('-created_at')

    categories = CATEGORY_COLORS
    return render(request, 'forum/index.html', {
        'topics': topics,
        'categories': categories,
        'tags': tags,
        'selected_tags': list(map(int, selected_tags)),
        'search_query': search_query,
        'unread_notifications_count': unread_notifications_count,
        'notifications': notifications,
    })


def create_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST, request.FILES)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            if hasattr(request.user, 'avatar') and request.user.avatar:
                topic.avatar = request.user.avatar.url
            else:
                topic.avatar = '../static/images/skuf_9.jpg'
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

    user_liked = topic.likes.filter(id=request.user.id).exists()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.topic = topic
            comment.author = request.user
            if hasattr(request.user, 'avatar') and request.user.avatar:
                comment.avatar = request.user.avatar.url
            else:
                comment.avatar = '../static/images/skuf_9.jpg'
            comment.save()
            if topic.author != request.user:
                Notification.objects.create(
                    user=topic.author,
                    topic=topic,
                    notification_type='reply',
                    created_at=timezone.now(),
                    is_read=False
                )
            return redirect('single_topic', id=topic.id)
    else:
        comment_form = CommentForm()

    return render(request, 'forum/single-topic.html', {
        'topic': topic,
        'comments': comments,
        'comment_form': comment_form,
        'user_liked': user_liked,
    })


@login_required
def toggle_like(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    like, created = Like.objects.get_or_create(user=request.user, topic=topic)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True
        if topic.author != request.user:
            Notification.objects.create(
                user=topic.author,
                topic=topic,
                notification_type='like',
                created_at=timezone.now(),
                is_read=False
            )

    return JsonResponse({
        'liked': liked,
        'total_likes': topic.likes.count(),
    })


@login_required
def mark_notifications_read(request):
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)
