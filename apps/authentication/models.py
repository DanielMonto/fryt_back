from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime
import random
import re

def generate_code():
    '''
        Generates random code of 7 length
    '''
    code=''
    lists=[[chr(i) for i in range(65,79)],[f"{i}" for i in range(10)] ,[chr(i) for i in range(97, 111)]]
    for _ in range(7):
        list_chosen=random.choice(lists)
        char=random.choice(list_chosen)
        code+=str(char)
    return code 

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
            return False, 'Email and username unused'
        # Email or username used because users is not empty
        else:
            user=users[0]
            # Chose the right message depending if email and username are used or if one of them is
            message='Username and email used' if user.username==username and user.email==email else 'Email used' if user.email==email else 'Username used'
            return True, message
    
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

class PasswordResetRequest(models.Model):
    '''
        Model for requesting a reset password
    '''
    user=models.OneToOneField(UserOwnModel,on_delete=models.CASCADE)
    code=models.CharField(max_length=7,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def generate_unique_code(self):
        '''
            Generates unique code for checking precedence
        '''
        code_generated=""
        # Do a loop until finds an unused code
        while True: 
            code_generated=generate_code()
            # Checks the code_generated is not used
            if len(PasswordResetRequest.objects.filter(code=code_generated))==0:
                return code_generated
    
    def save(self,*args,**kwargs):
        '''
            Save method adapting expiration time and code
        '''
        self.code=self.generate_unique_code()
        self.expires_at=timezone.now() + datetime.timedelta(minutes=30)
        return super().save(*args,**kwargs)
    
    @classmethod 
    def is_valid_code(cls, password_reset_request):
        '''
            Checks if the reset password request is still valid,
            whether by date or not exist
        '''
        # Checks if the password_reset_request param is not a PasswordResetRequest
        if not isinstance(password_reset_request,cls):
            password_reset_requests=cls.objects.filter(code=password_reset_request)
            # Code unused return False
            if len(password_reset_requests)==0:
                return False
            password_reset_request=password_reset_requests[0]
        # Code expired by time
        if password_reset_request.expires_at > timezone.now():
            return True
        # Code invalid deleted, returning False
        password_reset_request.delete()
        return False

#1029580425JO'han
#https://www.facebook.com/login_alerts/start/?fbid=122131509242221724&s=j&notif_id=1713215384798992&notif_t=login_alerts_new_device&ref=notif
