import yaml
import os
import inspect

current_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
main_yaml = current_dir + '/resource/main.yml'
conf = yaml.load(open(main_yaml))
