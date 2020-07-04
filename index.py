from flask import (Flask, Blueprint, render_template)

bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    return render_template('test.html')
    #return render_template('index.html')