"""urlconf for the base application"""

from django.conf.urls import url, patterns


urlpatterns = patterns('base.views',
    url(r'^$', 'mysql', name='mysql'),
    url(r'^mysql$', 'mysql', name='mysql'),
    url(r'^mysql/students/add$', 'mysql_add_student', name='mysql_add_student'),
    url(r'^mysql/students/delete/(?P<student_id>\w{0,50})$', 'mysql_delete_student', name='delete_student' ),

    url(r'^dynamo$', 'dynamo', name='dynamo'),
    url(r'^dynamo/(?P<attribute>\w{0,50})/$', 'dynamo_by_attribute', name='dynamo_by_attribute'),
    url(r'^dynamo/students/add$', 'dynamo_add_student', name='add_student'),
    url(r'^dynamo/students/delete/(?P<student_id>\w{0,50})$', 'dynamo_delete_student', name='delete_student' ),
    url(r'^dynamo/clear$', 'clear_dynamo', name='clear_dynamo'),
)
