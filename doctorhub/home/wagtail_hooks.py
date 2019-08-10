from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from wagtail.core import hooks


@hooks.register('before_serve_page')
def hit_page(page, request, serve_args, serve_kwargs):
    if isinstance(page, HitCountMixin):
        hit_count = HitCount.objects.get_for_object(page)
        page.hit_count(request, hit_count)
