from django.conf.urls.defaults import patterns, include, url
from views import PostsShow, PostsAll, PostsAllAdmin

urlpatterns = patterns('',
  url(r'admin/', PostsAllAdmin.as_view(), name="blog_posts_all_admin"),
  url(r'^show/(?P<slug>[^\.]+)$', PostsShow.as_view(), name='blog_posts_show'),
  url(r'^$', PostsAll.as_view(), name='blog_posts_all'),
)