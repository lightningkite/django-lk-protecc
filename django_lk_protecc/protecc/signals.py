from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import WhiteListTracker, FraudTracker
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail

@receiver(post_save, sender=FraudTracker)
def handle_fraud_tracking(sender, instance, created, **kwargs):
    if cache.get(f'{instance.ip_address}-whitelisted-ip'):
        return

    related_trackers = FraudTracker.objects.filter(ip_address=instance.ip_address)

    if related_trackers.count() >= settings.ALLOWED_STRIKES:
        urls = ', '.join(related_trackers.values_list('request_url', flat=True)) 
        alert_admin(
            'An IP address has been blocked in your application',
            f'Site: {settings.SITE_NAME} \nIP address: {instance.ip_address} \nurl history: {urls}'
        )
        # TODO: tell flarecloud to block the ip address
            # if this fails, tell administrator

@receiver(post_save, sender=WhiteListTracker)
def add_whitelist_cache(sender, instance, **kwargs):
    cache.set(f'{instance.ip_address}-whitelisted-ip', instance.pk) 

@receiver(post_delete, sender=WhiteListTracker)
def remove_whitelist_cache(sender, instance, **kwargs):
    cache.delete(f'{instance.ip_address}-whitelisted-ip')

def alert_admin(subject, message, from_email=None, **kwargs):
    send_mail(subject, message, from_email, [settings.ADMIN_EMAIL], **kwargs)