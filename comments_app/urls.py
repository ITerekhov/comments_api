from django.urls import path
from .views import CommentDetailView, PostDetailView

urlpatterns = [
    path('api/add_new_post', PostDetailView.as_view()),
    path('api/reply_to_post', CommentDetailView.as_view()),
    path('api/posts', PostDetailView.as_view()),
    path('api/comment', CommentDetailView.as_view())
]
