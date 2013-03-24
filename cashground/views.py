from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson as json
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User,Group
from models import *

VIDEO_AD = 20
ANDROID_DOWNLOAD = 21
IPHONE_DOWNLOAD = 22
MAKE_PURCHASE = 23
FACEBOOK_LIKE = 24
TWITTER_FOLLOW = 25
WEB_AD= 26

#AD_TYPES = [VIDEO_AD, APP_DOWNLOAD, MAKE_PURCHASE, FACEBOOK_LIKE, TWITTER_FOLLOW, WEB_AD];
AD_TYPES= [ [VIDEO_AD, "Video Ad"], [ANDROID_DOWNLOAD, "Android Download"], [IPHONE_DOWNLOAD, "iPhone Download"],
            [MAKE_PURCHASE, "Make Purchase"], [FACEBOOK_LIKE, "Facebook Like"],
            [TWITTER_FOLLOW, "Twitter Follow"], [WEB_AD, "Web Ad"] ];

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

@csrf_exempt
def request(request):
    raw = request.POST.keys()[0]
    query = raw
    try:
        request = json.loads(raw)
        query = request['name'];
        if(query == 'requestAds'):
            service = request['service']
            ads = getAdsDict(service)
            return makeResponse({'ads': ads }, name=query)
        elif query == 'createAd':
            quiz = request['quiz']
            ad = Ad(title=request['title'], ad_type=request['type'], uri=request['uri'], image=request['image'],
                    icon=request['icon'], value=request['value'], data="", campaign=Campaign.objects.all()[0])
            ad.save()
            createQuiz(ad, quiz)
            return makeResponse({ 'id':ad.id, 'timestamp':str(ad.timestamp) }, True, query)
        elif query == 'updateAd':
            ad = Ad.objects.get(id=request['id'])
            if ad:
                quiz = request['quiz']
                ad.update(request['title'], request['type'], request['icon'], request['value'], request['uri'], request['image'])
                ad.save()
                deleteQuiz(ad)
                createQuiz(ad, quiz)
                return makeResponse('', True, query)
            else:
                return makeResponse({'error':'User not in database.'}, False, query)
        elif query == 'deleteAd':
            adId = request['id'];
            Ad.objects.filter(id=adId).delete()
            return makeResponse(name=query);
        elif query == 'watchedAd':
            userId = request['userId']
            adId = request['adId']
            try:
                ad = Ad.objects.get(id=adId)
                user = User.objects.get(id=userId)
                userProf = UserProfile.objects.get(user=user)
                userProf.cash += ad.value
                userProf.save()
            except:
                return makeResponse({'error':'Could not update (invalid ad id or user).'}, False, query)
            return makeResponse({ 'cash': userProf.cash }, name=query)
        elif query == 'loginUser':
            username = request['username']
            password = request['password']
            service = request['service']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    if service == 'web':
                        login(request, user)
                    prof = UserProfile.objects.get(user=user)
                    return makeResponse(data={ 'id': user.id, 'cash': prof.cash }, name=query)
                else:
                    return makeResponse({ 'error': 'User is inactive.' }, False, query)
            else:
                return makeResponse({ 'error': 'Invalid username or password.' }, False, query)
        elif query == 'requestUsers':
            users = getUsersDict()
            return makeResponse({'users': users }, name=query)            
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
            registerUser(username, password, email, group)
            return makeResponse({'id':user.id}, name=query)
        elif query == 'deleteUser':
            id = request['id']
            User.objects.get(id=id).delete()
            return makeResponse('', True, query)
        elif query == 'createConsumable':
            icon = request['iconURI']
            title = request['title']
            cost = request['cost']
            item_type = request['type']
            cons = Consumable(title=title, icon=icon, cost=cost, item_type=item_type)
            cons.save()
            return makeResponse({'id':cons.id, 'timestamp':str(cons.timestamp) }, True, query)
        elif query == 'requestConsumables':
            return makeResponse({'consumables':getConsumablesDict()}, name=query)
        elif query == 'requestProducts':
            return makeResponse({'products':getProductsDict()}, name=query);
        elif query == 'requestCoupons':
            return makeResponse({'coupons':getCouponsDict()}, name=query);
        elif query == 'updateConsumable':
            consumable = Consumable.objects.get(id=request['id'])
            consumable.item_type = request['type']
            consumable.title = request['title']
            consumable.cost = request['cost']
            consumable.icon = request['iconURI']
            consumable.save()
            return makeResponse('', True, query)
        elif query == 'deleteConsumable':
            consumable = Consumable.objects.get(id=request['id']).delete()
            return makeResponse('', True, query)
    except Exception as e:
        error = e.message
        return makeResponse({ 'error': error }, False, query)

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

def getQuiz(ad):
    quizzes = AdQuiz.objects.filter(ad=ad)
    if len(quizzes) == 0:
        return ""
    else:
        quiz = quizzes[0]
    questions = AdQuizQuestion.objects.filter(quiz=quiz)
    questionList = []
    answerList = []
    for question in questions:
        questionList.append(question.question)
        answers = AdQuizAnswer.objects.filter(question=question)
        curAnswers = [answers.filter(correct=True)[0].answer]
        for answer in answers.filter(correct=False):
            curAnswers.append(answer.answer)
        answerList.append(curAnswers)
    return { "questions":questionList, "answers":answerList }

def createQuiz(ad, quizInfo):
    quiz = AdQuiz(ad=ad)
    quiz.save()
    questions = quizInfo['questions']
    answers = quizInfo['answers']
    for i in range(len(questions)):
        quest = AdQuizQuestion(quiz=quiz, question=questions[i])
        quest.save()
        curAnswers = answers[i]
        ans = AdQuizAnswer(question=quest, answer=curAnswers[0], correct=True)
        ans.save()
        for answer in curAnswers[1:]:
            ans = AdQuizAnswer(question=quest, answer=answer, correct=False)
            ans.save()

def deleteQuiz(ad):
    for quiz in AdQuiz.objects.filter(ad=ad):
        quiz.delete()

def registerUser(username, password, email, group):
    user = User.objects.create_user(username, email, password)
    user.groups.add(Group.objects.get(name=group))
    user.save()
    profile = UserProfile(ads_viewed=0, cash=0, user=user)
    profile.save()
    return user
