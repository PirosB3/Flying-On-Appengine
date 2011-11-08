from django.views.generic import ListView, DetailView
from django.http import HttpResponseForbidden
from models import *
from mixins import LoginRequiredMixin

class PostsShow(DetailView):
  model = Post
  template_name = 'posts/show.html'
  context_object_name = 'post'
  published = None
  
  def get_object(self):
    post = super(PostsShow, self).get_object()
    self.published = post.status == 'P'
    return post
    
  def get(self, request, *args, **kwargs):
    response = super(PostsShow, self).get(request, *args, **kwargs)
    if not self.published:
      return HttpResponseForbidden()
    return response

class PostsAll(ListView):
  model = Post
  template_name = 'posts/all.html'
  context_object_name = 'posts'
  paginate_by = 10
  
  def get_queryset(self):
    return Post.objects.filter(status='P')
  
class PostsAllAdmin(LoginRequiredMixin, PostsAll):
  template_name = 'posts/admin/all.html'