from gigaware import db, bcrypt, app, login_manager
from flask import session, g, request, flash, Blueprint, render_template, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
import twilio.twiml

from gigaware.forms import RegisterForm, LoginForm, JobListingForm, ApplicationForm, \
    ApplicationConfirmationForm, ExchangeForm, VerifyForm
from gigaware.view_helpers import twiml, view, redirect_to, view_with_params
from gigaware.models import init_models_module

init_models_module(db, bcrypt, app)

# from authy import AuthyApiException
# from gigaware.utils import create_user, send_authy_token_request, verify_authy_token
# from gigaware.decorators import login_required, verify_authy_request

from gigaware.models.user import User
from gigaware.models.job_task import JobTask
from gigaware.models.reservation import Reservation


@app.route('/', methods=["GET", "POST"])
@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():

            if User.query.filter(User.email == form.email.data).count() > 0:
                form.email.errors.append("Email address already in use.")
                return view('register', form)

            user = User(
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    password=form.password.data,
                    phone_number="+{0}{1}".format(form.country_code.data, form.phone_number.data),
                    area_code=str(form.phone_number.data)[0:3],
                    zip_code=form.zip_code.data)

            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)

            return redirect_to('home')
        else:
            return view('register', form)

    return view('register', form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """
    Powers the main login form.
    """
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            candidate_user = User.query.filter(User.email == form.email.data).first()

            if candidate_user is None or not bcrypt.check_password_hash(candidate_user.password,
                                                                        form.password.data):
                form.password.errors.append("Invalid credentials.")
                return view('login', form)

            login_user(candidate_user, remember=True)
            return redirect_to('home')
    return view('login', form)


@app.route('/logout', methods=["POST"])
@login_required
def logout():
    """Log out a user, clearing their session variables"""
    session.pop('user_id', None)

    logout_user()
    return redirect_to('home')


@app.route('/home', methods=["GET"])
@login_required
def home():
    return view('home')

@app.route('/account', methods=["GET"])
@login_required
def account():
    user = User.query.get(session['user_id'])
    return view_with_params('account', user=user)


@app.route('/support', methods=["GET"])
def support():
    return view('support')


@app.route('/listings', methods=["GET"])
@login_required
def listings():
    job_listings = JobTask.query.all()
    return view_with_params('listings', job_listings=job_listings)


@app.route('/listings/new', methods=["GET", "POST"])
@login_required
def new_property():
    form = JobListingForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            host = User.query.get(current_user.get_id())

            new_task = JobTask(form.description.data, form.image_url.data,
            form.city.data, form.country.data, form.zip_code.data,
            form.details.data, form.price.data, form.currency.data, host)
            db.session.add(new_task)
            db.session.commit()
            return redirect_to('listings')

    return view('listings_new', form)


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

            reservation.notify_host()

            return redirect_to('listings')

    if property_id is not None:
        job_task = JobTask.query.get(property_id)

    return view_with_params('reservation', job_task=job_task, form=form)


@app.route('/reservations', methods=["GET"])
@login_required
def reservations():
    user = User.query.get(current_user.get_id())

    reservations_as_host = Reservation.query \
        .filter(JobTask.host_id == current_user.get_id() and len(JobTask.reservations) > 0) \
        .join(JobTask) \
        .filter(Reservation.job_task_id == JobTask.id) \
        .all()

    reservations_as_guest = user.reservations

    return view_with_params('reservations',
                            reservations_as_guest=reservations_as_guest,
                            reservations_as_host=reservations_as_host)


@app.route('/reservations/confirm', methods=["POST"])
def confirm_reservation():
    form = ApplicationConfirmationForm()
    sms_response_text = "Sorry, it looks like you don't have any reservations to respond to."

    user = User.query.filter(User.phone_number == form.From.data).first()
    reservation = Reservation \
        .query \
        .filter(Reservation.status == 'pending'
                and Reservation.job_task.host.id == user.id) \
        .first()

    if reservation is not None:

        if 'yes' in form.Body.data or 'accept' in form.Body.data:
            reservation.confirm()
            reservation.buy_number(user.area_code)
        else:
            reservation.reject()

        db.session.commit()

        sms_response_text = "You have successfully {0} the reservation".format(reservation.status)
        reservation.notify_guest()

    return twiml(_respond_message(sms_response_text))


@app.route('/exchange/sms', methods=["POST"])
def exchange_sms():
    form = ExchangeForm()

    outgoing_number = _gather_outgoing_phone_number(form.From.data, form.To.data)

    response = twilio.twiml.Response()
    response.addSms(form.Body.data, to=outgoing_number)
    return twiml(response)


@app.route('/exchange/voice', methods=["POST"])
def exchange_voice():
    form = ExchangeForm()

    outgoing_number = _gather_outgoing_phone_number(form.From.data, form.To.data)

    response = twilio.twiml.Response()
    response.addPlay("http://howtodocs.s3.amazonaws.com/howdy-tng.mp3")
    response.addDial(outgoing_number)
    return twiml(response)

# controller utils
@app.before_request
def before_request():

    g.user = current_user
    uri_pattern = request.url_rule
    if current_user.is_authenticated and (
                        uri_pattern == '/' or uri_pattern == '/login' or uri_pattern == '/register'):
        redirect_to('home')


@login_manager.user_loader
def load_user(id):
    try:
        return User.query.get(id)
    except:
        return None


def _gather_outgoing_phone_number(incoming_phone_number, anonymous_phone_number):
    reservation = Reservation.query \
        .filter(Reservation.anonymous_phone_number == anonymous_phone_number) \
        .first()

    if reservation.guest.phone_number == incoming_phone_number:
        return reservation.job_task.host.phone_number

    return reservation.guest.phone_number


def _respond_message(message):
    response = twilio.twiml.Response()
    response.message(message)
    return response
