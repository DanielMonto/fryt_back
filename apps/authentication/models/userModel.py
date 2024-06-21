from django.contrib.auth.models import AbstractUser
from django.db import models
import re

class UserOwnModel(AbstractUser):
    '''
        User model, for user management
    '''
    @classmethod
    def email_or_username_used(cls,username,email):
        '''
            Checks if there is an user with those credentials (email and username)
        '''
        users=cls.objects.filter(models.Q(username=username) or models.Q(email=email))
        # Users empty, email and username unused
        if len(users)==0:
            return False, 'Email and username unused', None
        # Email or username used because users is not empty
        else:
            user=users[0]
            # Chose the right message depending if email and username are used or if one of them is
            if user.username==username and user.email==email:
                message='Username and email used'
                field='username/email'
            elif user.email==email:
                message='Email used'
                field='email'
            else:
                message='Username used'
                field='username'
            return True, message, field
    
    @staticmethod
    def safe_password(password):
        '''
            Checks if the password is safe
        '''
        # Check if the length of the password is less than 8 characters
        if len(password) < 8:
            return False, 'Password must be at least 8 characters long'
        # Check if the password does not contain at least one uppercase letter
        if not re.search(r"[A-Z]", password):
            return False, 'Password must contain at least one uppercase letter'
        # Check if the password does not contain at least one lowercase letter
        if not re.search(r"[a-z]", password):
            return False, 'Password must contain at least one lowercase letter'
        # Check if the password does not contain at least one digit
        if not re.search(r"[0-9]", password):
            return False, 'Password must contain at least one digit'
        # Check if the password does not contain at least one special character
        # If the password meets all the security criteria, return True and a success message
        return True, 'Password is safe'
        
    def __str__(self):
        '''
            Method for string representation
        '''
        return f"--{self.username} has {self.email}"