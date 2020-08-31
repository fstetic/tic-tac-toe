from flask import Blueprint, render_template

bp = Blueprint('game', __name__)
@bp.route('/play', methods=('GET', 'POST'))
def start_game():
	return render_template("template.html")