from django.db import models
from apps.authentication.models import UserOwnModel

class SubscriptionNotificationModel(models.Model):
    user = models.ForeignKey(UserOwnModel, on_delete=models.CASCADE,related_name='subscription_notifications')
    auth = models.CharField(max_length=100)
    endpoint = models.URLField(max_length=500)
    p256dh = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        subscription_notifications = SubscriptionNotificationModel.objects.filter(
            user = self.user,
            auth = self.auth,
            endpoint = self.endpoint,
            p256dh = self.p256dh
        )
        if subscription_notifications:
            return 'Data used'
        return super().save(*args, **kwargs)