from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse


class Post(models.Model):
    CHOISES = [
        ('Tanks', 'Танки'),
        ('Healers', 'Хилы'),
        ('DD', 'ДД'),
        ('Traders', 'Торговцы'),
        ('GMs', 'Гилдмастеры'),
        ('QGs', 'Квестгиверы'),
        ('Blacksmiths', 'Кузнецы'),
        ('Leatherworkers', 'Кожевники'),
        ('Potionmaker', 'Зельевары'),
        ('SM', 'Мастера заклинаний')
    ]

    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    text = RichTextUploadingField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=CHOISES, default='Танки')

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.title}'


class Reply(models.Model):
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply')
    text = models.TextField()
    accept_value = models.BooleanField(default=None, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

