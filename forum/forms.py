from django import forms
from django.contrib.auth.models import User
from .models import Topic, Comment

class LoginForm(forms.Form):
    username = forms.CharField(label='Никнейм', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords dont match.')
        return cd['password2']


class TopicForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('hobby', 'Хобби'),
        ('video', 'Видео'),
        ('art', 'Искусство'),
        ('games', 'Игры'),
        ('health', 'Здоровье'),
        ('entertainment', 'Развлечения'),
        ('qa', 'Q&A'),
        ('society', 'Общество'),
        ('random', 'Случайное'),
        ('tech', 'Технологии'),
        ('science', 'Наука'),
        ('animals', 'Животные'),
        ('education', 'Образование'),
        ('politics', 'Политика'),
    ]

    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        label="Категория",
        widget=forms.Select(attrs={'class': 'custom-select'})
    )

    tags = forms.CharField(
        required=False,
        label="Теги",
        widget=forms.TextInput(attrs={'placeholder': 'Введите теги через запятую'})
    )

    class Meta:
        model = Topic
        fields = ['title', 'category', 'description', 'tags', 'image']
        labels = {
            'title': 'Заголовок темы',
            'category': 'Категория',
            'description': 'Описание',
            'tags': 'Теги',
            'image': 'Изображение',
        }

    def __init__(self, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите заголовок'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите описание'})
        self.fields['tags'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'image']
        labels = {
            'text': 'Текст комментария',
            'image': 'Изображение',
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Напишите ваш комментарий здесь...'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
