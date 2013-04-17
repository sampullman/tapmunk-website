from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson as json
from django.http import HttpResponse
from models import *
from requests import *

#AD_TYPES = [VIDEO_AD, APP_DOWNLOAD, MAKE_PURCHASE, FACEBOOK_LIKE, TWITTER_FOLLOW, WEB_AD];
AD_TYPES= [ [VIDEO_AD, "Video Ad"], [ANDROID_DOWNLOAD, "Android Download"], [IPHONE_DOWNLOAD, "iPhone Download"],
            [MAKE_PURCHASE, "Make Purchase"], [FACEBOOK_LIKE, "Facebook Like"],
            [TWITTER_FOLLOW, "Twitter Follow"], [GOOGLE_PLUS_ONE, "Google Plus One"], [WEB_AD, "Web Ad"] [SLIDESHOW, "Slideshow"] ];

def crsf_render(request, url, c={}):
    c.update(csrf(request))
    return render_to_response(url, c)

def cashground(request):
    return crsf_render(request, 'cashground.html');

def cashground_login(request):
    return crsf_render(request, 'login.html');

def admin_account(request, user):
    c = { "ads":getAdsDict('admin'), 'users':getUsersDict(), 'consumables':getConsumablesDict(), "ad_types":AD_TYPES }
    return crsf_render(request, 'admin.html', c)

def user_account(request, user):
    return crsf_render(request, 'user.html', {"user":user.get_profile().getDict()})

def advertiser_account(request, user):
    return crsf_render(request, 'advertiser.html', {"advertiser":user.getDict()})

def account(request):
    username = request.POST['username']
    password = request.POST['password']
    if request.POST['name'] == 'register':
        group = request.POST['group']
        email = request.POST['email']
        user = registerUser(username, password, email, group)
        return user_account(request, user)
    else:
        user = authenticate(username=username, password=password)
        if user is None:
            return HttpResponse('Error: Invalid credentials.')
        elif not user.is_active:
            return HttpResponse('Error: User is inactive.')
        login(request, user)
        groups = group = user.groups.all()
        if len(groups) > 0:
            group = groups[0]
            if group.name == 'User':
                return user_account(request, user)
            elif group.name == 'Advertiser':
                return advertiser_account(request, user)
            else:
                return HttpResponse('Unkown error occured.')
        else:
            return admin_account(request, user)
