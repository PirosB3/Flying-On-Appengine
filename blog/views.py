from django.views.generic import ListView, DetailView
from models import *

class PostsShow(DetailView):
  model = Post
  template_name = 'posts/show.html'
  context_object_name = 'post'
  
class PostsAll(ListView):
  model = Post
  template_name = 'posts/all.html'
  context_object_name = 'posts'
  paginate_by = 10