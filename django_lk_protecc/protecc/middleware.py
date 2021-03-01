from .models import FraudTracker
from django.conf import settings

class ProteccFraudMiddleware:
    """
    Middleware that will take a request to make a tracked_model and run logic
    to determine if it's a possible occasion of fraud. 
    If it is a fraudulent request, we can log the FraudTracker for the ip address 
    """
    def process_request(self, request):
        # run imported settings' logic to check if request is fraudulent
        if settings.CHECK_CONTAINS_FRAUD is None:
            raise NotImplementedError(
            '''
            CHECK_CONTAINS_FRAUD is a required method for this middleware,
            please set in the settings.py
            '''
            )
        if settings.CHECK_CONTAINS_FRAUD(request):
            fraud_tracker = FraudTracker(
                user=request.user,
                request_url=request.build_absolute_uri(),
                ip_address=request.META.get('REMOTE_ADDR')
            )
            fraud_tracker.save()

        return None
