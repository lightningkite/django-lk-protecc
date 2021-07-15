from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import WhiteListTracker, FraudTracker
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from datetime import datetime, timedelta
from .utils import block_ip_address
# import requests
# import json

@receiver(post_save, sender=FraudTracker)
def handle_fraud_tracking(sender, instance, created, **kwargs):
    if cache.get(f'{instance.ip_address}-whitelisted-ip'):
        return
    elif WhiteListTracker.objects.filter(ip_address=instance.ip_address).exists():
        cache.set(f'{instance.ip_address}-whitelisted-ip', instance.pk)
        return

    expiration_delta = getattr(settings, 'DAYS_TO_EXPIRATION', None)
    time_range = datetime.now() - timedelta(days=expiration_delta or 0)
    import pdb; pdb.set_trace()
    related_trackers = FraudTracker.objects.filter(ip_address=instance.ip_address, created_at__gt=time_range)

    message = f'Site: {settings.SITE_NAME} \nIP address: {instance.ip_address}'
    url_message = f'\nurl {instance.request_url}'
    message += url_message
    user = instance.user.username if instance.user else 'Anonymous User'
    message += f'\nUser: {user}'
    email =  instance.user_email if not instance.user else instance.user.email
    message += f'\nEmail: {email}' if email else ''
    alert_admin(f'A request has been determined fraudulent in your app, currently the strike count is: {related_trackers.count()}', message)

    if related_trackers.count() >= settings.ALLOWED_STRIKES:
        urls = ', '.join(related_trackers.values_list('request_url', flat=True)) 
        url_history = f'\nurl history: {urls}'
        message += url_history
        alert_admin('An IP address has been blocked in your application', message)

        response = block_ip_address(instance.ip_address)
        if response.json().get('success') == False:
            alert_admin(
                'a request to block an IP address has failed',
                f'Site: {settings.SITE_NAME} \nIP address: {instance.ip_address} \nresponse: {response.json()}'
            )

@receiver(post_save, sender=WhiteListTracker)
def add_whitelist_cache(sender, instance, **kwargs):
    cache.set(f'{instance.ip_address}-whitelisted-ip', instance.pk) 

@receiver(post_delete, sender=WhiteListTracker)
def remove_whitelist_cache(sender, instance, **kwargs):
    cache.delete(f'{instance.ip_address}-whitelisted-ip')

def alert_admin(subject, message, from_email=None, **kwargs):
    send_mail(subject, message, from_email, [settings.ADMIN_EMAIL], **kwargs)

# def block_ip_address(ip_address):
#     headers = {
#         'X-Auth-Email': settings.CL_AUTH_EMAIL,
#         'X-Auth-Key': settings.CL_AUTH_KEY,
#         'Content-Type': 'application/json',
#     }

#     data = {
#         'ip': ip_address,
#         'comment': f'blocked ip for {settings.SITE_NAME}' 
#     }

#     response = requests.post(
#         f'https://api.cloudflare.com/client/v4/accounts/{settings.CL_ACCOUNT_ID}/rules/lists/{settings.CL_LIST_ID}/items',
#         headers=headers,
#         data=f'[{json.dumps(data)}]'
#     )

#     return response
