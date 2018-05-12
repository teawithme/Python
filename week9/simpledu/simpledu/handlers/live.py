from flask import Blueprint, render_template
from simpledu.models import Live
from flask_login import login_required

live = Blueprint('live', __name__, url_prefix='/live')


@live.route('/<int:live_id>')
@login_required
def index(live_id):
    live = Live.query.get_or_404(live_id)
    return render_template('live/index.html', live=live)

