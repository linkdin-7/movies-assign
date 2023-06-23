# All imports 
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import CollectionSerializer
from .models import Collection,RequestCount,Movie
from requests.auth import HTTPBasicAuth
from rest_framework import status
import environ 
import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from requests.adapters import HTTPAdapter,Retry
from django.http import JsonResponse,HttpResponse,Http404
from rest_framework.generics import ListAPIView

# Initialize environment
env = environ.Env()
environ.Env.read_env()

# Default timeout 
DEFAULT_TIMEOUT = 5 # seconds

# Setting timeout for requests
class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


# Combining timeout with retries for Third Party API
http = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500])
http.mount("https://", TimeoutHTTPAdapter(max_retries=retries))
http.mount("http://", TimeoutHTTPAdapter(max_retries=retries))


# Create your views here.

class MovieList(APIView):
    '''
    Creating a MovieList Class From Third Party API (List Of Movies)
    List all Movies
    '''
    
    # Authentication Of User With JWT Token 
    permission_classes=(IsAuthenticated,)
    authentication_classes= [JWTAuthentication]

    def get_movies(self,page=None):
        # Getting The Username and Passowrd From .env File 
        username=env('UsernameAPI')
        password=env('PasswordAPI')
        if page:
            url = 'https://demo.credy.in/api/v1/maya/movies/'+'?page='+page
        else:
            url = 'https://demo.credy.in/api/v1/maya/movies/'
        response = http.get(url,auth = HTTPBasicAuth(username,password),timeout=1)
        return response

    def get(self,request):
        
        page=request.GET.get('page')
        response=self.get_movies(page=page)
        data=response.json()
        if data.get('error'):
            return Response(data,status=response.status_code)
        '''
        Replacing The Current Third Party Url of Next & Prev Pages with localhost Url

        '''
        if data.get("next"):
            data["next"]=data['next'].replace('https://demo.credy.in/api/v1/maya','http://127.0.0.1:8000')

        if data.get("previous"):
            data["previous"]=data['previous'].replace('https://demo.credy.in/api/v1/maya','http://127.0.0.1:8000')

        return Response(data)

from django.db.models import Count

'''
Creating a Collection Class 

'''
class CollectionView(APIView):
    '''
    Create New Collection, or list a collection
    '''

    # Authentication Of User With JWT Token 
    permission_classes=(IsAuthenticated,)
    authentication_classes= [JWTAuthentication]

    def post(self,request):
        # Get the Current Logged in user(Using JWT Token)
        user = self.request.user
        serializer=CollectionSerializer(data=request.data)
        if serializer.is_valid():
            collectionInstance=serializer.save(user=user)

            res ={'collection_uuid':serializer.data['uuid']}
            return Response(res, status=status.HTTP_201_CREATED)
        # If serializer is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        '''
        Get the favourite genres and the collection data of movies
        '''
        genres = dict()
        all_genres = []
        for movie in  Movie.objects.filter(collection__user=request.user):
          genre = (movie.genres).split(',')
          all_genres.extend(genre)

        #Creating a list with genre,count
        for genre in all_genres:
            genres[genre] = genres.get(genre,0)+1

        # Sort by multiple keys First Descending and than Alphabetically (when frequecy same)
        sorted_genres = sorted(genres.items(), key=lambda x: (-x[1],x[0]))
        # Getting the top 3 genre
        top_genres = [genre[0] for genre in sorted_genres[:3]]
        collection_qs = Collection.objects.filter(user=request.user)
        
        if collection_qs is not None:
            response_data = {
                "collections": [{"title": collection.title, "uuid": str(collection.uuid), "description": collection.description}\
                                for collection in collection_qs],
                "favourite_genres": ", ".join(top_genres)
            }

        return Response({"is_success": True, "data": response_data})



'''
Creating a Collection UUID Class For (PUT,DELETE,GET)

'''
class CollectionUUIDView(APIView):
    '''
    Get, Update or Delete a Particular CollectionUUID instance
    '''

    # Authentication Of User With JWT Token 
    permission_classes=(IsAuthenticated,)
    authentication_classes= [JWTAuthentication]
    
    def get_object(self, collection_uuid):
        '''
        Checking That the Collection UUID exist for that particular User
        '''
        # Returns an object instance that should be used for detail views.
        user = self.request.user
        try:
            return user.collections.get(uuid=collection_uuid)
        except Collection.DoesNotExist:
            raise Http404

        
    def get(self,request,collection_uuid):
        '''
        Getting the Details of Particular Collection UUID 
        '''  
        collectionObj = self.get_object(collection_uuid)
        serializer=CollectionSerializer(collectionObj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def put(self,request,collection_uuid):
        '''
        Updating or partial changing the Particular Collection UUID detail
        '''
        collectionObj = self.get_object(collection_uuid)
        serializer=CollectionSerializer(collectionObj,data=request.data,partial=True)
        
        # Checking if serailizer Is valid
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self,request,collection_uuid):
        '''
        Deleting the Particular Collection UUID detail
        '''
        user = self.request.user

        try:
            collectionObj=user.collections.get(uuid=collection_uuid)
        except Collection.DoesNotExist:
            return Response({"Message":"This Collection UUID not exist"}, status=status.HTTP_404_NOT_FOUND)
    
        user.collections.get(uuid=collection_uuid).delete()
        return Response({"message":"Collection with UUID " + collection_uuid+ " Deleted Successfully!"},status=status.HTTP_204_NO_CONTENT)

       
class RequestCountView(APIView):
    '''
    Request count api view to get count of request made to the server
    '''

    # Authentication Of User With JWT Token 
    permission_classes=(IsAuthenticated,)
    authentication_classes= [JWTAuthentication]

    def get(self, request):
        '''
        Get the no of request made to the server
        '''
        countObj=RequestCount.objects.all().first()
        request_count=countObj.requestCount
        return Response({"requests": request_count},status=status.HTTP_200_OK)
    
    def post(self, request):
        '''
        It will reset the counter to 0 
        '''
        RequestCount.objects.all().delete()
        return Response({"message": "request count reset successfully"},status=status.HTTP_200_OK)