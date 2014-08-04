"""urlconf for the base application"""

from django.conf.urls import url, patterns


urlpatterns = patterns('base.views',
    url(r'^$', 'client_home'),
    url(r'^desktops/create$', 'create_desktop'),
    url(r'^desktops/delete/(?P<desktop_name>\w{0,50})$', 'delete_desktop'),
    url(r'^desktops/toggle/(?P<current_state>\w{0,50})/(?P<desktop_id>i-[0-9,a-z]{0,10})$', 'toggle_state'),
)

urlpatterns += patterns('',
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
)
