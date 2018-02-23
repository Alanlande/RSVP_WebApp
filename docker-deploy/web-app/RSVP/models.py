from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.forms import ModelForm

# Create your models here.
class Event(models.Model):
    event_name = models.CharField(max_length=200)
    event_date = models.DateField()
    event_location = models.CharField(max_length=200)
    canPlusOne = models.BooleanField(default= False) # danger log
    def __str__(self):
        return self.event_name + '---' + self.event_date.__str__()+'---'+self.event_location

class Role(models.Model):
    Role_Choices = {
    ('vendor', 'vendor'),
    ('owner', 'owner'),
    ('guest', 'guest'),
    }
    event = models.ForeignKey(Event, on_delete = models.CASCADE)
    users = models.ManyToManyField(User)
    roleType = models.CharField(
        max_length = 100,
        choices = Role_Choices,
    )
    status = models.CharField(max_length = 100, default='pending') #accept, deny, pending
    def __str__(self):
        return self.roleType + '---' + self.event.event_name + '---' + self.status
    class Meta:
      ordering = ('roleType',)

class Question(models.Model):
    Question_Choices = {
    ('Free', 'Free Text Question'),
    ('Multi', 'Multiple Choice Question'),
    }
    question_text = models.CharField(max_length=200)
    event = models.ForeignKey(Event, on_delete = models.CASCADE)
    question_type = models.CharField(   #不选会怎么样？
        max_length = 100,
        choices = Question_Choices,
    )
    vendor_permission = models.BooleanField(default=True) # can vandor see
    finalization = models.BooleanField(default=False)
    def __str__(self):
        return self.question_text + '---' + self.question_type + '---' + self.vendor_permission.__str__()
    class Meta:
      ordering = ('question_text',)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
    class Meta:
      ordering = ('choice_text',)

class Response(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete = models.CASCADE)
    def __str__(self):
        return self.user.username + '---' + self.question.__str__() + '---' + self.choice.__str__()
