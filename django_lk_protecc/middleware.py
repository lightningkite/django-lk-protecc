from .models import FraudTracker
from django.conf import settings

class ProteccFraudMiddleware:
    """
    Middleware that will take a request to make a tracked_model and run logic
    to determine if it's a possible occasion of fraud. 
    If it is a fraudulent request, we can log the FraudTracker for the ip address 
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # run imported settings' logic to check if request is fraudulent
        if settings.contains_fraud(request):
            FraudTracker.objects.create(
                user=request.user,
                request_url=request.url,
                ip_address=request.REMOTE_ADDR
            )

        return self.get_response(request)
