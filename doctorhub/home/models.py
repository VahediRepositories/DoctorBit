from django import forms
from django.utils.text import slugify
from hitcount.views import HitCountMixin
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalManyToManyField, ParentalKey
from taggit.models import TaggedItemBase, Tag as TaggitTag
from wagtail.admin.edit_handlers import StreamFieldPanel, MultiFieldPanel
from wagtail.core.blocks import StreamBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtailmetadata.models import MetadataPageMixin

from .blocks import *
from .categories.models import *
from .articles.blocks import *


class HomePage(Page):
    subpage_types = [
        'home.ArticlesCategoryPage'
    ]


class ArticlesCategoryPage(MetadataPageMixin, Page):
    category = models.ForeignKey(
        ArticleCategory, blank=False, on_delete=models.SET_NULL, null=True
    )

    content_panels = [
        SnippetChooserPanel('category')
    ]

    def get_home_page(self):
        return self.get_parent().specific

    promote_panels = []
    settings_panels = []

    def clean(self):
        super().clean()
        self.title = self.category.name
        self.slug = slugify(self.title, allow_unicode=True)

    parent_page_types = [
        'home.HomePage'
    ]
    subpage_types = [
        'home.ArticlePage'
    ]


class ArticleTag(TaggedItemBase):
    content_object = ParentalKey(
        'ArticlePage', related_name='article_tags', on_delete=models.CASCADE
    )


class ArticlePage(MetadataPageMixin, HitCountMixin, Page):
    image = models.ForeignKey(
        'wagtailimages.Image',
        help_text='square image',
        null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    categories = ParentalManyToManyField(ArticleCategory, blank=True)
    tags = ClusterTaggableManager(
        through=ArticleTag, blank=True
    )

    summary = StreamField(
        StreamBlock(
            [
                ('summary', SummaryBlock())
            ], min_num=1, max_num=1, required=True
        ), blank=False, null=True
    )
    introduction = StreamField(
        StreamBlock(
            [
                ('introduction', IntroductionBlock())
            ], min_num=1, max_num=1, required=True
        ), blank=False, null=True
    )
    conclusion = StreamField(
        StreamBlock(
            [
                ('conclusion', ConclusionBlock())
            ], min_num=0, max_num=1, required=True
        ), blank=False, null=True
    )

    paragraphs = StreamField([
        ('paragraph', ParagraphBlock()),
        ('image_paragraph', ImageParagraphBlock()),
        ('linkable_image_paragraph', LinkableImageParagraph()),
        ('linkable_paragraph', LinkableParagraph())
    ], blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('image'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
            FieldPanel('tags'),
        ], heading='Details', classname="collapsible collapsed"),
        MultiFieldPanel([
            StreamFieldPanel('summary'),
            StreamFieldPanel('introduction'),
            StreamFieldPanel('paragraphs'),
            StreamFieldPanel('conclusion'),
        ], heading='Paragraphs', classname="collapsible collapsed"),
    ]

    promote_panels = Page.promote_panels
    settings_panels = []

    def get_summary(self):
        return self.summary[0].value['paragraph']

    def get_introduction(self):
        return self.introduction[0].value['paragraph']

    def get_conclusion(self):
        return self.conclusion[0].value['paragraph']

    def get_context(self, request):
        linkable_paragraphs = []
        for paragraph in self.paragraphs:
            block_type = paragraph.block_type
            if 'linkable' in block_type:
                linkable_paragraphs.append(paragraph)
        context = super().get_context(request)
        context['linkable_paragraphs'] = linkable_paragraphs
        return context

    def get_home_page(self):
        return self.get_parent().specific.get_home_page()

    parent_page_types = [
        'home.ArticlesCategoryPage'
    ]
    subpage_types = []
