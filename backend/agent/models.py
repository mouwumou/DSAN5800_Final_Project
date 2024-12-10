from django.db import models
from django.contrib.auth import get_user_model
import uuid


User = get_user_model()

# Create your models here.
class Tool(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    backend_function = models.CharField(max_length=100)
    prompt_template = models.CharField(max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta: 
        verbose_name_plural = "Tools"


# class Agent(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True, null=True)
#     base_prompt = models.CharField(max_length=500)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return self.name
    
#     class Meta: 
#         verbose_name_plural = "Agents"

class History(models.Model):
    # This is a history of the conversation between the user and the agent, the conversation is stored in the form of a list of dictionaries
    conversation = models.JSONField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=50, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    