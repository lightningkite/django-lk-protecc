from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class FraudTracker(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    request_url = models.TextField(max_length=2048) # this is the max length of any given url
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()

class WhiteListTracker(models.Model):
    ip_address = models.GenericIPAddressField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)