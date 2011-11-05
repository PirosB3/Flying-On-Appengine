from django.test import TestCase
from blog.models import *
from django.contrib.auth.models import User

from django.template.defaultfilters import slugify

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
    
  def test_permalink(self):
    self.default_post.save()
    self.assertEqual(self.default_post.get_absolute_url(), '/posts/%s' % self.default_post.slug)