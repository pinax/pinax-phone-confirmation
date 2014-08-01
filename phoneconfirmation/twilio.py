import math
import requests

from django.conf import settings


MAX_MESSAGE_CHARS = settings.TWILIO_CONFIG["max_message_chars"]


class Message(object):

    def __init__(self, message, conf=settings.TWILIO_CONFIG):
        self.message = message
        self.conf = conf

        #need to break message smartly
        #only split on spaces
        #if we can't then do regular split

        #calculate how many parts we need
        #need to reduce chunk size to leave
        #space for part number
        #note: this might not work if we have
        #very large words and no spaces
        if len(message) > MAX_MESSAGE_CHARS:
            no_parts = int(math.ceil(float(len(message)) / (MAX_MESSAGE_CHARS - 10)))
            #tokenize
            words = message.split()
            if len(words) > 3:
                words_per_part = len(words) / no_parts
                self.parts = [
                    " ".join(words[i:i + words_per_part])
                    for i in range(0, no_parts * words_per_part, words_per_part)
                ]
            #to deal with unusual cases
            #which is likely to happen if we
            #have less than 4 words
            else:
                self.parts = [
                    self.message[i:i + MAX_MESSAGE_CHARS]
                    for i in range(0, len(self.message), MAX_MESSAGE_CHARS)
                ]
        else:
            self.parts = [message]

    @property
    def message_parts(self, chunk_size=MAX_MESSAGE_CHARS):
        return self.parts
        # return [
        #     self.message[i:i + chunk_size]
        #     for i in range(0, len(self.message), chunk_size)
        # ]

    def send(self, to):
        responses = []
        no_parts = len(self.message_parts)
        for i, part in enumerate(self.message_parts):
            r = requests.post(
                self.conf["end_point"],
                auth=(self.conf["account_sid"], self.conf["auth_token"]),
                data={
                    "From": self.conf["from"],
                    "To": "+%s" % to,
                    "Body": "%s\n%d/%d" % (part, i + 1, no_parts) if no_parts > 1
                    else part
                }
            )
            responses.append(r)
        return responses
