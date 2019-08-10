from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class ParagraphBlock(blocks.StructBlock):
    paragraph = blocks.RichTextBlock()


class ImageParagraphBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    paragraph = blocks.RichTextBlock()


class LinkableParagraph(blocks.StructBlock):
    title = blocks.TextBlock()
    paragraph = blocks.RichTextBlock()


class LinkableImageParagraph(blocks.StructBlock):
    title = blocks.TextBlock()
    image = ImageChooserBlock(help_text='square image')
    paragraph = blocks.RichTextBlock()
