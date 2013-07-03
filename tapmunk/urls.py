from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'tapmunk.views',
    url(r'^$', 'tapmunk'),
    #url(r'^account/$', 'account'),
    #url(r'^signup/$', 'signup'),
    #url(r'^signup/admin$', 'signup_admin'),
    #url(r'^admin_temp$', 'admin_temp'),
)
