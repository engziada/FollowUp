import datetime
from flask import  render_template, request
from apps.home import blueprint
from flask_login import login_required
from jinja2 import TemplateNotFound

from apps.home.models import Log
from apps.home.util import get_summerized_report

from icecream import ic


@blueprint.route('/index')
@login_required
def index():
    statistics = get_summerized_report()
    return render_template('home/index.html', segment='index', stats=statistics)


@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:
        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):
    try:
        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None


#////////////////////////////////////////////////////////////////////////////////////////

@blueprint.route("/log", methods=["GET", "POST"])
@login_required
def log():
    page = request.args.get("page", 1, type=int)
    per_page = 50  # Number of logs per page

    from_date = request.args.get("from_date", datetime.date.min)
    to_date = request.args.get("to_date", datetime.date.max)
    from_date=from_date if from_date else datetime.date.min
    to_date=to_date if to_date else datetime.date.max

    logs = (
        Log.query.filter(Log.creation_date >= from_date, Log.creation_date <= to_date)
        .order_by(Log.creation_date.desc())
        .order_by(Log.creation_time.desc())
        .paginate(page=page, per_page=per_page)
    )

    return render_template("home/log.html", logs=logs, from_date=from_date, to_date=to_date)

# ////////////////////////////////////////////////////////////////////////////////////////
