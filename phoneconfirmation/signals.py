from django.dispatch import Signal


phone_confirmed = Signal(providing_args=["phone_number"])
