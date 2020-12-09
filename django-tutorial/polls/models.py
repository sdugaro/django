import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    question_pdf = models.FileField(upload_to='pdf', default='',
                                    null=True, blank=True)
    question_img = models.ImageField(upload_to='img', default='/img/me.jpg',
                                     null=True, blank=True)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        # fails test
        #return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

        now = timezone.now()
        return now - datetime.timedelta(days=1) < self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
