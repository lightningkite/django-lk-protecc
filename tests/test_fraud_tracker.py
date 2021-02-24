from django.test import TestCase
from django_lk_protecc.protecc.middleware import ProteccFraudMiddleware
from django_lk_protecc.protecc.models import FraudTracker, WhiteListTracker
from django.conf import settings
from django.contrib.auth.models import User
from unittest.mock import Mock


class FraudTrackerTests(TestCase):
    def setUp(self):
        self.request = Mock()
        self.request.META = { 
                "HTTP_PROFILE_ID" : 1, 
                "REQUEST_METHOD": "POST", 
                "HTTP_OPERATING_SYSTEM_VERSION":"FAKE", 
                "HTTP_APP_VERSION":"1.0.0", 
                "HTTP_USER_AGENT":"AUTOMATED TEST"
        }
        self.request.user = User.objects.create_user('johnny', 'johnny@example.com', 'johnpassword')
        self.request.path = '/testURL/'
        self.request.session = {}
        self.middleware = ProteccFraudMiddleware(lambda response: None)
        FraudTracker.objects.all().delete()

    def test_fraud_middleware(self):
        settings.contains_fraud = lambda request: True
        self.middleware.__call__(self.request)
        self.assertEqual(FraudTracker.objects.all().count(), 1)

    def test_no_fraud_middleware(self):
        settings.contains_fraud = lambda request: False
        self.middleware.__call__(self.request)
        self.assertEqual(FraudTracker.objects.all().count(), 0)
    
    def test_contains_fraud_not_implemented(self):
        try:
            settings.contains_fraud = None
            self.middleware.__call__(self.request)
            print('THE NOT IMPLEMENTED ERROR IS NOT WORKING')
        except NotImplementedError:
            print('successfully warned about missing settings function')

    def test_whitelisting(self):
        WhiteListTracker.objects.create(user=self.request.user, ip_address=self.request.REMOTE_ADDR)
        settings.contains_fraud = lambda request: True
        self.middleware.__call__(self.request)
        self.assertEqual(FraudTracker.objects.all().count(), 0)

