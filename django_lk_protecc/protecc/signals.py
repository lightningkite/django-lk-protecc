from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import WhiteListTracker, FraudTracker
from django.conf import settings
from django.core.cache import cache

@receiver(post_save, sender=FraudTracker)
def handle_fraud_tracking(sender, created, **kwargs):
    #check if it's a whitelisted ip
    if cache.get(f'{sender.ip_address}-whitelisted-ip'):
        return
    #check for related ip addresses in other fraud trackers
    related_trackers = FraudTracker.objects.filter(ip_address=sender.ip_address)
    #check if there are too many strikes
    if related_trackers.count() > settings.ALLOWED_STRIKES:
        # send email to given address
        # tell flarecloud to block the ip address
            # if this fails, tell administrator
        pass
    pass

@receiver(post_save, sender=WhiteListTracker)
def add_whitelist_cache(sender, **kwargs):
    # resets the cache for whitelisted ip addresses
    cache.delete_many(cache.keys('*-whitelisted-ip'))
    for tracker in WhiteListTracker.objects.all():
        cache.set(tracker.ip_address, tracker.pk) 