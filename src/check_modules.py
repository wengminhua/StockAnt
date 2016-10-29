# coding:utf-8
import os
from utils import reflect
from stock_ant import StockAnt as ant


def load_modules(module_paths):
    for module_path in module_paths:
        reflect.get_module(module_path)


def scan_modules(path):
    module_paths = []
    if not os.path.isdir(path):
        return module_paths
    os.listdir(path)

if __name__ == '__main__':
    load_modules(["quant.BIAS"])
    print(ant.get_methods())
