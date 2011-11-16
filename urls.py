from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    url(r'^_ah/warmup$', 'djangoappengine.views.warmup'),
    url(r'^accounts/login', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout', 'django.contrib.auth.views.logout'),
    url(r'^accounts/', 'django.views.generic.simple.redirect_to', {'url' : '/'}),
    url(r'^', include('blog.urls')),
)
