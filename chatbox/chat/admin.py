from django.contrib import admin
from .models import Users, Conversation, Messages

class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
    search_fields = ('name', 'email')
