from flask import render_template
from gigaware.models import auth_token
from gigaware.models import account_sid
from gigaware.models import application_sid
from gigaware.models import phone_number
from twilio.rest import TwilioRestClient


class TwilioClient(object):
    @property
    def twilio_client(self):
        return TwilioRestClient(account_sid(), auth_token())

    def notify_host(self, reservation):
        self._send_message(
            reservation.job_task.host.phone_number,
            render_template(
                'messages/sms_host.txt',
                name=reservation.guest.first_name,
                description=reservation.job_task.description,
                message=reservation.message))

    def notify_guest(self, reservation):
        self._send_message(
            reservation.guest.phone_number,
            render_template(
                'messages/sms_guest.txt',
                description=reservation.job_task.description,
                status=reservation.status))

    def buy_number(self, area_code, reservation):
        numbers = self.twilio_client.phone_numbers.search(
            country="US",
            type="local",
            area_code=area_code,
            sms_enabled=True,
            voice_enabled=True
        )

        if numbers:
            number = self._purchase_number(numbers[0])
            reservation.anonymous_phone_number = number
            return number
        else:
            numbers = self.twilio_client.phone_numbers.search(
                country="US", type="local", sms_enabled=True, voice_enabled=True)

            if numbers:
                number = self._purchase_number(numbers[0])
                reservation.anonymous_phone_number = number
                return number

        return None

    def _purchase_number(self, number):
        return number.purchase(
            sms_application_sid=application_sid(),
            voice_application_sid=application_sid()).phone_number

    def _send_message(self, to, message):
        self.twilio_client.messages.create(
            to=to,
            from_=phone_number(),
            body=message
        )
