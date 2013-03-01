from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson as json
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User,Group
from models import *

VIDEO_AD = 20;
APP_DOWNLOAD = 21;
MAKE_PURCHASE = 22;
FACEBOOK_LIKE = 23;
TWITTER_FOLLOW = 24;
WEB_AD= 25;

#AD_TYPES = [VIDEO_AD, APP_DOWNLOAD, MAKE_PURCHASE, FACEBOOK_LIKE, TWITTER_FOLLOW, WEB_AD];
AD_TYPES= [ [VIDEO_AD, "Video Ad"], [APP_DOWNLOAD, "App Download"],
            [MAKE_PURCHASE, "Make Purchase"], [FACEBOOK_LIKE, "Facebook Like"],
            [TWITTER_FOLLOW, "Twitter Follow"], [WEB_AD, "Web Ad"] ];

def crsf_render(request, url, c={}):
    c.update(csrf(request))
    return render_to_response(url, c)

def cashground(request):
    return crsf_render(request, 'cashground.html');

def cashground_login(request):
    return crsf_render(request, 'login.html');

def admin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            c = { "ads":getAdsDict(), 'users':getUsersDict(), "ad_types":AD_TYPES }
            return crsf_render(request, 'admin.html', c)
        else:
            return HttpResponse('Error: User is inactive.')
    else:
        return HttpResponse('Error: Invalid credentials.')

def makeResponse(data='', success=True, name=''):
    return HttpResponse(json.dumps({'success':success, 'request_name':name,
                                    'data': data}))

@csrf_exempt
def request(request):
    raw = request.POST.keys()[0]
    query = raw
    try:
        request = json.loads(raw)
        query = request['name'];
        if(query == 'requestAds'):
            ads = getAdsDict()
            return makeResponse({'ads': ads }, name=query)
        elif query == 'createAd':
            ad = Ad(title=request['title'], ad_type=request['type'],
                    image=request['icon'], value=request['value'], data="", campaign=Campaign.objects.all()[0])
            ad.save()
            return makeResponse({ 'id':ad.id, 'timestamp':str(ad.timestamp) }, True, query)
        elif query == 'updateAd':
            ad = Ad.objects.get(id=request['id'])
            if ad:
                ad.update(request['title'], request['type'], request['icon'], request['value'])
                ad.save()
                return makeResponse('', True, query)
            else:
                return makeResponse({'error':'User not in database.'}, False, query)
        elif query == 'deleteAd':
            adId = request['id'];
            Ad.objects.filter(id=adId).delete()
            return makeResponse(name=query);
        elif query == 'loginUser':
            username = request['username']
            password = request['password']
            service = request['service']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    if service == 'web':
                        login(request, user)
                    return makeResponse(data={ 'id': user.id }, name=query)
                else:
                    return makeResponse({ 'error': 'User is inactive.' }, False, query)
            else:
                return makeResponse({ 'error': 'Invalid username or password.' }, False, query)
        elif query == 'updateUser':
            user = User.objects.get(id=request['id'])
            user.username = request['username']
            user.save()
            return makeResponse('', True, query)
        elif query == 'registerUser':
            username = request['username']
            password = request['password']
            email = request['email']
            group = request['group']
            user = User.objects.create_user(username, email, password)
            user.groups.add(Group.objects.get(name=group))
            user.save()
            profile = UserProfile(ads_viewed=0, cash=0, user=user)
            profile.save()
            return makeResponse({'id':user.id}, name=query)
        elif query == 'deleteUser':
            id = request['id']
            User.objects.get(id=id).delete()
            return makeResponse('', True, query)            
    except Exception as e:
        error = e.message
        return makeResponse({ 'error': error }, False, query)

def getAdsDict():
    ads = []
    for ad in Ad.objects.all():
        ads.append(ad.getDict())
    return ads

def getUsersDict():
    users = []
    for user in UserProfile.objects.all():
        users.append(user.getDict())
    return users
