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
from pygments import highlight, lex
from pygments.lexers import PythonLexer
from pygments.token import Token
from .custom_formatter import CodeHtmlFormatter


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
    def __init__(self, name, value, classobject, instance_class):
        self.name = name
        self.value = value
        self.classobject = classobject
        self.instance_class = instance_class
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
        return highlight(code, PythonLexer(), CodeHtmlFormatter(self.instance_class))


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
        existing = list(filter(lambda x: x.name == value.name, self.attrs))
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

    def _is_method(self, attr):
        return isinstance(attr, (types.FunctionType, types.MethodType))

    def get_attributes(self):
        attrs = Attributes()

        for klass in self.get_klass_mro():
            for attr_str in klass.__dict__.keys():
                attr = getattr(klass, attr_str)
                if (not attr_str.startswith('__') and not self._is_method(attr)):
                    attrs.append(
                        Attribute(
                            name=attr_str,
                            value=attr,
                            classobject=klass,
                            instance_class=self.get_klass(),
                        )
                    )
        return attrs

    def get_methods(self):
        attrs = Attributes()

        for klass in self.get_klass_mro():
            for attr_str in klass.__dict__.keys():
                attr = getattr(klass, attr_str)
                if (not attr_str.startswith('__') and self._is_method(attr)):
                    attrs.append(
                        Method(
                            name=attr_str,
                            value=attr,
                            classobject=klass,
                            instance_class=self.get_klass(),
                        )
                    )
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

    def get_unavailable_methods(self):
        def next_token(tokensource, lookahead, is_looking_ahead):
            for ttype, value in tokensource:
                while lookahead and not is_looking_ahead:
                    yield lookahead.popleft()
                yield ttype, value

        def lookahed_token_from_iter(lookahead, next_token_iter):
            lookahead_token = next(next_token_iter)
            lookahead.append(lookahead_token)
            return lookahead_token

        not_implemented_methods = []
        for method in self.get_methods():
            lookahead = collections.deque()
            lookback = collections.deque()
            is_looking_ahead = False
            tokensource = lex(inspect.getsource(method.value), PythonLexer())
            next_token_iter = next_token(tokensource, lookahead, is_looking_ahead)
            for ttype, value in next_token_iter:
                lookback.append((ttype, value))
                if ttype in Token.Name and lookback[-2][1] == '.' and lookback[-3][1] == 'self':
                    if not hasattr(self.get_klass(), value):
                        is_looking_ahead = True
                        try:
                            _, la_value = lookahed_token_from_iter(lookahead, next_token_iter)
                            if la_value == '(':
                                not_implemented_methods.append(value)
                        except StopIteration:
                            pass
                        is_looking_ahead = False
        return set(not_implemented_methods)
