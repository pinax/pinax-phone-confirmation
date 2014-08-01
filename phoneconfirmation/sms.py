import json
import logging

from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

from .twilio import Message

logger = logging.getLogger(__name__)
outbox = None


def send_confirmation(user, site, code, number):
    message = render_to_string("phoneconfirmation/message.txt", {
        "user": user,
        "current_site": site,
        "confirm_code": code,
        "url": "http://%s%s" % (site.domain, reverse("phone_confirm", args=[code]))
    })
    send(number, message)


def send(number, message):
    from .models import SMSLog
    SEND_SMS = getattr(settings, "SMS_SEND", False)

    if isinstance(message, unicode):
        message = message.encode("utf-8")
    msg = Message(message)

    payload = {"destination": number, "body": message}

    if outbox is not None:
        # Our Nose Plugin changes outbox to a list
        outbox.append(payload)

    log = SMSLog(
        endpoint=msg.conf["end_point"],
        payload=payload,
        number=number
    )

    if SEND_SMS:
        responses = msg.send(number)
        for response in responses:
            log.pk = None
            log.mocked = False
            log.response_code = response.status_code
            log.response_body = response.text
            log.save()

            if response.status_code == 201:
                message = json.loads(response.text)
                logger.debug("We have posted a new message with sid: %s" % message["sid"])
            elif response.status_code == 400:
                details = json.loads(response.text)
                logger.error(details["message"])
            else:
                logger.error("status %s" % response.status_code)
    else:
        log.mocked = True
        log.save()

    if settings.DEBUG:
        # Log the Message
        logger.info(u"[SMS SENT%s] Payload: %s" % ("" if SEND_SMS else " (Mocked)", payload))
