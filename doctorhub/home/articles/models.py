from django.db import models
from wagtail.snippets.models import register_snippet


@register_snippet
class ArticleComment(models.Model):
    article = models.ForeignKey(
        'home.ArticlePage', on_delete=models.CASCADE, blank=False
    )



