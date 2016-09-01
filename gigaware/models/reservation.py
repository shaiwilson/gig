from gigaware.models import app_db, auth_token, account_sid, phone_number, application_sid
from flask import render_template
from twilio.rest import TwilioRestClient

db = app_db()


class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    message = db.Column(db.String, nullable=False)
    status = db.Column(
        db.Enum(
            'pending',
            'confirmed',
            'rejected',
            name='reservation_status_enum'),
        default='pending')
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
