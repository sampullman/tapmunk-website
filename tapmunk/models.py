from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class UserProfile(models.Model):
    ads_viewed = models.IntegerField()
    cash = models.IntegerField()
    user = models.ForeignKey(User)
    email = models.CharField(max_length=80, unique=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    device_id = models.CharField(max_length=30)

    def getDict(self):
        return {'name':self.user.username, 'timestamp':str(self.user.date_joined),
                'cash':self.cash, 'ads_viewed':self.ads_viewed, 'id':self.user.id,
                'age':self.age, 'gender':self.gender, 'device_id':self.device_id }
                
class PreSignupProfile(models.Model):
    username = models.CharField(max_length=20, unique=True)
    email = models.CharField(max_length=30, unique=True)
    notes = models.CharField(max_length=500)
    timestamp = models.DateTimeField('date published')
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.timestamp = timezone.now()
        super(PreSignupProfile, self).save(*args, **kwargs)
        
    def getDict(self):
        return {'username':self.username, 'email':self.email, 'notes':self.notes,
                 'timestamp':str(self.timestamp) }

class Advertiser(models.Model):
    timestamp = models.DateTimeField('date published')

    def save(self, *args, **kwargs):
        if not self.id:
            self.timestamp = timezone.now()
        super(Advertiser, self).save(*args, **kwargs)

class Campaign(models.Model):
    timestamp = models.DateTimeField('date published')
    impressions = models.IntegerField()
    advertiser = models.ForeignKey(Advertiser)
    platform = models.CharField(max_length=10)

    def save(self, *args, **kwargs):
        if not self.id:
            self.timestamp = timezone.now()
        super(Campaign, self).save(*args, **kwargs)

class Ad(models.Model):
    company = models.CharField(max_length=20)
    title = models.CharField(max_length=30)
    blurb = models.CharField(max_length=60)
    timestamp = models.DateTimeField('date published')
    ad_type = models.IntegerField()
    icon = models.URLField()
    uri = models.CharField(max_length=40)
    data = models.CharField(max_length=300)
    campaign = models.ForeignKey(Campaign)
    value = models.IntegerField()
    image = models.CharField(max_length=40)

    def save(self, *args, **kwargs):
        if not self.id:
            self.timestamp = timezone.now()
        super(Ad, self).save(*args, **kwargs)

    def getDict(self):
        return { 'company':self.company, 'title':self.title, 'blurb':self.blurb,
                 'type':self.ad_type, 'uri':self.uri,
                 'data':"", 'icon':self.icon, 'value':self.value,
                 'timestamp':str(self.timestamp), 'id':self.id, 'image':self.image} 

    def update(self, company, title, blurb, ad_type, icon, value, uri, image):
        self.company = company
        self.title = title
        self.blurb = blurb
        self.ad_type = ad_type
        self.icon = icon
        self.value = value
        self.uri = uri
        self.image = image

class AdQuiz(models.Model):
    ad = models.ForeignKey(Ad)

class AdQuizQuestion(models.Model):
    question = models.CharField(max_length=50)
    quiz = models.ForeignKey(AdQuiz)

class AdQuizAnswer(models.Model):
    correct = models.BooleanField(default=False)
    answer = models.CharField(max_length=20)
    question = models.ForeignKey(AdQuizQuestion)

class AdQuizResult(models.Model):
    timestamp = models.DateTimeField('date published')
    question = models.ForeignKey(AdQuizQuestion)
    answer = models.ForeignKey(AdQuizAnswer)
    user = models.ForeignKey(User)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.timestamp = timezone.now()
        super(AdQuizResult, self).save(*args, **kwargs)

class ViewedAd(models.Model):
    user = models.ForeignKey(UserProfile)
    ad = models.ForeignKey(Ad)
    timestamp = models.DateTimeField('date published')

    def save(self, *args, **kwargs):
        if not self.id:
            self.timestamp = timezone.now()
        super(ViewedAd, self).save(*args, **kwargs)

ConsumableTypes = ['Product', 'Coupon']
class Consumable(models.Model):
    timestamp = models.DateTimeField('date published')
    icon = models.URLField()
    title = models.CharField(max_length=20)
    cost = models.IntegerField()
    item_type = models.CharField(max_length=14)

    def getDict(self):
        return { 'timestamp':str(self.timestamp), 'iconURI':self.icon, 'title':self.title,
                 'cost':self.cost, 'type':self.item_type, 'id':self.id }

    def save(self, *args, **kwargs):
        if not self.id:
            self.timestamp = timezone.now()
        super(Consumable, self).save(*args, **kwargs)

    
