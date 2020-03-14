from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'www', settings.ROOT_URLCONF, name='www'),
    # host(r'blog', 'blog.urls', name='blog-subdomain'),
    host(r'search', 'coresearch.urls', name='search-subdomain'),
)