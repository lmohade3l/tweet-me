from django.db import models

# Create your models here.
class Tweet(models.Model) :
    #id = models.AutoField(primary_key = true)
    #blank=true: its not required in django
    #null=true: its not required in the database
    content = models.TextField(blank=True , null=True)
    #a path to the image will be saved in the database. 
    image = models.FileField(upload_to='images/' , blank=True, null=True)  