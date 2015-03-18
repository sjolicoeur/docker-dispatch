from django.conf.urls import patterns, include, url
# from django.contrib.auth import views as auth_views
# from registry.dock.views import DockerImageDeployJobCreate
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'registry.views.home', name='home'),
    # url(r'^registry/', include('registry.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url('^accounts/', include('django.contrib.auth.urls')),
    url('^/?$', 'registry.dock.views.home'),
    # url(r'^dock/add/$', DockerImageDeployJobCreate.as_view(), name='author_add'),
)
