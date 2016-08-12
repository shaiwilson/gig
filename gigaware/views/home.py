from gigaware import app
from gigaware.views.view_helpers import view

from flask.ext.login import login_required


@app.route('/home', methods=["GET"])
@login_required
def home():
    return view('home')
