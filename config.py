import os
import pathlib


base_path = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
base_dir = os.path.dirname(os.path.abspath(base_path)) 


# Directory settings
VIEWS_DIR = os.path.join(base_path, 'views/')
STATIC_FILE_DIR = os.path.join(VIEWS_DIR, 'static/')
DATA_DIR = os.path.join(base_path, 'data/')
CONFIG_DIR = os.path.join(DATA_DIR, 'config/')
SAVES_DIR = os.path.join(DATA_DIR, 'saves/')
