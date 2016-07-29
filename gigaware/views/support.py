from gigaware import app
from flask import session

from flask.ext.login import login_required
from flask.ext.login import logout_user
from gigaware.views.view_helpers import redirect_to


@app.route('/logout', methods=["POST"])
@login_required
def logout():
    """Log out a user, clearing their session variables"""
    session.pop('user_id', None)

    logout_user()
    return redirect_to('home')
