"""
URL configuration for chatbox project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from chat.views import ConversationViewSet, MessagesViewSet, UserViewSet 
from rest_framework import routers
from chat.views import LogoutAPIView
from rest_framework.authtoken import views




router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessagesViewSet, basename='message')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/v1/', include('dj_rest_auth.urls')),
    path('api/v1/registration/', include('dj_rest_auth.registration.urls')),
    path('api-token-auth', views.obtain_auth_token),
    path('api/auth/logout/', LogoutAPIView.as_view(), name='logout'), 
    path('chat/', include('chat.urls')),
    

    
]
