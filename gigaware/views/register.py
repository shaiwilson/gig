from gigaware import app
from gigaware import db

from gigaware.forms import RegisterForm
from gigaware.models.user import User
from gigaware.views.view_helpers import view
from gigaware.views.view_helpers import redirect_to

from flask import request
from flask.ext.login import login_user


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
