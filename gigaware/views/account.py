from gigaware import app
from flask.ext.login import login_required
from flask import session

from gigaware.models.user import User
from gigaware.views.view_helpers import view_with_params


@app.route('/account', methods=["GET"])
@login_required
def account():
    user = User.query.get(session['user_id'])
    return view_with_params('account', user=user)
