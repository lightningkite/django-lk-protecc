import django
from django.conf import settings
import dev_settings

settings_params = dev_settings.settings()
settings.configure(**settings_params)
django.setup()

from django.test import TestCase
from django_lk_protecc.protecc.middleware import ProteccFraudMiddleware
from django_lk_protecc.protecc.models import FraudTracker, WhiteListTracker
from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from unittest.mock import Mock



class FraudTrackerTests(TestCase):
    def setUp(self):
        self.request = Mock()
        self.request.META = { 
                "HTTP_PROFILE_ID" : 1, 
                "REQUEST_METHOD": "POST", 
                "HTTP_OPERATING_SYSTEM_VERSION":"FAKE", 
                "HTTP_APP_VERSION":"1.0.0", 
                "HTTP_USER_AGENT":"AUTOMATED TEST",
                "REMOTE_ADDR": "192.168.17.43" # random ip address
        }

        self.request.user = User.objects.create_user('johnny', 'johnny@example.com', 'johnpassword')
        self.request.build_absolute_uri = lambda : '/Test/url'
        self.request.session = {}
        self.middleware = ProteccFraudMiddleware()
        FraudTracker.objects.all().delete()

    def test_fraud_middleware(self):
        settings.CHECK_CONTAINS_FRAUD = lambda request: True
        self.middleware.process_request(self.request)
        self.assertEqual(FraudTracker.objects.all().count(), 1)

    def test_no_fraud_middleware(self):
        settings.CHECK_CONTAINS_FRAUD = lambda request: False
        self.middleware.process_request(self.request)
        self.assertEqual(FraudTracker.objects.all().count(), 0)
    
    def test_contains_fraud_not_implemented(self):
        try:
            settings.CHECK_CONTAINS_FRAUD = None
            self.middleware.process_request(self.request)
            self.fail('the middleware should throw an error without a CHECK_CONTAINS_FRAUD function')
        except NotImplementedError:
            pass
    
    def test_whitelisting(self):
        white_list_tracker = WhiteListTracker(user=self.request.user, ip_address=self.request.META.get('REMOTE_ADDR'))
        white_list_tracker.save()
        self.assertIsNotNone(cache.get(f'{self.request.META.get("REMOTE_ADDR")}-whitelisted-ip'))

