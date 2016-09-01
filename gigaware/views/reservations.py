import twilio

from gigaware import db, app, bcrypt
from flask import request
from flask.ext.login import current_user
from flask.ext.login import login_required

from gigaware.models.user import User
from gigaware.models.reservation import Reservation
from gigaware.models.job_task import JobTask

from gigaware.forms import ApplicationForm
from gigaware.forms import ApplicationConfirmationForm

from gigaware.views.view_helpers import view_with_params
from gigaware.views.view_helpers import redirect_to
from gigaware.views.view_helpers import twiml

import gigaware.sms

@app.route('/reservations', methods=["GET"])
@login_required
def reservations():
    user = User.query.get(current_user.get_id())

    reservations_as_host = Reservation.query.filter(
        JobTask.host_id == current_user.get_id() and
        len(JobTask.reservations) > 0
    ).join(JobTask).filter(Reservation.job_task_id == JobTask.id).all()

    reservations_as_guest = user.reservations

    return view_with_params('reservations',
                            reservations_as_guest=reservations_as_guest,
                            reservations_as_host=reservations_as_host)


@app.route('/reservations/', methods=["POST"], defaults={'property_id': None})
@app.route('/reservations/<property_id>', methods=["GET", "POST"])
@login_required
def new_reservation(property_id):
    job_task = None
    form = ApplicationForm()
    form.property_id.data = property_id

    if request.method == 'POST':
        if form.validate_on_submit():
            guest = User.query.get(current_user.get_id())
            job_task = JobTask.query.get(form.property_id.data)

            reservation = Reservation(form.message.data, job_task, guest)
            db.session.add(reservation)
            db.session.commit()

            gigaware.sms.sms_client.notify_host(reservation)

            return redirect_to('listings')

    if property_id is not None:
        job_task = JobTask.query.get(property_id)

    return view_with_params('reservation', job_task=job_task, form=form)


@app.route('/reservations/confirm', methods=["POST"])
def confirm_reservation():
    form = ApplicationConfirmationForm()
    sms_response_text = "Sorry, it looks like you don't have any reservations to respond to."

    user = User.query.filter(User.phone_number == form.From.data).first()

    reservation = Reservation.query.filter(
        Reservation.status == 'pending' and
        Reservation.job_task.host.id == User.id
    ).first()

    if reservation is None:
        return

    if 'yes' in form.Body.data or 'accept' in form.Body.data:
        reservation.confirm()
        gigaware.sms.sms_client.buy_number(user.area_code, reservation)
    else:
        reservation.reject()

    db.session.commit()

    sms_response_text = "You have successfully {0} the reservation".format(
        reservation.status)

    gigaware.sms.sms_client.notify_guest(reservation)

    return twiml(_respond_message(sms_response_text))

def _respond_message(message):
    response = twilio.twiml.Response()
    response.message(message)
    return response
