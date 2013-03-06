from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'cashground.views',
    url(r'^$', 'cashground'),
    url(r'^request/$', 'request'),
    url(r'^account/$', 'account')
)
