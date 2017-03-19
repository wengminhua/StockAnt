# coding:utf-8
import sys
import types


def get_module(module_path):
    try:
        module = sys.modules[module_path]
        if not isinstance(module, types.ModuleType):
            raise KeyError
    except KeyError:
        module = __import__(module_path, globals(), locals(), [''])
        sys.modules[module_path] = module
    return module


def get_func(full_func_name):
    last_dot = full_func_name.rfind(u'.')
    func_name = full_func_name[last_dot + 1:]
    module_path = full_func_name[:last_dot]
    module = get_module(module_path)
    func = getattr(module, func_name)
    assert callable(func), u'%s is not callable' % full_func_name
    return func


def apply_func(full_func_name, args_dict):
    func = get_func(full_func_name)
    return apply(func, (), args_dict)