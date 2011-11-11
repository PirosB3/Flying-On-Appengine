from django import forms
from blog.models import *

class CreatePostForm(forms.ModelForm):
  class Meta:
    fields = ('title', 'status', 'body')
    model = Post
    
class CreateCommentForm(forms.ModelForm):
  class Meta:
    fields = ('email', 'body')
    model = Comment