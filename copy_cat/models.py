# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class AI(models.Model):
	name = models.CharField(max_length=100)
	filename = models.CharField(max_length=100)
	style = models.CharField(max_length=250)

class SN(models.Model):
	sn = models.CharField(max_length=100)
	time = models.DateTimeField('date published')

class Message(models.Model):
	user = models.ForeignKey(SN, on_delete=models.CASCADE)
	text = models.CharField(max_length=500)
	speaker = models.CharField(max_length=100)
	pub_date = models.DateTimeField('date published')


