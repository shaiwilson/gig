from flask import session
from flask import request

from flask.ext.login import login_user

from gigaware import app
from gigaware import bcrypt
from gigaware.forms import LoginForm
from gigaware.models.user import User
from gigaware.views.view_helpers import redirect_to
from gigaware.views.view_helpers import view


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Powers the main login form.
    """
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            candidate_user = User.query.filter(
                User.email == form.email.data).first()

            if candidate_user is None or not bcrypt.check_password_hash(
                    candidate_user.password, form.password.data):
                form.password.errors.append("Invalid credentials.")
                return view('login', form)

            elif candidate_user is not None and \
                    bcrypt.check_password_hash(candidate_user.password, form.password.data):
                session['user_id'] = User.id
                login_user(candidate_user, remember=True)
                return redirect_to('home')
    return view('login', form)
