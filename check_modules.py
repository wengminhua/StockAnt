# coding:utf-8
import os
import sys
import json

from utils.stock_ant import StockAnt as ant
from utils import reflect
from flask import jsonify


def load_modules(module_paths):
    for module_path in module_paths:
        reflect.get_module(module_path)


def scan_modules(path):
    module_paths = []
    if not os.path.isdir(path):
        return module_paths
    os.listdir(path)


def output_modules(path, output_filename):
    print path
    print output_filename
    load_modules(path)
    file = open(output_filename, "w")
    file.write(jsonify(ant.get_methods()))
    file.close()


if __name__ == '__main__':
    sys.path.append('./')
    module_paths = sys.argv[1].split(',')
    output_filename = sys.argv[2]
    load_modules(module_paths)
    file = open(output_filename, "w")
    file.write(json.dumps(ant.get_methods()))
    file.close()
