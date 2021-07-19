from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class FraudTracker(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    request_url = models.TextField(max_length=2048) # this is the max length of any given url
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    # in case your user is an anonymous user, but you would like to store the email associated, you can use user_email
    user_email = models.EmailField(null=True)

class WhiteListTracker(models.Model):
    ip_address = models.GenericIPAddressField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # in case your user is an anonymous user, but you would like to store the email associated, you can use user_email
    user_email = models.EmailField(null=True)