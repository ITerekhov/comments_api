import json

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import JsonResponse
from django.views import View
from django.db.models import F 

from .models import Post, Comment


class CommentDetailView(View):

    def get(self, request):
        comment_id = request.GET.get('id')
        try:
            comment = Comment.objects.get(pk=comment_id)
        except ObjectDoesNotExist:
            return JsonResponse(
                {'error': 'Комментарий с указанным id не существует'},
                status=404)
        all_comments = Comment.objects.filter(post=comment.post).select_related('parent')
        serialized_comment = serialize_comments([comment], all_comments)
        return JsonResponse({'comment': serialized_comment})

    def post(self, request):
        post_body = json.loads(request.body)
        post_id = post_body.get('post_id')
        if not post_id:
            return JsonResponse(
                {'error': 'Укажите id поста'},
                status=400,
            )
        text = post_body.get('text')
        try:
            post_id = Post.objects.get(pk=post_id)
        except (ObjectDoesNotExist, ValueError):
            return JsonResponse(
                {'error': 'Пост с указанным id не существует'},
                status=404
            )
        parent_id = post_body.get('parent')
        if parent_id:
            try:
                parent=Comment.objects.get(pk=parent_id)
                Comment.objects.create(
                    text=text, 
                    post=post_id,
                    parent=parent,
                    level = parent.level + 1
                )
            except (ObjectDoesNotExist, ValueError):
                return JsonResponse(
                    {'error': 'Комментарий с указанным id не существует'},
                )
        else:
            Comment.objects.create(text=text, post=post_id)
        return JsonResponse({'text': 'Комментарий успешно создан'},
                            status=201)


def serialize_comments(comments_level, all_comments):
    response = []
    for comment in comments_level:
        serialized_comment = {'id': comment.id, 
               'text': comment.text, 
               'level': comment.level,
               'replies': serialize_comments([i for i in all_comments if i.parent == comment], all_comments)}
        response.append(serialized_comment)
    return response

class PostDetailView(View):
    def get(self, request):
        post_title = request.GET.get('title', '')
        try:
            posts = Post.objects.filter(title__contains=post_title).prefetch_related('comments__parent')
        except ObjectDoesNotExist:
            return JsonResponse(
                {'error': 'Пост с указанным названием не существует'},
                status=404)
        response = {}
        for post in posts:
            all_comments = post.comments.all()
            serialized_comments = serialize_comments([i for i in all_comments if not i.parent], all_comments)
            response[post.title] = {
                'id': post.id,
                'title': post.title,
                'text': post.text,
                'comments': serialized_comments
            }
        return JsonResponse(response, status=200)

    def post(self, request):
        post_body = json.loads(request.body)
        title = post_body.get('title')
        if not title:
            return JsonResponse(
                {'error': 'Укажите заголовок поста'},
                status=400
            )
        text = post_body.get('text', '')
        try:
            Post.objects.create(title=title, text=text)
        except IntegrityError:
            return JsonResponse(
                {'error': 'Пост с таким названием уже существует'}, status=400)
        return JsonResponse({'text': 'Пост успешно создан'}, status=201)
