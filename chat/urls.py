from django.urls import path, include
from .views import user_list, conversation_list, message_list, home, join_conversation, view_messages, conversation_not_found
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views
from .views import UserDetailAPI


router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'conversations', views.ConversationViewSet)
router.register(r'messages', views.MessagesViewSet)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', home, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('users/', user_list, name='user_list'),
    path('conversations/', conversation_list, name='conversation_list'),
    path('user/<int:user_id>/conversations/', conversation_list, name='conversation_list'),
    path('conversation/<int:conversation_id>/', message_list, name='message_list'),
    path('join/', join_conversation, name='join_conversation'),
    path('view_messages/<int:conversation_id>/', view_messages, name='view_messages'),
    path('conversation_not_found/', conversation_not_found, name='conversation_not_found'),
    path("get-details",UserDetailAPI.as_view()),
    #path('register',RegisterUserAPIView.as_view()),
    
]