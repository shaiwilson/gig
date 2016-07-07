from gigaware.models import app_db, auth_token, account_sid, phone_number, application_sid
from flask import render_template
from twilio.rest import TwilioRestClient

db = app_db()


class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String, nullable=False)
    status = db.Column(db.Enum('pending', 'confirmed', 'rejected', name='reservation_status_enum'), default='pending')
    anonymous_phone_number = db.Column(db.String, nullable=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    job_task_id = db.Column(db.Integer, db.ForeignKey('job_listings.id'))
    guest = db.relationship("User", back_populates="reservations")
    job_task = db.relationship("JobTask", back_populates="reservations")

    def __init__(self, message, job_task, guest):
        self.message = message
        self.guest = guest
        self.job_task = job_task
        self.status = 'pending'

    def confirm(self):
        self.status = 'confirmed'

    def reject(self):
        self.status = 'rejected'

    def __repr__(self):
        return '<Application {0}>'.format(self.id)

    def notify_host(self):
        self._send_message(self.job_task.host.phone_number,
                           render_template('messages/sms_host.txt',
                                           name=self.guest.name,
                                           description=self.job_task.description,
                                           message=self.message))

    def notify_guest(self):
        self._send_message(self.guest.phone_number,
                           render_template('messages/sms_guest.txt',
                                           description=self.job_task.description,
                                           status=self.status))

    def buy_number(self, area_code):
        numbers = self._get_twilio_client().phone_numbers.search(country="US",
                                                                 type="local",
                                                                 area_code=area_code,
                                                                 sms_enabled=True,
                                                                 voice_enabled=True)

        if numbers:
            number = self._purchase_number(numbers[0])
            self.anonymous_phone_number = number
            return number
        else:
            numbers = self._get_twilio_client().phone_numbers.search(country="US",
                                                                     type="local",
                                                                     sms_enabled=True,
                                                                     voice_enabled=True)

            if numbers:
                number = self._purchase_number(numbers[0])
                self.anonymous_phone_number = number
                return number

        return None

    def _purchase_number(self, number):
        return number.purchase(sms_application_sid=application_sid(),
                               voice_application_sid=application_sid()).phone_number

    def _get_twilio_client(self):
        return TwilioRestClient(account_sid(), auth_token())

    def _send_message(self, to, message):
        self._get_twilio_client().messages.create(
                to=to,
                from_=phone_number(),
                body=message)
