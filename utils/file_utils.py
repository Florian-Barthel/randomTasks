import uuid
import os
import shutil


def create_id_if_none(id):
    if id is None:
        return str(uuid.uuid1().hex)
    else:
        return id


def create_path_if_not_exists(path):
    if not os.path.isdir(path):
        os.mkdir(path)
    return path


def reset_dir(path):
    shutil.rmtree(path)
    os.mkdir(path)
