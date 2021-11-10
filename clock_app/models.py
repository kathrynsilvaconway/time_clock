import bcrypt
from django.db import models
import re

from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
class UserManager(models.Manager):
    def reg_validator(self, postData):
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if not email_regex.match(postData['email']):
            errors['email'] = "Pleas enter a valid email address."
        if len(User.objects.filter(email = postData['email'])) > 0:
            errors['emailAlreadyExists'] ="There is already an account associated with this email address."
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters."
        if postData['first_name'].isalpha() == False:
            errors['first_name'] = "Frist name must contain only letters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters."
        if postData['last_name'].isalpha() == False:
            errors['last_name'] = "Last name must contain only letters."
        if len(postData['password']) < 5:
            errors['password_length'] = "Password must be at least 5 characters."
        if postData['password'] != postData['conf_password']:
            errors['password_no_match'] = 'Passwords do not match'
        return errors
    
    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email = postData['email'])
        if len(user) == 0:
            errors['bad_email'] = "We can't find an account for that email address."

        elif bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()) == False:
            errors['bad_password'] = "Password is incorrect."
        return errors
    
    def update_validator(self, postData):
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if not email_regex.match(postData['email']):
            errors['email'] = "Pleas enter a valid email address."
        if len(postData['first_name']) < 1:
            errors['first_name'] = "First name is required."
        if len(postData['last_name']) < 1:
            errors['last_name'] = "last name is required."
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True )
    objects = UserManager()