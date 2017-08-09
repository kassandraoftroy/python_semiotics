# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from .models import AI, SN, Message
from LinguistTools import Copy_Cat, Walk
from django.conf import settings
import random
import os

bot_dict = {}

def home(request):
	return render(request, 'copy_cat/home.html')

def index(request):
	return render(request, 'copy_cat/index.html')

def chat_home(request):
	return render(request, 'copy_cat/chat_home.html')

def analysis(request):
	return HttpResponse("In development... coming soon :)")

def select_bot(request):
	bots = AI.objects.all()
	new_username = request.POST['sn']
	new_user = SN()
	new_user.sn = new_username
	new_user.time = timezone.now()
	new_user.save()
	context = {"new_user":new_user, "bots":bots}
	return render(request, 'copy_cat/select.html', context)


def start_chat(request, sn_id, bot_id):
	user = SN.objects.get(pk=sn_id)
	bot = AI.objects.get(pk=bot_id)
	bot_dict[bot.name]=Copy_Cat(os.path.join(settings.BASE_DIR, bot.filename))
	context = {"user":user, "bot":bot}
	return render(request,'copy_cat/start.html', context)

def chatroom(request, sn_id, bot_id):
	user_input = request.POST['chat']
	user = SN.objects.get(pk=sn_id)
	user_message = Message()
	user_message.user = user
	user_message.text = user_input
	user_message.speaker = user.sn
	user_message.pub_date = timezone.now()
	user_message.save()
	bot = AI.objects.get(pk=bot_id)
	bot_input = bot_dict[bot.name].response(user_input)
	bot_message = Message()
	bot_message.user = user 
	bot_message.text = bot_input
	bot_message.speaker = bot.name
	bot_message.pub_date = timezone.now()
	bot_message.save()
	all_msgs = user.message_set.all()
	n = len(all_msgs)
	if n > 10:
		show_msgs = all_msgs[len(all_msgs) - 10: len(all_msgs)]
	else:
		show_msgs = all_msgs
	show_msgs = list(reversed(show_messages))
	context = {"user":user, "bot":bot, "show_msgs": show_msgs}
	return render(request, 'copy_cat/chatroom.html', context)

def walk_home(request):
	random_number = random.randint(1,150000)
	context = {"random_number":random_number}
	return render(request, 'copy_cat/walk_home.html', context)

def walk_result(request, r):
	try:
		input_text= request.POST['walk']
		if "," in input_text:
			input_text = input_text.replace(",", "")
		words=input_text.split()
		readout = Walk(words[0], words[1]).take_walk()
		all_paths = [readout[2][-i] for i in range (1, len(readout[2])+1)]
		context = {"rounds":readout[0],"volume":readout[1],"all_paths":all_paths,"example_path":readout[3],"midpoints":readout[4], "word_a":words[0], "word_b":words[1]}
		return render(request, 'copy_cat/walk_result.html', context)
	except:
		return render(request, 'copy_cat/walk_noresult.html')
