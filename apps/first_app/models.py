# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import bcrypt
from django.db import models

# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class UserManager(models.Manager):
    def validatelogin(self, post_data):
        errors = []

        if len(self.filter(email=post_data['email'])) > 0:

            user = self.filter(email=post_data['email'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(),user.password.encode()):
                errors.append('email/password incorrect')
        else:
            errors.append('email/password incorrect')
        if errors:
            return errors
        return user

    def validateregistration(self, post_data):
        errors = []

        if len(post_data['name']) < 2 or len(post_data['alias']) < 2:
            errors.append('name fields must be at least 3 characters')

        if len(post_data['password']) < 8:
            errors.append('password must be at least 8 characters')

        if not re.match(NAME_REGEX, post_data['name']):
            errors.append('Name field must be alpha characters only')

        if not re.match(EMAIL_REGEX, post_data['email']):
            errors.append('invalid email format')
        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors.append('email already in use')
        if post_data['password'] != post_data['password_confirm']:
            errors.append('passwords do not match')

        if not errors:

            hashed= bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

            new_user = self.create(
                name = post_data['name'],
                alias = post_data['alias'],
                email = post_data['email'],
                password = hashed
            )
            return new_user
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    objects = UserManager()
        
    def __repr__(self):
        return "User: \n{}\n{}\n{}\n".format(self.id, self.name, self.email)
    def __str__(self):
        return "User: \n{}\n{}\n{}\n".format(self.id, self.name, self.email)