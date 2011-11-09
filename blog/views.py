from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
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
  filter_published = True
  
  def get_queryset(self):
    if self.filter_published:
      return Post.objects.filter(status='P')
    return super(PostsAll, self).get_queryset()

# ADMIN VIEWS

class PostsAllAdmin(LoginRequiredMixin, PostsAll):
  template_name = 'posts/admin/all.html'
  filter_published = False
  
class PostsCreateAdmin(LoginRequiredMixin, CreateView):
  form_class = CreatePostForm
  template_name = 'posts/admin/create.html'
  
  def form_valid(self, form):
    post = form.save(commit=False)
    post.author = self.request.user
    post.save()
    return HttpResponseRedirect(reverse('blog_posts_all_admin'))
    
class PostsEditAdmin(LoginRequiredMixin, UpdateView):
  model = Post
  form_class = CreatePostForm
  template_name = 'posts/admin/create.html'
  
  def get_success_url(self):
    if self.object.status == 'P':
      return super(PostsEditAdmin, self).get_success_url()
    return reverse('blog_posts_all_admin')
    
class PostsDeleteAdmin(LoginRequiredMixin, DeleteView):
  model = Post
  template_name = 'posts/admin/delete.html'
  context_object_name = 'post'
  
  def post(self, request, slug):
    """ensure box ticked on POST request"""
    if 'confirm' not in request.POST.keys():
      return HttpResponseRedirect(reverse('blog_posts_delete_admin', args=[slug]))
    return super(PostsDeleteAdmin, self).post(request, slug)
  
  def get_success_url(self):
    return reverse('blog_posts_all_admin')