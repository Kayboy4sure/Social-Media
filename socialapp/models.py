from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Profile(models.Model):
    Gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )
    Marital_status = (
        ('Single','Single'),
        ('In Relationship','In Relationship'),
        ('Divorce','Divorce'),
        ('Widow','Widow'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    dateofbirth = models.DateField(blank=True, null=True)
    gender = models.CharField(choices=Gender_list, blank=True, max_length=10)
    marital = models.CharField(choices=Marital_status, blank=True, max_length=20)
    profilepic = models.ImageField(upload_to='profile_pictures/', default='blank-profile-picture.png')
    wallpaper = models.ImageField(upload_to='profile_wallpapers/', default='blank-profile-picture.png')

    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.user.username

class LikePost(models.Model):
    username = models.CharField(max_length=50)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.username

class FollowersCount(models.Model):
    following = models.CharField(max_length=50)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.following