from django.db import models
import re, bcrypt
from time import gmtime, strftime, localtime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$')

######################################################################################
#                                   Validator                                        *
######################################################################################
class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        all_users = User.objects.all()

        if len(post_data['fname']) < 3:
            errors["fname"] = "The first name must be at least 3 characters"
        if len(post_data['lname']) < 3:
            errors["lname"] = "The last name must be at least 3 characters"
        if all_users.filter(email=(post_data['email'])):
            errors['email'] = "Email already exists in system"
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Email must be in standard format: abc@abc.com"
        if len(post_data['password']) < 8:
            errors["password"] = "The password must be at least 8 characters"
        if post_data['password'] != post_data['confirm']:
            errors['password'] = "Your passwords do not match!"
        return errors

    def login_validator(self, post_data):
        errors = {}
        
        email = post_data['email']
        password = post_data['password']
        data = User.objects.filter(email=email)
        # Email - Ensure valid format:
        if not EMAIL_REGEX.match(email):
            errors["email"] = "Invalid Email Address!"
        # Check that the user is registered:
        elif len(data) == 0:
            errors["email"] = "This email does not match our records"
        # Make sure the password matches:
        elif not bcrypt.checkpw(password.encode(), data[0].password.encode()):
            errors["password"] = "Password is incorrect"
        return errors

######################################################################################
#                               Login Classes                                        *
######################################################################################
class User(models.Model):
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    email = models.CharField(max_length=55)
    password = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()