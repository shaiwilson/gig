from gigaware import app
from gigaware.views.view_helpers import view


@app.route('/support', methods=["GET"])
def support():
    return view('support')
