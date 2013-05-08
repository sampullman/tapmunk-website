from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User,Group
from django.template.loader import render_to_string
from django.core.mail import send_mail
from views import *
from constants import *
import re

def crsf_render(request, url, c={}):
    c.update(csrf(request))
    return render_to_response(url, c)

def getRequestName(request):
    raw = request.POST.keys()[0]
    data = json.loads(raw)
    return (data['name'], data)

def makeResponse(data='', response=SUCCESS, name=''):
    return HttpResponse(json.dumps({'response':response, 'request_name':name,
                                    'data': data}))

def makeErrorResponse(query, error, response=INVALID_DATA):
    return makeResponse({ 'error': error }, response, query)

@csrf_exempt
def general_request(request):
    try:
        query, data = getRequestName(request)
        if query == 'contactEmail':
            text = data['text']
            sender = data['sender']
            send_mail('Site Contact', text, sender, ('casheggshared@gmail.com',), fail_silently=False)
            return makeResponse(name='contactEmail')
        elif query == 'requestPreSignups':
            profiles = getPresignupProfiles()
            return makeResponse({'profiles': profiles}, name=query)
        elif query == 'createPreSignup':
            error = False
            username = data['username']
            email = data['email']
            if len(username) < 3 or len(username) >= 20:
                error = "Username must be more than 2 and less than 20 characters."
            elif not re.match(r'[a-zA-Z0-9_-]+', username):
                error = "Username can only contain: a-z A-Z 0-9 - _"
            elif not re.match(r'.+@.+\..+', email):
                error = "Please enter a valid email"
                
            if error:
                return makeErrorResponse(query, error)
            else:
                profile = PreSignupProfile(username=username, email=email, notes="")
                profile.save()
                return makeResponse(name=query)
        elif query == 'savePreSignup':
            username = data['username']
            notes = data['notes']
            profile = PreSignupProfile.objects.get(username=username)
            profile.notes = notes
            profile.save()
            return makeResponse(name=query)
        elif query == 'deletePreSignup':
            username = data['username']
            PreSignupProfile.objects.get(username=username).delete()
            return makeResponse(name=query)
        elif query == 'requestProfilesTable':
            c = { 'profiles':getPreSignupProfiles() }
            return makeResponse(render_to_string('signup_admin_table.html', c))
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
            return makeResponse({ 'id':ad.id, 'timestamp':str(ad.timestamp) }, name=query)
        elif query == 'updateAd':
            try:
                ad = Ad.objects.get(id=data['id'])
            except Exception as e:
                ad = None
            quiz = data['quiz']
            if ad:
                ad.update(data['company'], data['title'], data['blurb'], data['type'], data['icon'],
                          data['value'], data['uri'], data['image'])
                ad.save()
                deleteQuiz(ad)
                createQuiz(ad, quiz)
                return makeResponse('', name=query)
            else:
                ad = Ad(company=data['company'], title=data['title'], blurb=data['blurb'],
                        ad_type=data['type'], uri=data['uri'], image=data['image'],
                        icon=data['icon'], value=data['value'], data="", campaign=Campaign.objects.all()[0])
                ad.save()
                createQuiz(ad, quiz)
                return makeResponse({ 'id':ad.id, 'timestamp':str(ad.timestamp) }, name=query)
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
                quizData = data['quiz']
                if quizData and quizData != "":
                    reportQuizResult(user, quizData)
            except Exception as e:
                return makeErrorResponse(query, 'Could record watched ad: '+e.message)
            return makeResponse({ 'cash': userProf.cash, 'value': ad.value }, name=query)
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
            return makeResponse({'id':cons.id, 'timestamp':str(cons.timestamp) }, name=query)
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
            return makeResponse('', name=query)
        elif query == 'deleteConsumable':
            consumable = Consumable.objects.get(id=data['id']).delete()
            return makeResponse('', name=query)
    except Exception as e:
        return makeErrorResponse(query, e.message)

@csrf_exempt
def user_request(request):
    query = "JSON parsing failed"
    try:
        query, data = getRequestName(request)
        if query == 'loginUser':
            username = getUsernameFromEmail(data['email'])
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
                    return makeErrorResponse(query, 'User is inactive.')
            else:
                return makeErrorResponse(query, 'Invalid username or password.')
        elif query == 'requestUsers':
            users = getUsersDict()
            return makeResponse({'users': users }, name=query)            
        elif query == 'updateUser':
            user = User.objects.get(id=data['id'])
            user.username = data['username']
            user.save()
            return makeResponse('', name=query)
        elif query == 'registerUser':
            password = data['password']
            email = data['email']
            group = data['group']
            age = data['age']
            gender = data['gender'].lower()
            deviceId = data['device_id']
            user, prof = registerUser(email, password, deviceId, age, gender, group)
            return makeResponse({ 'id': user.id, 'cash': prof.cash }, name=query)
        elif query == 'deleteUser':
            id = data['id']
            User.objects.get(id=id).delete()
            return makeResponse('', name=query)
    except Exception as e:
        return makeErrorResponse(query, e.message)

def reportQuizResult(user, quizResultObj):
    try:
        quiz = AdQuiz.objects.get(id=quizResultObj['id'])
        questions = quizResultObj['questions']
        answers = quizResultObj['answers']
        for question, answer in zip(questions, answers):
            if question and answer and question != "" and answer != "":
                questionObj = AdQuizQuestion.objects.get(quiz=quiz, question=question)
                answerObj = AdQuizAnswer.objects.get(question=questionObj, answer=answer)
                result = AdQuizResult(question=questionObj, answer=answerObj, user=user)
                result.save()
        return True
    except Exception as e:
        raise e
        

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
    return { "id":quiz.id, "questions":questionList, "answers":answerList }

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
    for ad in Ad.objects.exclude(ad_type=getServiceFilter(service))[::-1]:
        dic = ad.getDict()
        dic['quiz'] = getQuiz(ad)
        ads.append(dic)
    return ads

def getUsersDict():
    users = []
    for user in UserProfile.objects.all():
        users.append(user.getDict())
    return users
    
def getPreSignupProfiles():
    profiles = []
    for profile in PreSignupProfile.objects.all().order_by('-timestamp'):
        profiles.append(profile.getDict())
    return profiles

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
    
def getUsernameFromEmail(email):
    return email[:30]

def registerUser(email, password, deviceId, age, gender, group):
    username = getUsernameFromEmail(email)
    user = User.objects.create_user(username, email, password)
    user.groups.add(Group.objects.get(name=group))
    user.save()
    profile = UserProfile(ads_viewed=0, cash=0, email=email, age=age, gender=gender, user=user, device_id=deviceId)
    profile.save()
    return user, profile
