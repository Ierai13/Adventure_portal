from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail


def new_reply(instance):
    if instance:
        post = instance.post
        author = post.author
        email_subject = f'Новый отклик к Вашему посту {post.title}'
        email_message = f'Посмотреть все отклики к этому посту: ' \
                        f'http://127.0.0.1:8000/account/profile/replyforme?post={post.id}'
        send_mail(
            subject=email_subject,
            message=email_message,
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[author.email]
        )