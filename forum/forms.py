from django import forms
from .models import Topic

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