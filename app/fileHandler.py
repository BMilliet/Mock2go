import os
import shutil
from werkzeug.utils import secure_filename

JSON_STORAGE_DIR = "jsonMock"


def save_file_on_path(full_path, file):
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    file.save(os.path.join(full_path))


def build_file_path(service, route, file_name):
    clean_route = route.replace('/PARAMETER', '')
    file_name_edit = secure_filename(file_name)
    file_path = './%s/%s/%s/%s' % (JSON_STORAGE_DIR,
                                   service,
                                   clean_route,
                                   file_name_edit)
    return file_path

def delete_service(service):
    shutil.rmtree('./%s/%s' % (JSON_STORAGE_DIR, service))


def get_file_name(path):
    full_path = path.split('/')
    return full_path[-1]


def remove_file(file_path):
    os.remove(file_path)
    # path_dir = file_path.replace(get_file_name(file_path), "")
    # if len(os.listdir(path_dir)) == 0:
    #     os.remove(path_dir)
