from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError

STATUS_CHOICES = (
    ('P', 'Published'),
    ('D', 'Draft'),
)

class Post(models.Model):
  """ An entry to the blog """
  title = models.CharField(blank=False, max_length=50, help_text="Insert the title for your entry")
  slug = models.SlugField()
  date_created = models.DateTimeField(auto_now_add=True)
  author = models.ForeignKey(User)
  status = models.CharField(max_length= 1, choices= STATUS_CHOICES)
  body = models.TextField(blank=False, help_text="Insert the content for your entry")
  
  @models.permalink
  def get_absolute_url(self):
    return ('blog_posts_show', [str(self.slug)])
  
  def save(self, *args, **kwargs):
    # validate status
    if self.status not in [x[0] for x in STATUS_CHOICES]:
      raise ValidationError('Invalid status')
    # builds stug if not existing
    if not self.slug:
      self.slug = slugify(self.title)
    super(Post, self).save(*args, **kwargs)