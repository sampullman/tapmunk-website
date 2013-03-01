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
    name = models.CharField(max_length=30)

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
    image = models.URLField()
    data = models.CharField(max_length=300)
    campaign = models.ForeignKey(Campaign)
    value = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.timestamp = timezone.now()
        super(Ad, self).save(*args, **kwargs)

    def getDict(self):
        return { 'title':self.title, 'type':self.ad_type,
                 'data':"", 'icon':self.image, 'value':self.value,
                 'timestamp':str(self.timestamp), 'id':self.id} 

    def update(self, title, ad_type, icon, value):
        self.title = title
        self.ad_type = ad_type
        self.image = icon
        self.value = value

class ViewedAd(models.Model):
    user = models.ForeignKey(User)
    ad = models.OneToOneField(Ad)
    timestamp = models.DateTimeField('date published')
