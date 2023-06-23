from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Movie,Collection
from drf_writable_nested.serializers import WritableNestedModelSerializer


'''
Serializer for Movie
'''
class MovieSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Movie
        fields = ['title','description','genres','uuid']


'''
Serializer for Collection Using WritableNestedModelSerializer Library
'''
class CollectionSerializer(WritableNestedModelSerializer):
    movies=MovieSerializer(many=True)
    class Meta:
        model = Collection
        fields = ['title','uuid','description','movies']
        
        read_only_fields = ['uuid'] 
