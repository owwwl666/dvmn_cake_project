from django.db.models.signals import post_save
from django.dispatch import receiver

from cake_app.models import Order
from cake_app.bakerbot import send_order


@receiver(post_save, sender=Order)
def send_orders(sender, instance, created, **kwargs):
    if created:
        send_order(instance)

