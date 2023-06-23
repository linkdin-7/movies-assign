from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.



'''
Defining Collection Model
'''
class Collection(models.Model):
    title = models.CharField(max_length=225)
    description=models.TextField(max_length=500)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='collections')
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)

    def __str__(self):
        return self.title

'''
Defining Movies Model
'''
class Movie(models.Model):
    title = models.CharField(max_length=225)
    description = models.TextField()
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    genres = models.CharField(max_length=200)
    collection=models.ManyToManyField(Collection,related_name="movies")

    def __str__(self):
        return self.title


'''
Defining Model for keeping Count of Requests
'''
class RequestCount(models.Model):
    requestCount=models.PositiveIntegerField()
    
    def __str__(self):
        return self.requestCount