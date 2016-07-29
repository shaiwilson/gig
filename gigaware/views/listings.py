from gigaware import app
from gigaware import db

from gigaware.forms import JobListingForm
from gigaware.models.job_task import JobTask
from gigaware.models.user import User

from gigaware.views.view_helpers import redirect_to
from gigaware.views.view_helpers import view_with_params
from gigaware.views.view_helpers import view

from flask import request
from flask.ext.login import login_required
from flask.ext.login import current_user


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

            new_task = JobTask(
                form.description.data,
                form.image_url.data,
                form.city.data,
                form.country.data,
                form.zip_code.data,
                form.details.data,
                form.price.data,
                form.currency.data,
                host)
            db.session.add(new_task)
            db.session.commit()
            return redirect_to('listings')

    return view('listings_new', form)
