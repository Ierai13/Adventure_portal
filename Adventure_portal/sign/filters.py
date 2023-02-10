from django import forms
from django_filters import FilterSet, ModelChoiceFilter, DateFilter
from board.models import Reply, Post


def postauthor(request):
    if request is None:
        return Post.objects.none()

    return Post.objects.filter(author=request.user)


class ReplyFilter(FilterSet):

    post = ModelChoiceFilter(
        field_name='post',
        queryset=postauthor,
        label='Выберите объявление',
        empty_label='Любое'
    )


