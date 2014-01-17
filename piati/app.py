import simplejson

from lxml import etree

from flask import Flask, render_template, request
from flask.json import tojson_filter

from .iati import get_model
from .helpers import get_data_filepath, get_main_sectors, reverseSafeIdentifier,\
    get_rates_filepath, RATES

app = Flask(__name__)

DATA = {}


@app.route("/")
def index():
    last_projects = sorted(DATA.values(), key=lambda p: p.last_updated, reverse=True)[:5]
    active_projects = [p for p in DATA.values() if p.is_active]
    total_budget = sum(p.budget or p.total_budget for p in DATA.values())
    context = {
        "projects": list(DATA.values()),
        "last_projects": last_projects,
        "active_projects": active_projects,
        "main_sectors": get_main_sectors(DATA),
        "total_budget": total_budget,
    }
    return render_template('index.html', **context)


@app.route("/projects/<iati_identifier>/")
def show_project(iati_identifier=None):
    iati_identifier = reverseSafeIdentifier(iati_identifier)
    project_data = DATA[iati_identifier]
    return render_template('project.html', project=project_data)


@app.route("/projects/")
def show_projects():
    return render_template('projects.html', projects=list(DATA.values()))


@app.route("/about/")
def about():
    return render_template('about.html')


@app.route("/testpostfeedback/", methods=['POST'])
def test_post_feedback():
    print(request.form)
    return '{"success": true}'


@app.route("/feedback/")
def feedback():
    projects = {}
    for p in DATA.values():
        key = p.default_sector['name']
        projects[key] = projects.get(key, [])
        projects[key].append(p)
    return render_template('feedback.html', projects_by_sector=projects)


def load_data():
    for name in app.config['DATA'].keys():
        filepath = get_data_filepath(app, name)
        with open(filepath, mode="r") as f:
            # Avoid namespace pollution, useless here
            # xml = re.sub(' xmlns:\w{2}="[\w:/\.]*"', '', f.read())
            xml = f.read()
            parent = etree.fromstring(xml).find('iati-activities')
            for node in parent.findall('iati-activity'):
                project = get_model(app)(app, node)
                DATA[project.id] = project
    with open(get_rates_filepath(app)) as f:
        rates = simplejson.loads(f.read())
        RATES.update(rates['rates'])


@app.template_filter('piati_tojson')
def tojson(s):
    """Allow use of for_json method."""
    return tojson_filter(s, for_json=True)


@app.template_filter('piati_money')
def money(i, currency="€"):
    return "{:,} {currency}".format(
        int(i), currency=currency).replace(",", " ")


@app.template_filter('piati_timestamp')
def timestamp(d):
    return int(d.timestamp() * 1000)


@app.template_filter('piati_colclass')
def colclass(i):
    classes = {
        1: "wide",
        2: "half",
        3: "third",
        4: "quarter"
    }
    return classes.get(i)
