from allauth.account.forms import SignupForm, LoginForm
from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import Group, User
from django.core.mail import send_mail
from django.conf.global_settings import DEFAULT_FROM_EMAIL

import datetime as dt


class EditUserProfileForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Введите Ваш email'}))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                               'placeholder': 'Введите Ваше имя'}), )
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                              'placeholder': 'Введите Вашу фамилию'}), )
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Введите Ваш никнейм'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль',
                                   widget=forms.PasswordInput(
                                       attrs={'class': 'form-control', 'placeholder': 'Введите Ваш текущий пароль'}))
    new_password1 = forms.CharField(label='Новый пароль',
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'form-control', 'placeholder': 'Введите новый пароль'}))
    new_password2 = forms.CharField(label='Новый пароль еще раз',
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'form-control', 'placeholder': 'Введите новый пароль еще раз'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


NewsletterCHOISE = (('1', 'Техработы'), ('2', 'Информационное сообщение'))
mail_title = {'1': 'Техработы', '2': 'Информационное сообщение'}
users = User.objects.filter(is_staff=False, is_superuser=False)
users_email = []
for i in users:
    users_email.append(i.email)
HOUR_CHOICES = [(dt.time(hour=x), '{:02d}'.format(x)) for x in range(0, 24)]


class NewsletterForm(forms.Form):
    head = forms.ChoiceField(choices=NewsletterCHOISE, label='Тема', widget=forms.Select(
        attrs={'class': 'form-select', 'style': 'max-width:40%'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 15}),
                           label='Сообщение')

    def send_newsletter(self):
        send_mail(
            subject=mail_title[self.cleaned_data['head']],
            message=self.cleaned_data['text'],
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=users_email
        )


class CustomLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        # добавление аргументов в widget к определенным полям
        self.fields['login'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        # для добавления агрументов в widget ко всем полям:
        # for fieldname, field in self.fields.items():
        #     field.widget.attrs.update({'class': 'form-control'})


class CustomSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
