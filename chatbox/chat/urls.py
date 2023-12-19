from django.urls import path
from .views import user_list, conversation_list, message_list, home

urlpatterns = [
    path('', home, name='home'),
    path('users/', user_list, name='user_list'),
    path('conversations/', conversation_list, name='conversation_list'),
    path('conversation/<int:conversation_id>/', message_list, name='message_list'),
]