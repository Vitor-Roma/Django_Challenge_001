# Django-Challenge-001

## Introduction

This is my first django project with API, i learned a lot of new tools and how i can use them to future projects while also improving the knowledge i already had to begin with.

## Installation


```python
- Docker
- Docker Compose
- Makefile
- Postman
```

## First steps

- Rename your '.env_sample' file to '.env' to connect to database
- open your terminal and type:
```
make run
make build
```


## To realize all tests type:

```
make test
```


# Database

## Articles

    
      "id": "39df53da-542a-3518-9c19-3568e21644fe",
      "author": {
        "id": "2d460e48-a4fa-370b-a2d0-79f2f601988c",
        "name": "Author Name",
        "picture": "https://picture.url"
      },
      "category": "Category",
      "title": "Article title",
      "summary": "This is a summary of the article",
      "firstParagraph": "<p>This is the first paragraph of this article</p>"
      "body": "<div><p>Second paragraph</p><p>Third paragraph</p></div>" 

## Authors

    {
    "id": "2d460e48-a4fa-370b-a2d0-79f2f601988c",
    "name": "Author Name",
    "picture": "https://picture.url"}


# API End-Points

- You can now open the API in the Postman and import Collections and Environment from Postman directory

<img src='https://user-images.githubusercontent.com/105290851/169929406-6b3b47a2-7297-4404-abc9-151bb112af41.png'>


    0.0.0.0:8000 (default page)
    0.0.0.0:8000/api/sign-up (Create an user)
    0.0.0.0:8000/api/login (Get your acess Token)
    0.0.0.0:8000/api/admin/authors  (List all authors)  *need token
    0.0.0.0:8000/api/admin/articles (List all articles) * need token
    0.0.0.0:8000/api/articles (list all articles) **can read without token, but not with full access
    
    
# Source

[Jungle Devs - Django Challenge #001] (https://github.com/JungleDevs/django-challenge-001)
