'''
MovieList App urls.py
'''
from django.urls import path

from .views import MovieList,CollectionView,CollectionUUIDView,RequestCountView

urlpatterns = [
    path('movies/',MovieList.as_view(),name='movie-list'),
    path('collection/',CollectionView.as_view(),name='collectionview'),
    path('collection/<collection_uuid>/',CollectionUUIDView.as_view(),name='collectionuuidview'),
    path('request-count/', RequestCountView.as_view(), name='updaterequestCount'),
    path('request-count/reset/',RequestCountView.as_view(), name='resetrequestCount')
    
    
    
]
