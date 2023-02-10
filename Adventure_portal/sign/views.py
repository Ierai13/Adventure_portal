from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DeleteView, UpdateView, ListView, FormView, CreateView
from django.core.mail import send_mail

from board.models import Post, Reply
from .forms import EditUserProfileForm, PasswordChangingForm, NewsletterForm
from .filters import ReplyFilter
from .models import UserActivate

import random


def password_creator():
    LOWER = 'abcdefghijklmnopqrstuvwxyz'
    UPPER = LOWER.upper()
    NUMBRES = '1234567890'
    SIMBOLS = '!@#№$%^&?*<>'
    ALL = LOWER + UPPER + NUMBRES + SIMBOLS
    password = ''.join(random.choices(ALL, k=30))
    return password


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'sign/profile.html'



class MyReplyView(LoginRequiredMixin, TemplateView):
    template_name = 'sign/my_reply.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_replyes'] = User.objects.get(id=self.request.user.id).reply.all()
        return context


class MyPostView(LoginRequiredMixin, TemplateView):
    model = Post
    ordering = '-pub_date'
    template_name = 'sign/my_posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_posts'] = Post.objects.filter(author=User.objects.get(id=self.request.user.id))
        return context


class ReplyDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('board.delete_reply')
    model = Reply
    template_name = 'board/delete_reply.html'
    success_url = reverse_lazy('my_replyes')


class UpdateUserView(LoginRequiredMixin, UpdateView):
    form_class = EditUserProfileForm
    template_name = 'sign/edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


class CustomPasswordChangedView(PasswordChangeView):
    template_name = 'sign/password_change.html'
    form_class = PasswordChangingForm
    success_url = reverse_lazy('profile')


class ReplyForMeView(LoginRequiredMixin, ListView):
    model = Reply
    ordering = '-pub_date'
    template_name = 'sign/reply_to_me.html'
    context_object_name = 'replyes'
    paginate_by = 6

    def get_queryset(self):
        queriset = Reply.objects.filter(post__author=self.request.user)
        self.filterset = ReplyFilter(self.request.GET, queriset, request=self.request)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class MailingFormView(FormView):
    template_name = 'sign/mailing.html'
    form_class = NewsletterForm
    success_url = reverse_lazy('all_posts')

    def form_valid(self, form):
        form.send_newsletter()
        return super().form_valid(form)


@login_required
def accept_reply(request, pk):
    try:
        reply = Reply.objects.get(id=pk)
        reply.accept_value = True
        reply.save()

        send_mail(
            subject=f'{reply.author}',
            message=f'Ваш отклик к послу {reply.post.title} был принят!',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[reply.author.email]
        )
    except ObjectDoesNotExist:
        raise Http404
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def reject_reply(request, pk):
    try:
        reply = Reply.objects.get(id=pk)
        reply.accept_value = False
        reply.save()
    except ObjectDoesNotExist:
        raise Http404
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def activate_account(request):
    template = 'sign/activation.html'
    group = Group.objects.get(name='author')
    user = request.user
    if request.method == 'POST':
        cpassword = request.POST['text-password']
        person = UserActivate.objects.get(user=user)
        if person.rpassword == cpassword:
            person.activate_status = True
            group.user_set.add(user)
            person.save()
            return redirect('all_posts')
    return render(request, template)


@login_required
def send_activate_mail(request):
    if not UserActivate.objects.filter(user=request.user):
        password = password_creator()
        UserActivate.objects.create(user=request.user, rpassword=password)
        send_mail(
            subject=f'{request.user.username}',
            message=f'Ваш пароль для активации аккаунта: {password}',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email]
        )
        person = UserActivate.objects.get(user=request.user)
        person.email_sended = True
        person.save()
    else:
        person = UserActivate.objects.get(user=request.user)
        if person.rpassword and not person.activate_status and not person.email_sended:
            password = person.rpassword
            person.email_sended = True
            person.save()
            send_mail(
                subject=f'{request.user.username}',
                message=f'Ваш пароль для активации аккаунта: {password}',
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email]
            )
        elif not person.rpassword and not person.activate_status and not person.email_sended:
            password = password_creator()
            person.rpassword = password
            person.email_sended = True
            person.save()
            send_mail(
                subject=f'{request.user.username}',
                message=f'Ваш пароль для активации аккаунта: {password}',
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email]
            )
    return redirect('activation')
