import os
import json
from helpers.yolo_csv import YoloCSV
from helpers.yolo_tree import YoloTree

"""
Doc Doc Doc
"""


def get_source_files():

    return [{"label": v, "value": v} for v in os.listdir("data")]


def get_valid_trap_num_from_children(children):

    c_json = json.loads(children)

    return [{"label": v, "value": v} for v in c_json["valid_trap_nums"]]


def load_source_file(file_name):

    return YoloCSV("data/{}".format(file_name))
