from django.core.cache import cache

from blog.models import Blog
from config.settings import CACHE_ENABLE


def get_blog_from_cache():
    if not CACHE_ENABLE:
        return Blog.objects.all()
    key = 'blog_list'
    blog = cache.get(key)
    if blog is not None:
        return blog
    blog = Blog.objects.all()
    cache.set(key, blog)
    return blog
