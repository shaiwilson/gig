import twilio

from gigaware import app
from gigaware.forms import ExchangeForm
from gigaware.models.reservation import Reservation

from gigaware.views.view_helpers import twiml
from gigaware.models.reservation import Reservation


@app.route('/exchange/sms', methods=["POST"])
def exchange_sms():
    form = ExchangeForm()

    outgoing_number = _gather_outgoing_phone_number(
        form.From.data, form.To.data)

    response = twilio.twiml.Response()
    response.addSms(form.Body.data, to=outgoing_number)
    return twiml(response)


@app.route('/exchange/voice', methods=["POST"])
def exchange_voice():
    form = ExchangeForm()

    outgoing_number = _gather_outgoing_phone_number(
        form.From.data, form.To.data)

    response = twilio.twiml.Response()
    response.addPlay("http://howtodocs.s3.amazonaws.com/howdy-tng.mp3")
    response.addDial(outgoing_number)
    return twiml(response)


def _gather_outgoing_phone_number(
        incoming_phone_number,
        anonymous_phone_number):
    reservation = Reservation.query \
        .filter(Reservation.anonymous_phone_number == anonymous_phone_number) \
        .first()

    if reservation.guest.phone_number == incoming_phone_number:
        return reservation.job_task.host.phone_number

    return reservation.guest.phone_number
