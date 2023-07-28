from django.db import models
import random
from django.conf import settings

User = settings.AUTH_USER_MODEL


class TweetLike(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    tweet = models.ForeignKey('Tweet' , on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

# Create your models here.
class Tweet(models.Model) :
    #id = models.AutoField(primary_key = true)
    user = models.ForeignKey(User , on_delete=models.CASCADE)  #many users  can have many tweets
    likes = models.ManyToManyField(User , related_name='tweet_user' , blank=True, through=TweetLike)
    #blank=true: its not required in django
    #null=true: its not required in the database
    content = models.TextField(blank=True , null=True)
    #a path to the image will be saved in the database. 
    image = models.FileField(upload_to='images/' , blank=True, null=True)  
    timestamp = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.content
    
    class Meta:
        ordering = ['-id']

    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'likes': random.randint(0,50)
        }