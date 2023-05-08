# api_yamdb
## Description
API_YAMDB is a project-data base of products of literature, cinematography, art and other culture spheres.
On this resource you can get/add information about the products you are interested in: read a reviews about this products and learn an opinion of other people, also add your own comment or review.  

## Installing on the local machine (All commands in cmd/bash)
1. clone this repository 
```
git clone git@github.com:N89701/api_yamdb.git
```
2. create venv and activate it 
```
python -m venv 
```
```
venv source venv/Scripts/activate or source venv/bin/activate for Mac and Linux
```
3. install all the requirements from requirements.txt 
```
pip install -r requirements.txt
```
4. Follow to the working directory
```
cd api_yamdb
``` 
5. Migrate data-base
```
python manage.py makemigrations
``` 
```
python manage.py migrate
``` 
6. Load csv-data to database on your local computer 
```
python manage.py load_data
``` 
7. run server 
```
python manage.py runserver
```
8. Complete. App is ready to use it

## Examples of requests
It is a 5 roles of users in this project:
-Anonym (can make only get-requests)
-Authorized user (besides the get-requests, he also can add reviews, comments, categories and titles)
-Moderator (Can patch/delete all reviews and comments added by other users)
-Admin (Full possibility to manage all content on the resource)
-Superuser Django (always admin)

For unauthorized user other endpoints are available:
api/v1/categories/ - Getting categories list
api/v1/genres/ - Getting genres list
api/v1/titles/ - Getting titles list
api/v1/titles/{title_id}/reviews/ - Getting reviews for particular title list 
api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Getting comments for particular review list

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
## Project designed by:
1.Nikolay Khvan(https://github.com/N89701/)
2.Anton Kuznetsov(https://github.com/kuzantiv)
3.Yuri Pomazkin(https://github.com/1yunker)
