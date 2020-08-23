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
    service_dir = './%s/%s' % (JSON_STORAGE_DIR, service)
    print('[fileHandler] deleting dir: %s' % service_dir)
    shutil.rmtree(service_dir)


def get_file_name(path):
    full_path = path.split('/')
    return full_path[-1]


def remove_file(file_path):
    print('[fileHandler] deleting file: %s' % file_path)
    os.remove(file_path)
    path_dir = file_path.replace(get_file_name(file_path), "")
    _remove_route_dir_if_needed(path_dir)


def _remove_route_dir_if_needed(path_dir):
    if len(os.listdir(path_dir)) == 0:
        route_dir = _extract_route_dir(path_dir)

        if route_dir is not None:
            print('[fileHandler] deleting dir: %s' % route_dir)
            shutil.rmtree(route_dir)


def _extract_route_dir(response_path):
    dir_list = response_path.replace('.', '')
    dir_list = dir_list.split('/')
    dir_list = list(filter(('').__ne__, dir_list))

    if dir_list[0] == JSON_STORAGE_DIR:
        last_dir = response_path.replace(dir_list[-1], '')
        last_dir = last_dir.replace('//', '/')
        return last_dir
    return None
