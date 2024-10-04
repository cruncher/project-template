{%- if cookiecutter.add_submodule_slideshow %}
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class SlideShowBlock(blocks.StreamBlock):
    image = ImageChooserBlock()

    class Meta:
        template = "news/blocks/slideshow.html"
        icon = 'image'

{%- endif %}