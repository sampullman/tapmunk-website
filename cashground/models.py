from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class UserProfile(models.Model):
    ads_viewed = models.IntegerField()
    cash = models.IntegerField()
    user = models.ForeignKey(User, unique=True)

    def getDict(self):
        return {'name':self.user.username, 'timestamp':str(self.user.date_joined),
                'cash':self.cash, 'ads_viewed':self.ads_viewed, 'id':self.user.id}

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
    title = models.CharField(max_length=20)
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
        return { 'title':self.title, 'type':self.ad_type, 'uri':self.uri,
                 'data':"", 'icon':self.icon, 'value':self.value,
                 'timestamp':str(self.timestamp), 'id':self.id, 'image':self.image} 

    def update(self, title, ad_type, icon, value, uri, image):
        self.title = title
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

class ViewedAd(models.Model):
    user = models.ForeignKey(User)
    ad = models.OneToOneField(Ad)
    timestamp = models.DateTimeField('date published')

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

    
