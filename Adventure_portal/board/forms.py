from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Reply


class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': 'Введите заголовок'}))
    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'category',
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if len(title) < 10:
            raise ValidationError({
                'title': 'Заголовок не может быть короче 10 символов или пустым!'
            })


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = [
            'text'
        ]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        if len(text) < 10:
            raise ValidationError({
                'title': 'Отклик не может быть короче 10 символов или пустым!'
            })
