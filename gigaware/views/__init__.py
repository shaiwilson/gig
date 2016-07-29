from flask import g
from flask import request
from flask.ext.login import current_user

from gigaware import app
from gigaware import login_manager
from gigaware.models.user import User
from gigaware.views.view_helpers import redirect_to

import gigaware.views.home
import gigaware.views.login
import gigaware.views.reservations
import gigaware.views.listings
import gigaware.views.support
import gigaware.views.account
import gigaware.views.register
import gigaware.views.exchange


def should_redirect(current_user, uri_pattern):
    return (
        current_user.is_authenticated and
        uri_pattern == '/' or
        uri_pattern == '/login' or
        uri_pattern == '/register'
    )

# controller utils


@app.before_request
def before_request():
    g.user = current_user
    if should_redirect(current_user, request.url_rule):
        redirect_to('home')


@login_manager.user_loader
def load_user(id):
    try:
        return User.query.get(id)
    except:
        return None
