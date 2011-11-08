from django.test import TestCase
from blog.models import *
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.test.client import Client

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
    self.default_post.status = 'Z'
    with self.assertRaises(ValidationError):
      self.default_post.save()
      
class TestBlogUrls(TestCase):
  fixtures = ['users.json', 'posts.json']
  def setUp(self):
    self.post = Post.objects.get(pk=33)
  
  def test_permalink(self):
    self.assertEqual(self.post.get_absolute_url(), '/posts/show/%s' % self.post.slug)
    
  def test_not_published(self):
    self.post.status = 'D'
    self.post.save()
    response = Client().get(self.post.get_absolute_url())
    self.assertEqual(response.status_code, 403)