from django.contrib import admin
from .models import Conversation, Messages, User
from django.contrib.auth.models import User 

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
    search_fields = ('name', 'email')


class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_user', 'date')

    def display_user(self, obj):
        return ', '.join([user.username for user in obj.user.all()])

    display_user.short_description = 'user'


class MessagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'conversation', 'text', 'date')
    search_fields = ('user__name', 'conversation__id')    



# admin.site.register(User, UserAdmin)
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Messages, MessagesAdmin)