from django.db import models
from apps.authentication.models import UserOwnModel

class FriendshipApplication(models.Model):
    applicator = models.ForeignKey(UserOwnModel, on_delete=models.CASCADE, related_name='applications_from_me')
    applied = models.ForeignKey(UserOwnModel, on_delete=models.CASCADE, related_name='applications_to_me')

    @classmethod
    def application_is_valid(cls, applicator, applied):
        return FriendshipApplication.objects.filter(applicator = applicator, applied = applied).first()  == None