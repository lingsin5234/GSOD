# this custom file is to house global functions across all my django apps
import os
from .settings import BASE_DIR


# calling the correct template page from its corresponding app - and not the first one listed
# especially if they have the same html name, e.g. project.html
def get_this_template(app_name, page_name):

    template_location = os.path.join(BASE_DIR, app_name, 'templates', 'pages', page_name)

    return template_location
