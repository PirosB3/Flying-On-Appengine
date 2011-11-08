from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpResponseForbidden, HttpResponseRedirect
from models import *
from forms import *
from mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse

# PUBLIC VIEWS

class PostsShow(DetailView):
  model = Post
  template_name = 'posts/show.html'
  context_object_name = 'post'
  published = None
  
  def get_object(self):
    """ gets post object and sets it's published status """
    post = super(PostsShow, self).get_object()
    self.published = post.status == 'P'
    return post
    
  def get(self, request, *args, **kwargs):
    """ if post is not published, will return a 403 """
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

# ADMINISTRATED VIEWS

class PostsAllAdmin(LoginRequiredMixin, PostsAll):
  template_name = 'posts/admin/all.html'
  
class PostsCreateAdmin(LoginRequiredMixin, CreateView):
  form_class = CreatePostForm
  template_name = 'posts/admin/create.html'
  
  def form_valid(self, form):
    post = form.save(commit=False)
    post.author = self.request.user
    post.save()
    return HttpResponseRedirect(reverse('blog_posts_all_admin'))
    