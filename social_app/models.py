from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=15) 
    bio = models.CharField(max_length=100, blank=True) 
    email = models.EmailField(max_length=50)
    date_of_birth = models.DateField()
    about = models.CharField(max_length=50, blank=True)  
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    created_at =models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user.username
     
class Message(models.Model):
    from_user =models.OneToOneField(User,related_name="sender",on_delete=models.CASCADE)
    to_user = models.OneToOneField(User,related_name="reciever",on_delete=models.CASCADE)
    message_text =models.CharField(max_length=100)