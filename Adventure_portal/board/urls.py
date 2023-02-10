from django.urls import path
from .views import *


urlpatterns = [
    path('', PostView.as_view(), name='all_posts'),
    path('detail/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('detail/<int:pk>/edit', PostEdit.as_view(), name='post_edit'),
    path('detail/<int:pk>/delete', PostDelete.as_view(), name='delete_post'),
    path('<category>/', PostSortView.as_view(), name='post_in_category'),
    path('detail/<int:pk>/sendreply/', add_reply, name='sendreply'),
]