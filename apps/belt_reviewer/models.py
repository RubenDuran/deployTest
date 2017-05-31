from __future__ import unicode_literals
from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):

    def validate(self, post):
        errors = []
        if len(post['name']) < 2:
            errors.append('Name must be at least 2 characters long')
        if not post['name'].isalpha():
            errors.append('Name can only contain letters')
        if len(post['alias']) < 2:
            errors.append('Alias must be at least 2 characters long')
        if not EMAIL_REGEX.match(post['email']):
            errors.append('Invalid Email Address!')
        if len(post['pw']) < 8:
            errors.append('password must be at least 8 characters long')
        if post['pw'] != post['pwconf']:
            errors.append('password and confirmation fields do not match')
        check_email = self.filter(email=post['email'])
        if check_email:
            errors.append('email already exist in the database')
        return errors

    def signin(self, post):
        errors = []
        if not EMAIL_REGEX.match(post['email']):
            errors.append('Invalid Email Address!')
        elif len(post['pw']) < 8:
            errors.append('password must be at least 8 characters long')
        else:
            email = post['email']
            pw = post['pw']
            check_email = self.filter(email=post['email'])
            if not check_email:
                errors.append('no such user in database')
            else:
                pw_check = self.get(email=post['email'])
                if pw != pw_check.password:
                    errors.append('Incorect Password for user')
                else:
                    pass
        return errors

class BookManager(models.Manager):

    def validate(self, post):
        errors = []
        if len(post['title']) < 2:
            errors.append('Title must be at least 2 characters long')
        if len(post['review']) < 8:
            errors.append('Review must be at least 8 characters long')
        if post['new_author'] != "":
            author = post['new_author']
        else:
            author = post['author']
        check_title = self.filter(title=post['title'])
        check_author = self.filter(author__name=author)
        if check_title and check_author:
            errors.append('Book already exist in the database')
        return errors


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    rating = models.CharField(max_length=255)
    author = models.ForeignKey('Author')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = BookManager()


class Review(models.Model):
    user = models.ForeignKey('User')
    book = models.ForeignKey('Book')
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
