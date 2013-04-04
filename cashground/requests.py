from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User,Group
from views import *

def getRequestName(request):
    raw = request.POST.keys()[0]
    data = json.loads(raw)
    return (data['name'], data)

def makeErrorResponse(query, error):
    return makeResponse({ 'error': error }, False, query)

@csrf_exempt
def ads_request(request):
    query = "JSON parsing failed"
    try:
        query, data = getRequestName(request)
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
    except Exception as e:
        return makeErrorResponse(query, e.message)

@csrf_exempt
def user_request(request):
    query = "JSON parsing failed"
    try:
        query, data = getRequestName(request)
        if query == 'createConsumable':
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
        return makeErrorResponse(query, e.message)

@csrf_exempt
def consumable_request(request):
    query = "JSON parsing failed"
    try:
        query, data = getRequestName(request)
        if query == 'loginUser':
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
