# coding:utf-8
import inspect


class StockAnt:
    __methods = []

    def __init__(self):
        return

    @classmethod
    def register(cls, **options):
        def decorator(func):
            module_name = inspect.getmodule(func).__name__
            method_name = func.__name__
            step = options['step']
            arg_names = inspect.getargspec(func)[0]
            arg_types = options['types']
            cls.__add_method(module_name, method_name, step, arg_names, arg_types)
            return func
        return decorator


    @classmethod
    def __add_method(cls, module_name, method_name, step, arg_names, arg_types):
        one_method = dict()
        one_method['name'] = method_name
        one_method['module'] = module_name
        one_method['step'] = step
        one_method['args'] = []
        for i in range(0, len(arg_names)):
            one_arg = dict()
            one_arg['name'] = arg_names[i]
            one_arg['type'] = arg_types[i]
            one_method['args'].append(one_arg)
        cls.__methods.append(one_method)

    @classmethod
    def get_methods(cls):
        return cls.__methods
