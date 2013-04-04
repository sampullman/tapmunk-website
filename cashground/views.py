from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson as json
from django.http import HttpResponse
from models import *
from requests import *

VIDEO_AD = 20
WEB_AD = 21
ANDROID_DOWNLOAD = 22
IPHONE_DOWNLOAD = 23
MAKE_PURCHASE = 24
FACEBOOK_LIKE = 25
TWITTER_FOLLOW = 26
GOOGLE_PLUS_ONE = 27

#AD_TYPES = [VIDEO_AD, APP_DOWNLOAD, MAKE_PURCHASE, FACEBOOK_LIKE, TWITTER_FOLLOW, WEB_AD];
AD_TYPES= [ [VIDEO_AD, "Video Ad"], [ANDROID_DOWNLOAD, "Android Download"], [IPHONE_DOWNLOAD, "iPhone Download"],
            [MAKE_PURCHASE, "Make Purchase"], [FACEBOOK_LIKE, "Facebook Like"],
            [TWITTER_FOLLOW, "Twitter Follow"], [GOOGLE_PLUS_ONE, "Google Plus One"], [WEB_AD, "Web Ad"] ];

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
    
    

def makeResponse(data='', success=True, name=''):
    return HttpResponse(json.dumps({'success':success, 'request_name':name,
                                    'data': data}))

def getServiceFilter(service):
    if service == 'iphone':
        return ANDROID_DOWNLOAD
    elif service == 'admin':
        return -1
    else:
        return IPHONE_DOWNLOAD

def getAdsDict(service):
    ads = []
    for ad in Ad.objects.exclude(ad_type=getServiceFilter(service)):
        dic = ad.getDict()
        dic['quiz'] = getQuiz(ad)
        ads.append(dic)
    return ads

def getUsersDict():
    users = []
    for user in UserProfile.objects.all():
        users.append(user.getDict())
    return users

def getConsumablesDict():
    consumables = []
    for cons in Consumable.objects.all():
        consumables.append(cons.getDict())
    return consumables

def getProductsDict():
    products = []
    for product in Consumable.objects.filter(item_type='Product'):
        products.append(product.getDict())
    return products

def getCouponsDict():
    coupons = []
    for coupon in Consumable.objects.filter(item_type='Coupon'):
        coupons.append(coupon.getDict())
    return coupons

def registerUser(username, password, email, group):
    user = User.objects.create_user(username, email, password)
    user.groups.add(Group.objects.get(name=group))
    user.save()
    profile = UserProfile(ads_viewed=0, cash=0, user=user)
    profile.save()
    return user
