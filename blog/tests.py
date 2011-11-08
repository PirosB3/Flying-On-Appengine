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
    
class TestWorkflow(TestCase):
  fixtures = ['users.json']
  
  def setUp(self):
    self.client = Client()
    self.client.login(username="test_admin", password="test")
    
  def test_admin_page(self):
    response = self.client.get(reverse('blog_posts_all_admin'))
    self.assertEqual(response.status_code, 200)
    
  def test_admin_create_post(self):
    self.client.post(reverse('blog_posts_create_admin'), {'title' : 'My post', 'status' : 'P', 'body' : 'lorem ipsum..'})
    self.assertEqual(Post.objects.get(title='My post').body, 'lorem ipsum..')