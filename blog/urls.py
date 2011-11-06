from django.conf.urls.defaults import patterns, include, url
from views import PostsShow

urlpatterns = patterns('',
  url(r'^posts/show/(?P<slug>[^\.]+)$', PostsShow.as_view(), name='blog_posts_show'),
)