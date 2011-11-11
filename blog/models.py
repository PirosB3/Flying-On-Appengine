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
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User)
    status = models.CharField(max_length= 1, choices= STATUS_CHOICES)
    body = models.TextField(blank=False, help_text="Insert the content for your entry")

    class Meta:
        ordering = ['-date_created']

    @models.permalink
    def get_absolute_url(self):
        return ('blog_posts_show', [str(self.slug)])

    def __unicode__(self):
        return " - ".join([self.title, self.author.username])

    def save(self, *args, **kwargs):
        # validate status
        if self.status not in [x[0] for x in STATUS_CHOICES]:
            raise ValidationError('Invalid status')
        # builds stug if not existing
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Post, self).save(*args, **kwargs)

class Comment(models.Model):

    class Meta:
        ordering = ['-date_created']

    def save(self, *args, **kwargs):
        if self.post and self.post.status == 'P':
            return super(Comment, self).save(*args, **kwargs)
        return False

    post = models.ForeignKey(Post)
    date_created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(help_text="Insert your email address")
    body = models.CharField(blank=False, max_length=100, help_text="Insert your comment here")
