from django.test import TestCase
from blog.models import *
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.test.client import Client
from django.core.urlresolvers import reverse

# Models
class TestPost(TestCase):
  fixtures = ['users.json']
  
  def setUp(self):
    self.user = User.objects.get(pk=31)
    self.default_post = Post(title='Hello World', body='Lorem ipsum', status='P', author= self.user)
  
  def test_slug_correctly_setup(self):
    """ ensures slug is generated correctly on save """
    self.default_post.save()
    self.assertEqual(self.default_post.slug, slugify(self.default_post.title))
  
  def test_status_choices(self):
    """ status must be declared in STATUS_CHOICES """
    self.default_post.status = 'Z'
    with self.assertRaises(ValidationError):
      self.default_post.save()
      
  def test_unicode(self):
    self.assertEqual('Hello World - test_admin', str(Post(title="Hello World", body="asd", author= self.user)))
    
class TestComment(TestCase):
  fixtures = ['posts.json']
  
  def setUp(self):
    self.post = Post.objects.get(pk=33)
  
  def test_raise_if_post_not_published(self):
    self.post.status = 'D'
    self.post.save()
    self.assertFalse(Comment(email='lol@email.com', body='cool article', post = self.post).save())

# Urls    
class TestBlogUrls(TestCase):
  fixtures = ['users.json', 'posts.json']
  def setUp(self):
    self.post = Post.objects.get(pk=33)
  
  def test_permalink(self):
    """ ensures correct permalink for absolute url """
    self.assertEqual(self.post.get_absolute_url(), '/posts/show/%s' % self.post.slug)
    
  def test_not_published(self):
    """ if post not published, will return a 403 """
    self.post.status = 'D'
    self.post.save()
    response = Client().get(self.post.get_absolute_url())
    self.assertEqual(response.status_code, 403)

# Functional  
class TestWorkflow(TestCase):
  fixtures = ['users.json', 'posts.json', 'comments.json']
  
  def setUp(self):
    self.client = Client()
    self.client.login(username="test_admin", password="test")
    self.post = Post.objects.get(pk=33)
    self.comment = Comment.objects.get(pk=80)
    
  def test_admin_page(self):
    response = self.client.get(reverse('blog_posts_all_admin'))
    self.assertEqual(response.status_code, 200)
    
  def test_admin_edit_published_post(self):
    response = self.client.post(reverse('blog_posts_edit_admin', args=[self.post.slug]), {'title' : 'just changed you!', 'body' : self.post.body, 'status' : self.post.status })
    self.assertEqual(Post.objects.get(title='just changed you!').pk, 33)
    
  def test_delete_without_confirm(self):
    self.client.post(reverse('blog_posts_delete_admin', args=[self.post.slug]))
    self.assertTrue(Post.objects.get(pk=33))
    
  def test_delete_with_confirm(self):
    self.client.post(reverse('blog_posts_delete_admin', args=[self.post.slug]), {'confirm' : 'true'})
    with self.assertRaises(Post.DoesNotExist):
      Post.objects.get(pk=33)
      
  def test_create_comment_successful(self):
    response = self.client.post(reverse('blog_posts_show', args=[self.post.slug]), {'email' : 'test@google.com', 'body' : 'brilliant!'})
    # CHECK REDIRECT
    self.assertEqual(len(Comment.objects.all()), 2)
    
  def test_create_comment_not_complete(self):
    response = self.client.post(reverse('blog_posts_show', args=[self.post.slug]), {'email' : 'testgoogle.com', 'body' : 'brilliant!'})
    # CHECK REDIRECT
    self.assertEqual(len(Comment.objects.all()), 1)
    
  def test_create_comment_not_published(self):
    self.post.status = 'D'
    self.post.save()
    response = self.client.post(reverse('blog_posts_show', args=[self.post.slug]), {'email' : 'test@google.com', 'body' : 'brilliant!'})
    self.assertEqual(len(Comment.objects.all()), 1)
  
  def test_delete_comment_unsuccessful(self):
    self.client.post(reverse('blog_comments_delete_admin', args=[str(self.comment.id)]))
    # CHECK REDIRECT
    self.assertEqual(len(Comment.objects.all()), 1) 
  
  def test_delete_comment_successful(self):
    self.client.post(reverse('blog_comments_delete_admin', args=[str(self.comment.id)]), {'confirm' : 'true'})
    # CHECK REDIRECT
    self.assertEqual(len(Comment.objects.all()), 0)
    