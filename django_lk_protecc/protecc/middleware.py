from .models import FraudTracker
from django.conf import settings

class ProteccFraudRequestMiddleware:
    """
    Middleware that will take a request to make a tracked_model and run logic
    to determine if it's a possible occasion of fraud. 
    If it is a fraudulent request, we can log the FraudTracker for the ip address 
    """
    def process_request(self, request, *args, **kwargs):
        # run imported settings' logic to check if request is fraudulent
        if settings.CHECK_CONTAINS_FRAUD is None:
            raise NotImplementedError(
            '''
            CHECK_CONTAINS_FRAUD is a required method for this middleware,
            please set in the settings.py
            '''
            )
        is_fraudulent, optional_attrs = settings.CHECK_CONTAINS_FRAUD(request, *args, **kwargs)
        if is_fraudulent:
            user_email = optional_attrs.get('user_email', None) if optional_attrs else None
            fraud_tracker = FraudTracker(
                user=request.user if not request.user_is_anonymous else None,
                request_url=request.build_absolute_uri(),
                ip_address=request.META.get('REMOTE_ADDR'),
                user_email=user_email
            )
            fraud_tracker.save()

        return None

class ProteccFraudViewMiddleware:
    """
    Middleware that will take a request to make a tracked_model and run logic
    to determine if it's a possible occasion of fraud. 
    If it is a fraudulent request, we can log the FraudTracker for the ip address 
    """
    def process_view(self, request, *args, **kwargs):
        # run imported settings' logic to check if request is fraudulent
        if settings.CHECK_CONTAINS_FRAUD is None:
            raise NotImplementedError(
            '''
            CHECK_CONTAINS_FRAUD is a required method for this middleware,
            please set in the settings.py
            '''
            )
        is_fraudulent, optional_attrs = settings.CHECK_CONTAINS_FRAUD(request, *args, **kwargs)
        if is_fraudulent:
            user_email = optional_attrs.get('user_email', None) if optional_attrs else None
            fraud_tracker = FraudTracker(
                user=request.user if not request.user.is_anonymous else None,
                request_url=request.build_absolute_uri(),
                ip_address=get_ip_from_request(request),
                user_email=user_email
            )
            fraud_tracker.save()

        return None

def get_ip_from_request(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip