import types
import collections
import inspect
import json

from rest_framework import generics
from rest_framework import views as rest_views
try:
    from rest_framework import viewsets
except ImportError:
    viewsets = None
from rest_framework.compat import View
from rest_framework import serializers
from rest_framework.serializers import BaseSerializer
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


def add_to_klasses_if_its_restframework(klasses, klass):
    if not klass.__module__.startswith('rest_framework'):
        return
    klasses[klass.__module__ + '.' + klass.__name__] = klass


def get_klasses():
    modules = [rest_views, generics, serializers]

    if viewsets is not None:
        modules.append(viewsets)
    klasses = {}

    for module in modules:
        for attr_str in dir(module):
            is_subclass = False
            attr = getattr(module, attr_str)
            try:
                is_subclass = (issubclass(attr, View) or
                               issubclass(attr, BaseSerializer))
            except TypeError:
                pass
            if not attr_str.startswith('_') and is_subclass:
                add_to_klasses_if_its_restframework(klasses, attr)
                for klass in attr.mro():
                    add_to_klasses_if_its_restframework(klasses, klass)
    return klasses
drfklasses = get_klasses()


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
        existing = filter(lambda x: x.name == value.name, self.attrs)
        # methods can't be dirty, because they don't necessarily override
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
    def __init__(self, klass_name, module_name):
        self.klass_name = klass_name
        self.module_name = module_name

    def get_klass(self):
        return drfklasses[self.module_name + '.' + self.klass_name]

    def get_klass_mro(self):
        ancestors = []
        for ancestor in self.get_klass().mro():
            if ancestor is object:
                break
            ancestors.append(ancestor)
        return ancestors

    def get_children(self):
        children = []
        for klass in drfklasses.values():
            if (issubclass(klass, self.get_klass()) and
                    klass != self.get_klass()):
                children.append(klass)
        return children

    def get_attributes(self):
        attrs = Attributes()

        for klass in self.get_klass_mro():
            for attr_str in klass.__dict__.keys():
                attr = getattr(klass, attr_str)
                if (not attr_str.startswith('__') and
                        not isinstance(attr, types.MethodType)):
                    attrs.append(Attribute(name=attr_str, value=attr,
                                           classobject=klass))
        return attrs

    def get_methods(self):
        attrs = Attributes()

        for klass in self.get_klass_mro():
            for attr_str in klass.__dict__.keys():
                attr = getattr(klass, attr_str)
                if (not attr_str.startswith('__') and
                        isinstance(attr, types.MethodType)):
                    attrs.append(Method(name=attr_str,
                                 value=attr,
                                 classobject=klass))
        return attrs

    def get_direct_ancestors(self):
        klass = self.get_klass()
        return klass.__bases__

    def get_available_versions(self):
        with open('.klasses.json', 'r') as f:
            klass_versions = json.loads(f.read())

        return [
            version
            for version in klass_versions
            if self.module_name in klass_versions[version] and
            self.klass_name in klass_versions[version][self.module_name]]
