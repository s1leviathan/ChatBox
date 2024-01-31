from django.db import models
from django.contrib.auth.models import User
import openai
from django.conf import settings

# class User(models.Model):
#     class Meta:
#         verbose_name_plural = "users"
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)

#     def __str__(self):
#         return self.name

class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ManyToManyField(User)
    date = models.DateField(auto_now_add=True)

    def add_message_and_bot_response(self, text):
       
        bot_user, _ = User.objects.get_or_create(username='bot_user', defaults={'email': 'bot@example.com'})

        human_message = Messages.objects.create(user=self.user, conversation=self, text=text)
        human_message.save()

        bot_message = Messages.objects.create(user=bot_user, conversation=self, text=human_message.get_openai_response())
        bot_message.save()


    def __str__(self):
        return f"Conversation {self.id}"
    

class Messages(models.Model):
    class Meta:
        verbose_name_plural = "messages"
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def get_openai_response(self):
        openai.api_key = settings.OPENAI_API_KEY

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": self.text},
                ]
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error: {e}")
            return "Sorry, I couldn't process your request."  

    def __str__(self):
        return f"Message {self.id} by {self.user.username} in Conversation {self.conversation.id}"
    


  
