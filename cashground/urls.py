from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'cashground.views',
    url(r'^$', 'cashground'),
    url(r'^request/ads$', 'ads_request'),
    url(r'^request/user$', 'user_request'),
    url(r'^request/consumables$', 'consumables_request'),
    url(r'^account/$', 'account'),
)
