from django.dispatch import receiver

from django.db.models.signals import post_save

from .models import PhoneNumber, PhoneConfirmation


@receiver(post_save, sender=PhoneNumber)
def handle_user_save(sender, instance, created, **kwargs):
    if created:
        PhoneConfirmation.objects.send_confirmation(instance)
