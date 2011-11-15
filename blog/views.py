from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import BaseCreateView, BaseDetailView
from django.http import HttpResponseForbidden, HttpResponseRedirect
from models import *
from forms import *
from mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse

# PUBLIC VIEWS

class PostsShow(BaseCreateView, BaseDetailView, TemplateView):
    """
    Renders a single post, it's comments and a comment form. On post validates the form and adds the comment.
    """
    model = Post
    form_class = CreateCommentForm
    template_name = 'posts/show.html'
    context_object_name = 'post'
    published = None

    def get_context_data(self, **kwargs):
        # on GET, add form context value. on POST, add post context value.
        context_data = super(PostsShow, self).get_context_data(**kwargs)
        if self.request.method == 'GET':
            context_data['form'] = self.get_form_class()
        if self.request.method == 'POST':
            context_data['post'] = self.get_object()
        return context_data

    def form_valid(self, form):
        # If comment form is valid, save with post relationship and re-render post
        comment = form.save(commit=False)
        comment.post = self.get_object()
        comment.save()
        return HttpResponseRedirect(self.get_object().get_absolute_url())

    def get_object(self):
        # gets post object and sets it's published status
        post = super(PostsShow, self).get_object()
        self.published = post.status == 'P'
        return post

    def deny_if_unpublished(self, response):
        if not self.published:
            return HttpResponseForbidden()
        return response

    def post(self, request, *args, **kwargs):
        # if post is not published, will return a 403
        response = super(PostsShow, self).post(request, *args, **kwargs)
        return self.deny_if_unpublished(response)

    def get(self, request, *args, **kwargs):
        # if post is not published, will return a 403
        response = super(PostsShow, self).get(request, *args, **kwargs)
        return self.deny_if_unpublished(response)

class PostsAll(ListView):
    """
    Renders all posts in a list, 10 results at a time
    """
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
    """
    Inherits PostsAll behaviour, with admin goodness
    """
    template_name = 'posts/admin/all.html'
    filter_published = False

class PostsCreateAdmin(LoginRequiredMixin, CreateView):
    """
    Admin view to create a new post
    """
    form_class = CreatePostForm
    template_name = 'posts/admin/create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return HttpResponseRedirect(reverse('blog_posts_all_admin'))

class PostsEditAdmin(LoginRequiredMixin, UpdateView):
    """
    Admin view to edit an existing post
    """
    model = Post
    form_class = CreatePostForm
    template_name = 'posts/admin/create.html'

    def get_success_url(self):
        if self.object.status == 'P':
            return super(PostsEditAdmin, self).get_success_url()
        return reverse('blog_posts_all_admin')

class PostsDeleteAdmin(LoginRequiredMixin, DeleteView):
    """
    Admin view to confirm post deletion
    """
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
