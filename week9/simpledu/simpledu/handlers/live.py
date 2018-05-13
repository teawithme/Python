from flask import Blueprint, render_template
from simpledu.models import Live
from flask_login import login_required

live = Blueprint('live', __name__, url_prefix='/live')


@live.route('/')
def index():
    live = Live.query.order_by(Live.created_at).limit(1).first()
    return render_template('live/index.html', live=live)

