"""urlconf for the base application"""

from django.conf.urls import url, patterns


urlpatterns = patterns('base.views',
    url(r'^$', 'client_home'),
    url(r'^desktops/create$', 'create_desktop'),
    url(r'^desktops/delete/(?P<desktop_name>\w{0,50})$', 'delete_desktop'),
)

urlpatterns += patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
)
