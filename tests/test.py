import pytest
from django.contrib.auth.models import User
from factories import RegisterFactory,CollectionFactory,MovieFactory
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken


client = APIClient()


@pytest.fixture()
def user_token():
        user= User.objects.create_user(username="test", password="passtest")
        refresh = RefreshToken.for_user(user)
        return refresh.access_token


@pytest.mark.django_db
class TestViews:
    def test_create_register(self, client) -> None:
            '''
            Testing the Register
            '''
            register: Register = RegisterFactory()
            response = client.post(
                "/register/",
                {"username": "New1", "password": "Tech@123"},
            )
            assert response.status_code == 201
            userinstance = response.data['access_token']
            return userinstance

    def test_get_collection(self,client,user_token):
        '''
        Testing the collection get
        '''
        response = client.get("/collection/", HTTP_AUTHORIZATION=f"Bearer {user_token}",)

        assert response.status_code == 200
        assert response.data['is_success'] == True
        assert "favourite_genres" in response.data['data']

    def test_get_movielist(self,client,user_token):
        '''
        Testing the Movielist
        '''
        response = client.get('/movies/',HTTP_AUTHORIZATION=f"Bearer {user_token}",)
        data = response.data
        assert response.status_code == 200
        assert "count" in data
        assert "next" in data
        assert "previous" in data
        assert len(data["results"]) == 10


@pytest.mark.django_db
def test_collection_create(user_token):
    '''
    Testing the Collection  
    '''
    user= User.objects.create_user(username="test_new", password="passtest")
    movies_payload = [
        dict(
            title = "movie_title",
            description = "movie_description",
            genres = "movie_genres",
            uuid = "4cac8453-a512-4bde-b79d-e2f5bc897a5f"
        )
    ]

    collection_payload = dict(
        title = "collection_title",
        description = "collection_description",
        movies = movies_payload,
        username = user.id
    )

    response = client.post("/collection/", collection_payload, HTTP_AUTHORIZATION=f"Bearer {user_token}",format='json')

    assert response.status_code == 201
    assert 'collection_uuid' in response.data


'''
Testing the Request Count 
'''
@pytest.mark.django_db
def test_request_count(client,user_token):
    response = client.get('/request-count/', HTTP_AUTHORIZATION=f"Bearer {user_token}", )
    assert response.status_code == 200
    assert response.data["requests"] > -1



@pytest.mark.django_db
def test_request_count_reset(client,user_token):
    response = client.post('/request-count/reset/', HTTP_AUTHORIZATION=f"Bearer {user_token}",)
    assert response.status_code == 200
    assert response.data["message"]  == "request count reset successfully"

  