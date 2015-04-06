import types
import collections
import inspect
import json

from rest_framework import generics
from rest_framework import views as rest_views
from rest_framework.compat import View
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


def add_to_views_if_its_restframework(views, klass):
    if not klass.__module__.startswith('rest_framework'):
        return
    views[klass.__module__ + '.' + klass.__name__] = klass


def get_views():
    modules = [rest_views, generics]
    views = {}

    for module in modules:
        for attr_str in dir(module):
            is_subclass = False
            attr = getattr(module, attr_str)
            try:
                is_subclass = issubclass(attr, View)
            except TypeError:
                pass
            if not attr_str.startswith('_') and is_subclass:
                add_to_views_if_its_restframework(views, attr)
                for klass in attr.mro():
                    add_to_views_if_its_restframework(views, klass)
    return views
drfviews = get_views()


class Attribute(object):
    def __init__(self, name, value, classobject):
        self.name = name
        self.value = value
        self.classobject = classobject
        self.dirty = False

    def __eq__(self, obj):
        return self.name == obj.name and self.value == obj.value

    def __neq__(self, obj):
        return not self.__eq__(obj)


class Method(Attribute):
    def __init__(self, *args, **kwargs):
        super(Method, self).__init__(*args, **kwargs)
        self.children = []

    def params_string(self):
        stack = []
        argspec = inspect.getargspec(self.value)
        if argspec.keywords:
            stack.insert(0, '**' + argspec.keywords)
        if argspec.varargs:
            stack.insert(0, '*' + argspec.varargs)
        defaults = list(argspec.defaults or [])
        for arg in argspec.args[::-1]:
            if defaults:
                default = defaults.pop()
                stack.insert(0, '{}={}'.format(arg, default))
            else:
                stack.insert(0, arg)
        return ', '.join(stack)

    def code(self):
        code = inspect.getsource(self.value)
        return highlight(code, PythonLexer(), HtmlFormatter())


class Attributes(collections.MutableSequence):
    # Attributes must be added following mro order
    def __init__(self):
        self.attrs = []

    def __getitem__(self, key):
        return self.attrs[key]

    def __setitem__(self, key, value):
        if key < len(self.attrs) or not isinstance(key, int):
            raise ValueError("Can't change value of position")
        if not isinstance(value, Attribute):
            raise TypeError('Can only hold Attributes')
        # find attributes higher in the mro
        # PS: methods can't be dirty, because they don't necessarily override
        existing = filter(lambda x: x.name == value.name, self.attrs)
        if existing and not isinstance(value, Method):
            value.dirty = True
        elif existing:
            existing[-1].children.append(value)
            return
        self.attrs.append(value)
        self.attrs.sort(key=lambda x: x.name)

    def __delitem__(self, key):
        del self.attrs[key]

    def __len__(self):
        return len(self.attrs)

    def insert(self, i, x):
        self.__setitem__(i, x)


class Inspector(object):
    def __init__(self, view_name, module_name):
        self.view_name = view_name
        self.module_name = module_name

    def get_view(self):
        return drfviews[self.module_name + '.' + self.view_name]

    def get_views_mro(self):
        ancestors = []
        for ancestor in self.get_view().mro():
            if ancestor is object:
                break
            ancestors.append(ancestor)
        return ancestors

    def get_children(self):
        children = []
        for view in drfviews.values():
            if issubclass(view, self.get_view()) and view != self.get_view():
                children.append(view)
        return children

    def get_attributes(self):
        attrs = Attributes()

        for view in self.get_views_mro():
            for attr_str in view.__dict__.keys():
                attr = getattr(view, attr_str)
                if (not attr_str.startswith('__') and
                        not isinstance(attr, types.MethodType)):
                    attrs.append(Attribute(name=attr_str, value=attr,
                                           classobject=view))
        return attrs

    def get_methods(self):
        attrs = Attributes()

        for view in self.get_views_mro():
            for attr_str in view.__dict__.keys():
                attr = getattr(view, attr_str)
                if (not attr_str.startswith('__') and
                        isinstance(attr, types.MethodType)):
                    attrs.append(Method(name=attr_str,
                                 value=attr,
                                 classobject=view))
        return attrs

    def get_available_versions(self):
        with open('.views.json', 'r') as f:
            views_versions = json.loads(f.read())
        
        return [version
            for version in views_versions 
            if self.view_name in views_versions[version][self.module_name]]
