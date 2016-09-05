import os

import yaml

project_dir = os.path.dirname(os.path.dirname(__file__))
resource_dir = project_dir + '/resource'


def get_resource_path(name):
    return resource_dir + '/' + name


main_yaml = get_resource_path('main.yml')
conf = yaml.load(open(main_yaml))
