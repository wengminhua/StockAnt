import sys
import types


def _get_mod(module_path):
    try:
        mod = sys.modules[module_path]
        if not isinstance(mod, types.ModuleType):
            raise KeyError
    except KeyError:
        mod = __import__(module_path, globals(), locals(), [''])
        sys.modules[module_path] = mod
    return mod


def _get_func(full_func_name):
    last_dot = full_func_name.rfind(u'.')
    func_name = full_func_name[last_dot + 1:]
    mod_path = full_func_name[:last_dot]
    mod = _get_mod(mod_path)
    func = getattr(mod, func_name)
    assert callable(func), u'%s is not callable' % full_func_name
    return func


def applyFunc(full_func_name, args_dict):
    func = _get_func(full_func_name)
    return apply(func, (), args_dict)