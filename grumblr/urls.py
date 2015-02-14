from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'grumblr.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('grumblrApp.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grumblrApp/', include('grumblrApp.urls')),
)
