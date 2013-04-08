from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User,Group
from django.core.mail import send_mail
from views import *

VIDEO_AD = 20
WEB_AD = 21
ANDROID_DOWNLOAD = 22
IPHONE_DOWNLOAD = 23
MAKE_PURCHASE = 24
FACEBOOK_LIKE = 25
TWITTER_FOLLOW = 26
GOOGLE_PLUS_ONE = 27

def getRequestName(request):
    raw = request.POST.keys()[0]
    data = json.loads(raw)
    return (data['name'], data)

def makeResponse(data='', success=True, name=''):
    return HttpResponse(json.dumps({'success':success, 'request_name':name,
                                    'data': data}))

def makeErrorResponse(query, error):
    return makeResponse({ 'error': error }, False, query)

@csrf_exempt
def general_request(request):
    try:
        query, data = getRequestName(request)
        if query == 'contactEmail':
            text = data['text']
            sender = data['sender']
            send_mail('Site Contact', text, sender, ('casheggshared@gmail.com',), fail_silently=False)
            return makeResponse(name='contactEmail')
    except Exception as e:
        return makeErrorResponse(query, e.message)

@csrf_exempt
def ads_request(request):
    query = "JSON parsing failed"
    try:
        query, data = getRequestName(request)
        if(query == 'requestAds'):
            service = data['service']
            ads = getAdsDict(service)
            return makeResponse({'ads': ads }, name=query)
        elif query == 'createAd':
            quiz = data['quiz']
            ad = Ad(title=data['title'], ad_type=data['type'], uri=data['uri'], image=data['image'],
                    icon=data['icon'], value=data['value'], data="", campaign=Campaign.objects.all()[0])
            ad.save()
            createQuiz(ad, quiz)
            return makeResponse({ 'id':ad.id, 'timestamp':str(ad.timestamp) }, True, query)
        elif query == 'updateAd':
            ad = Ad.objects.get(id=data['id'])
            if ad:
                quiz = data['quiz']
                ad.update(data['title'], data['type'], data['icon'], data['value'], data['uri'], data['image'])
                ad.save()
                deleteQuiz(ad)
                createQuiz(ad, quiz)
                return makeResponse('', True, query)
            else:
                return makeResponse({'error':'User not in database.'}, False, query)
        elif query == 'deleteAd':
            adId = data['id'];
            Ad.objects.filter(id=adId).delete()
            return makeResponse(name=query);
        elif query == 'watchedAd':
            userId = data['userId']
            adId = data['adId']
            try:
                ad = Ad.objects.get(id=adId)
                user = User.objects.get(id=userId)
                userProf = UserProfile.objects.get(user=user)
                userProf.cash += ad.value
                userProf.save()
            except:
                return makeResponse({'error':'Could not update (invalid ad id or user).'}, False, query)
            return makeResponse({ 'cash': userProf.cash }, name=query)
    except Exception as e:
        return makeErrorResponse(query, e.message)

@csrf_exempt
def consumables_request(request):
    query = "JSON parsing failed"
    try:
        query, data = getRequestName(request)
        if query == 'createConsumable':
            icon = data['iconURI']
            title = data['title']
            cost = data['cost']
            item_type = data['type']
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
            consumable = Consumable.objects.get(id=data['id'])
            consumable.item_type = data['type']
            consumable.title = data['title']
            consumable.cost = data['cost']
            consumable.icon = data['iconURI']
            consumable.save()
            return makeResponse('', True, query)
        elif query == 'deleteConsumable':
            consumable = Consumable.objects.get(id=data['id']).delete()
            return makeResponse('', True, query)
    except Exception as e:
        return makeErrorResponse(query, e.message)

@csrf_exempt
def user_request(request):
    query = "JSON parsing failed"
    try:
        query, data = getRequestName(request)
        if query == 'loginUser':
            username = data['username']
            password = data['password']
            service = data['service']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    if service == 'web':
                        login(data, user)
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
            user = User.objects.get(id=data['id'])
            user.username = data['username']
            user.save()
            return makeResponse('', True, query)
        elif query == 'registerUser':
            username = data['username']
            password = data['password']
            email = data['email']
            group = data['group']
            registerUser(username, password, email, group)
            return makeResponse({'id':user.id}, name=query)
        elif query == 'deleteUser':
            id = data['id']
            User.objects.get(id=id).delete()
            return makeResponse('', True, query)
    except Exception as e:
        return makeErrorResponse(query, e.message)

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
