from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User,related_name="personal_user" , on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='media/images/', default='media\images\default.png')
    username = models.CharField(max_length=15) 
    email = models.EmailField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    following = models.ManyToManyField(User ,related_name="following", blank=True, default= User.objects.none())
    followers = models.ManyToManyField(User ,related_name="followers", blank=True, default= User.objects.none())
    bio = models.CharField(max_length=100, blank=True) 
    about = models.CharField(max_length=50, blank=True)  
    created_at =models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username
    
class Message(models.Model):
    from_user =models.ForeignKey(User,related_name="sender",on_delete=models.CASCADE)
    to_user = models.ForeignKey(User,related_name="reciever",on_delete=models.CASCADE)
    message_text =models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)

class ImagePost(models.Model):
    user = models.ForeignKey(User,related_name="image_post_user",on_delete=models.CASCADE)
    post_picture = models.ImageField(upload_to='images/posts', default='images/images.png')
    post_description = models.CharField(max_length=60)
    hashtag = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User,related_name="image_liked_by",blank=True,default=User.objects.none())
    
    def __str__(self):
        return (self.post_description) +" -- "+ (self.user.username)
    
class TextPost(models.Model):
    user = models.ForeignKey(User,related_name="text_post_user",on_delete=models.CASCADE)
    post_description = models.CharField(max_length=60)
    hashtag = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User,related_name="text_liked_by",blank=True,default=User.objects.none())
    
    def __str__(self):
        return (self.post_description) +" -- "+ (self.user.username)