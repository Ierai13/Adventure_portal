from django.urls import path
from django.contrib.auth.decorators import permission_required

from .views import *

urlpatterns = [
    path('profile/', IndexView.as_view(), name='profile'),
    path('mailing/', permission_required('is_staff')(MailingFormView.as_view()), name='mailing'),
    path('profile/editprofile/', UpdateUserView.as_view(), name='update_user'),
    path('profile/my_reply', MyReplyView.as_view(), name='my_replyes'),
    path('profile/my_reply/<int:pk>/', ReplyDelete.as_view(), name='delete_reply'),
    path('profile/replyforme', ReplyForMeView.as_view(), name='reply_for_me'),
    path('profile/replyforme/accept/<int:pk>/', accept_reply, name='accept_reply'),
    path('profile/replyforme/reject/<int:pk>/', reject_reply, name='reject_reply'),
    path('profile/my_posts', MyPostView.as_view(), name='my_posts'),
    path('profile/sendactivationmail', send_activate_mail, name='sendactivationmail'),
    path('profile/activation', activate_account, name='activation'),
    path('profile/password', CustomPasswordChangedView.as_view(), name='password_change')
]