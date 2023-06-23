'''
Identity App urls.py
'''
from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView

urlpatterns = [
    path('register/',RegisterView.as_view(), name='registration'),
    path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh'), 
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair')
]