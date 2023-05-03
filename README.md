# api_yamdb
## Description
API_YAMDB is a project-data base of products of literature, cinematography, art and other culture spheres.
On this resource you can get/add information about the products you are interested in: read a reviews about this products and learn an opinion of other people, also add your own comment or review.  

## Installing on the local machine
1. clone this repository
2. create venv and activate it 
3. install all the requirements from requirements.txt
4. run server
5. Complete. App ready to use it

## Examples of requests
It is a 5 roles of users in this project:
-Anonym (can make only get-requests)
-Authorized user (besides the get-requests, he also can add reviews, comments, categories and titles)
-Moderator (Can patch/delete all reviews and comments added by other users)
-Admin (Full possibility to manage all content on the resource)
-Superuser Django (always admin)

For unauthorized user other endpoints are available:
api/v1/categories/ - Получение списка всех категорий
api/v1/genres/ - Получение списка всех жанров
api/v1/titles/ - Получение списка всех произведений
api/v1/titles/{title_id}/reviews/ - Получение списка всех отзывов
api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Получение списка всех комментариев к отзыву

For registration you have to post your email and username on api/v1/auth/signup/, then post gotten confirmation code and username to api/v1/auth/token/. After that you can add new reviews and comments to reviews.
### Examples of post-requests

for review create(post-request):

endpoint: '/api/v1/titles/{title_id}/reviews/'

body of request:
{
"text": "string",
"score": 1
}

for reading the comments on the product(get-request):

endpoint: '/api/v1/titles/{title_id}/reviews/{review_id}/comments/'

## All examples of requests on the endpoint: '/redoc/'
