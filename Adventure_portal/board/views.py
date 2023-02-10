from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from django.contrib.auth.decorators import login_required

from .forms import PostForm, ReplyForm
from .models import Post, Reply


class PostView(ListView):
    model = Post
    ordering = '-pub_date'
    template_name = 'board/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['form'] = ReplyForm
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'board/post_detail.html'
    context_object_name = 'post_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['form'] = ReplyForm
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('board.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'board/post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('board.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'board/post_create.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('board.delete_post',)
    model = Post
    template_name = 'board/delete_post.html'
    success_url = reverse_lazy('all_posts')


class PostSortView(ListView):
    template_name = 'board/post_list.html'
    paginate_by = 6

    def get_queryset(self):
        queryset = Post.objects.filter(category=self.request.path[1:-1])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        category = self.request.path[1:-1]
        context['posts'] = Post.objects.filter(category=category).order_by('-pub_date')
        return context


def categoryview(request, category):
    template = 'board/post_list.html'
    posts = Post.objects.filter(category=category)
    context = {
        'posts': posts
    }
    return render(request, template, context)


@login_required
def add_reply(request, pk):
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            Reply.objects.create(author=User.objects.get(id=request.user.id), text=request.POST['text'],
                                 post=Post.objects.get(id=pk))
            return redirect('all_posts')
    else:
        return redirect('all_posts')
