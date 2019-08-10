from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet


class Category(models.Model):
    name = models.CharField(
        max_length=300, unique=True, blank=False
    )

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'), ImageChooserPanel('image')
    ]

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


@register_snippet
class ArticleCategory(Category):
    class Meta:
        verbose_name_plural = 'articles categories'

