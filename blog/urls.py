from django.conf.urls.defaults import patterns, include, url
from views import PostsShow, PostsAll, PostsAllAdmin, PostsCreateAdmin, PostsEditAdmin, PostsDeleteAdmin

urlpatterns = patterns('',
  url(r'admin/posts/delete/(?P<slug>[^\.]+)$', PostsDeleteAdmin.as_view(), name="blog_posts_delete_admin"),
  url(r'admin/posts/edit/(?P<slug>[^\.]+)$', PostsEditAdmin.as_view(), name="blog_posts_edit_admin"),
  url(r'admin/posts/create', PostsCreateAdmin.as_view(), name="blog_posts_create_admin"),
  url(r'admin/', PostsAllAdmin.as_view(), name="blog_posts_all_admin"),
  url(r'^show/(?P<slug>[^\.]+)$', PostsShow.as_view(), name='blog_posts_show'),
  url(r'^$', PostsAll.as_view(), name='blog_posts_all'),
)
