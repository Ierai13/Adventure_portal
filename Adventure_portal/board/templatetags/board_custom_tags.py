from django import template

from board.models import Reply
from sign.models import UserActivate

register = template.Library()


# Тэг для проверки откликов пользователя, если пользователь оставлял отклик, вернет True, иначе False
@register.simple_tag()
def reply_check(user=None, post_id=None):
    reply = Reply.objects.filter(author=user, post__id=post_id)
    if reply:
        return True
    else:
        return False


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()


# Тег для проверки активации аккаунта
@register.simple_tag()
def check_activation(user):
    person = UserActivate.objects.filter(user=user).first()
    if person:
        if person.activate_status:
            return False
        else:
            return True
    else:
        return True


# Тег для отображения откликов только на объявления, которые пренадлежат пользователю
@register.simple_tag()
def sort_replyes(replylist, user):
    clear_reply = []
    for reply in replylist:
        if reply.post.author == user:
            clear_reply.append(reply)
    return clear_reply
