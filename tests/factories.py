from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from movielist.models import Collection,Movie
import factory
'''
Register Factory
'''
class RegisterFactory(DjangoModelFactory):
    class Meta:
        model = User
    username = "New2"
    password = "Tech@1234"


'''
Collection Factory
'''
class CollectionFactory(DjangoModelFactory):
    class Meta:
        model = Collection
    title = "New Collection"
    description ="Creating a Collection"
    
'''
Movie Factory
'''
class MovieFactory(DjangoModelFactory):
    class Meta:
        model = Movie
    
    title = "Swing"
    description ="New Movie"
    genres = "Action,Thriller"
    collection = factory.SubFactory(CollectionFactory)