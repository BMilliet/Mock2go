import os
import json


def loadJson(file_path):
    with open(file_path) as f:
        return json.loads(f.read())
