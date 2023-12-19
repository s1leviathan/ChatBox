from django.contrib import admin
from .models import Users, Conversation, Messages

class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
    search_fields = ('name', 'email')


class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_users', 'date')

    def display_users(self, obj):
        return ', '.join([user.name for user in obj.users.all()])

    display_users.short_description = 'Users'


class MessagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'conversation', 'text', 'date')
    search_fields = ('user__name', 'conversation__id')    



admin.site.register(Users, UsersAdmin)
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Messages, MessagesAdmin)