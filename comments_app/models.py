from django.db import models

from mptt.models import MPTTModel, TreeForeignKey


class Post(models.Model):

    title = models.CharField(max_length=200, unique=True)
    text = models.TextField()

    def __str__(self):
        return self.title


class Comment(MPTTModel):
    text = models.TextField(null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['text']

    def serialize_object(self, limit=float('inf')):
        '''Функция упаковывает объект комментария
           со всеми ответами на него в словарь'''
        if self.level > limit:
            return None
        obj = {'id': self.id, 'level': self.level,
               'post': self.post.title,
               'text': self.text, 'replies': []}
        for child in self.get_children():
            obj['replies'].append(child.serialize_object(limit))
        return obj
