import json

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import JsonResponse
from django.views import View

from .models import Post, Comment


class CommentDetailView(View):

    def get(self, request):
        comment_id = request.GET.get('id')
        try:
            comment = Comment.objects.get(pk=comment_id)
        except ObjectDoesNotExist:
            return JsonResponse(
                {'text': 'Комментарий с указанным id не существует'},
                status=404)
        return JsonResponse({'comment': comment.serialize_object()})

    def post(self, request):
        post_body = json.loads(request.body)
        text = post_body.get('text')
        try:
            post_id = Post.objects.get(pk=post_body['post_id'])
        except ObjectDoesNotExist:
            return JsonResponse(
                {'text': 'Пост с указанным id не существует'},
                status=404)
        parent = post_body.get('parent')
        if parent:
            Comment.objects.create(text=text, post=post_id,
                                   parent=Comment.objects.get(pk=parent))
        else:
            Comment.objects.create(text=text, post=post_id)
        return JsonResponse({'text': 'Комментарий успешно создан'},
                            status=201)

            
class PostDetailView(View):
    def get(self, request):
        post_title = request.GET.get('title', '')
        try:
            posts = Post.objects.filter(title__contains=post_title)
        except ObjectDoesNotExist:
            return JsonResponse(
                {'text': 'Пост с указанным названием не существует'},
                status=404)
        response = {}
        for post in posts:
            comments = []
            for comment in post.comments.filter(level=0):
                comments.append(comment.serialize_object(limit=2))
            response[post.title] = {
                'id': post.id,
                'title': post.title,
                'text': post.text,
                'comments': comments
            }
        return JsonResponse(response, status=200)

    def post(self, request):
        post_body = json.loads(request.body)
        try:
            Post.objects.create(title=post_body['title'],
                                text=post_body['text'])
        except IntegrityError:
            return JsonResponse(
                {'text': 'Пост с таким названием уже существует'}, status=400)
        return JsonResponse({'text': 'Пост успешно создан'}, status=201)
