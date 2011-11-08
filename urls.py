from django.conf.urls.defaults import *

import blog

from django.contrib import admin
admin.autodiscover()

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    url('^_ah/warmup$', 'djangoappengine.views.warmup'),
    url(r'^admin/', include(admin.site.urls)),
    url('^posts/', include('blog.urls')),
    url('^$', 'django.views.generic.simple.redirect_to', {'url' : '/posts/'})
)
