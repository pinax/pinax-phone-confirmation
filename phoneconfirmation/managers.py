import hashlib
import random

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone

from django.contrib.sites.models import Site

from . import sms
from .signals import phone_confirmed
from .utils import digits_only


class PhoneNumberManager(models.Manager):

    def add_phone(self, user, phone, country_code):
        phone_number, created = self.get_or_create(
            user=user,
            phone_number=phone,
            country_code=country_code
        )
        return phone_number

    def get_primary(self, user):
        try:
            return self.get(user=user, primary=True)
        except ObjectDoesNotExist:
            return None

    def number_exists(self, phone, country_code):
        digits = digits_only(phone=phone, country_code=country_code)
        return self.filter(digits_only=digits).exists()

    def get_by_number(self, phone, country_code):
        digits = digits_only(phone=phone, country_code=country_code)
        return self.get(digits_only=digits)


class PhoneConfirmationManager(models.Manager):

    def confirm_phone(self, confirm_code):
        try:
            confirmation = self.get(confirm_code=confirm_code)
        except self.model.DoesNotExist:
            return None

        if not confirmation.code_expired():
            phone_number = confirmation.phone_number
            phone_number.verified = True
            phone_number.set_as_primary(conditional=True)
            phone_number.save()
            phone_confirmed.send(sender=self.model, phone_number=phone_number)
            return phone_number

    def send_confirmation(self, phone_number):
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        confirm_code = hashlib.sha1(
            (salt + phone_number.phone_number).encode("utf8")
        ).hexdigest()[:5]
        current_site = Site.objects.get_current()

        sms.send_confirmation(
            phone_number.user,
            current_site,
            confirm_code,
            phone_number.digits_only
        )

        return self.create(
            phone_number=phone_number,
            sent=timezone.now(),
            confirm_code=confirm_code
        )

    def delete_expired_confirmations(self):
        for confirmation in self.all():
            if confirmation.code_expired():
                confirmation.delete()
