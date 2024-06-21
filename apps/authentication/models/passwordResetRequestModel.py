from django.db import models
from django.utils import timezone
from datetime import datetime
from .userModel import UserOwnModel
import random

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