from django.conf.urls import url

from . import views

app_name = 'copy_cat'
urlpatterns = [
    url(r'^$', views.chat_home, name='chat_home'),
    url(r'^select/$', views.select_bot, name='select'),
    url(r'^start/(?P<sn_id>[0-9]+)/(?P<bot_id>[0-9]+)/$', views.start_chat, name='start'),
    url(r'^chatroom/(?P<sn_id>[0-9]+)/(?P<bot_id>[0-9]+)/$', views.chatroom, name='chatroom')
]