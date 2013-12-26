import os

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir))
FREEZER_RELATIVE_URLS = True
FREEZER_DESTINATION = os.path.join(PROJECT_DIR, 'build')
DATA = {
    "NL": "http://iati-datastore.herokuapp.com/api/1/access/activity.xml?reporting-org=NL-1&recipient-country=ML"
}
DATA_DIR = os.path.join(PROJECT_DIR, "data")
DEFAULT_MAP_CENTER = [15, -5]
DEFAULT_MAP_ZOOM = 6
SITE_NAME = "L'aide française au Mali"
SITE_BASELINE = "Suivez l'aide au développement au Mali."
