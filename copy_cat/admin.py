# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import AI, Message, SN

admin.site.register(AI)
admin.site.register(SN)
admin.site.register(Message)