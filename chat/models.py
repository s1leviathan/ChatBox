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

    def __str__(self):
        return f"Conversation {self.id}"
    
    def get_openai_response(prompt):
        openai.api_key = settings.OPENAI_API_KEY

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ]
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error: {e}")
            return "Sorry, I couldn't process your request."

class Messages(models.Model):
    class Meta:
        verbose_name_plural = "messages"
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} by {self.user.username} in Conversation {self.conversation.id}"    