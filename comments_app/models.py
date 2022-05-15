from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    text = models.TextField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(blank=True)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий'
    )
    parent = models.ForeignKey(
        'self',
        related_name='children',
        verbose_name='Ответ к комментарию',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    level = models.IntegerField(default=0)

    class MPTTMeta:
        order_insertion_by = ['text']
