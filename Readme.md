## Overview
This App integrates with a third-party movie API to serve a paginated list of movies and their respective genres.
Using the REST APIs of the users can view the movie details and add them to their collections.
It also allows users to create multiple collection of movies while keeping a track of top 3 genres present across the collections owned by each user.

## Setup and Installation

1. Clone the project.
    ```
    git clone https://github.com/linkdin-7/movies-assign.git
    ```

2. Run virtual environment in the root folder
    ```
    python -m venv test
    test\Scripts\activate
    ```

3. Install required packages using requirement.txt in the movieCollection folder.

    ```
    pip install -r requirement.txt
    ```

4. Run Migrate Command
    ```
    python manag.py makemigrations
    python manage.py migrate
    ```

5. Run the Django Server
    ```
    python manage.py runserver
    ```

6. Use **POST http://localhost:8000/register/** to register with a username and password.

7. After registering, you will receive an **access token**. Use the token for authorization in the following requests that you will be making.


## API Reference
|   API  | Parameter     | Description                |
| :-------- | :------- | :------------------------- |
| `POST http://localhost:8000/register/` | `username, password` | **Required** for registration |
| `GET http://localhost:8000/movies/` | `-` | Return paginated list of movies from 3rd party API |
| `GET http://localhost:8000/collection/` | `-` | Return all collections of user |
| `POST http://localhost:8000/collection/` | `-` | Creates a collection of movies |
| `PUT http://localhost:8000/collection/<collection_uuid>/` | `collection_uuid` |Update the particular collection |
| `GET http://localhost:8000/collection/<collection_uuid>/` | `collection_uuid` |Returns data of the particular collection |
| `DELETE http://localhost:8000/collection/<collection_uuid>/` | `collection_uuid` | Deletes the particular collection|
| `GET http://localhost:8000/request-count/` | `-` |Returns the counter number of request served|
| `POST http://localhost:8000/request-count/reset/` | `-` |Resets the request counter |




## Register the app
![Register_paylo](https://github.com/linkdin-7/movies-assign/assets/56730903/ac04fa79-11c1-4cbd-bdba-00d5d6a23aad)

# Register Successfully(Get the Access Token)
![Register_suc](https://github.com/linkdin-7/movies-assign/assets/56730903/234f57dd-f4ba-4353-bc38-763906485a10)

## Get list of movies
![movie_list](https://github.com/linkdin-7/movies-assign/assets/56730903/c2c9525f-9b03-4c80-8a71-994f19dee156)

## Creating a Collection
![collection_post](https://github.com/linkdin-7/movies-assign/assets/56730903/79435f01-1346-4b19-aeb3-725e33ac3c6f)

## Get a Collections with Top 3 Genres
![collection_get(for particular user)](https://github.com/linkdin-7/movies-assign/assets/56730903/64de03c4-3dd8-470d-b672-d0cfba917b2e)

## Get The Collection UUID Details
![collectionuuid_get](https://github.com/linkdin-7/movies-assign/assets/56730903/e1fe3882-8554-4c83-8c9d-0d393264518b)

## Update The Collection with UUID
![update_collectionuuid](https://github.com/linkdin-7/movies-assign/assets/56730903/10bc0c33-1b80-4bff-99fe-ca26c2018065)

## Delete The Particular Collection with UUID
![delete_collectionuuid](https://github.com/linkdin-7/movies-assign/assets/56730903/40d65f1b-a5d3-4ebd-8110-5771ee3851d3)

## Get Request count for Session
![get_req_count(middleware)](https://github.com/linkdin-7/movies-assign/assets/56730903/f5b4f34c-fbb5-4fda-8e4b-8bf2df4892b4)

## Reset Request Count
![request_count_reset](https://github.com/linkdin-7/movies-assign/assets/56730903/92da19c0-a7a3-43cb-8f7e-9122cb14e749)



