import django
from django.conf import settings
import dev_settings

settings_params = dev_settings.settings()
settings.configure(**settings_params)
django.setup()

from django.test import TestCase
from django_lk_protecc.protecc.middleware import ProteccFraudViewMiddleware, ProteccFraudRequestMiddleware
from django_lk_protecc.protecc.models import FraudTracker, WhiteListTracker
from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser
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
        self.request_middleware = ProteccFraudRequestMiddleware()
        self.view_middleware = ProteccFraudViewMiddleware()
        FraudTracker.objects.all().delete()

    def test_fraud_request_middleware(self):
        settings.CHECK_CONTAINS_FRAUD = lambda request, *args, **kwargs: (True, None)
        self.request_middleware.process_request(self.request)
        self.assertEqual(FraudTracker.objects.all().count(), 1)

    def test_no_fraud_request_middleware(self):
        settings.CHECK_CONTAINS_FRAUD = lambda request, *args, **kwargs: (False, None)
        self.request_middleware.process_request(self.request)
        self.assertEqual(FraudTracker.objects.all().count(), 0)

    def test_fraud_view_middleware(self):
        settings.CHECK_CONTAINS_FRAUD = lambda request, *args, **kwargs: (True, None)
        self.view_middleware.process_view(self.request, 'a value', 'another value')
        self.assertEqual(FraudTracker.objects.all().count(), 1)

    def test_no_fraud_view_middleware(self):
        settings.CHECK_CONTAINS_FRAUD = lambda request, *args, **kwargs: (False, None)
        self.view_middleware.process_view(self.request, 'a value', 'another value')
        self.assertEqual(FraudTracker.objects.all().count(), 0)

    def test_fraud_view_middleware_anonymous_user(self):
        settings.CHECK_CONTAINS_FRAUD = lambda request, *args, **kwargs: (True, {'user_email': 'anonymoususer@fraud.com'})
        self.request.user = AnonymousUser()
        self.view_middleware.process_view(self.request, 'a value', 'another value')
        self.assertEqual(FraudTracker.objects.first().user_email, 'anonymoususer@fraud.com')
        self.assertEqual(FraudTracker.objects.all().count(), 1)

    def test_fraud_view_middleware_extra_content(self):
        extra_content = '''
            Hey there! This is some extra content with a few things
            - thing 1
            - thing 2
            - thing 3
            - facebook.com
        '''
        settings.CHECK_CONTAINS_FRAUD = lambda request, *args, **kwargs: (True, {'user_email': 'anonymoususer@fraud.com', 'extra_content': extra_content})
        self.request.user = AnonymousUser()
        self.view_middleware.process_view(self.request, 'a value', 'another value')
        self.assertEqual(FraudTracker.objects.first().user_email, 'anonymoususer@fraud.com')
        self.assertEqual(FraudTracker.objects.all().count(), 1)
    
    def test_contains_fraud_not_implemented(self):
        try:
            settings.CHECK_CONTAINS_FRAUD = None
            self.request_middleware.process_request(self.request)
            self.fail('the middleware should throw an error without a CHECK_CONTAINS_FRAUD function')
        except NotImplementedError:
            pass
    
    def test_whitelisting(self):
        white_list_tracker = WhiteListTracker(user=self.request.user, ip_address=self.request.META.get('REMOTE_ADDR'))
        white_list_tracker.save()
        self.assertIsNotNone(cache.get(f'{self.request.META.get("REMOTE_ADDR")}-whitelisted-ip'))

