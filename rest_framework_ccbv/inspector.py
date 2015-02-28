import types

from rest_framework import generics
from rest_framework.compat import View


def get_views():
    modules = [generics]
    views = {}

    for module_str in modules:
        for attr in dir(module_str):
            is_subclass = False
            module = getattr(module_str, attr)
            try:
                is_subclass = issubclass(module, View)
            except TypeError:
                pass
            if not attr.startswith('_') and is_subclass:
                views[attr] = getattr(module_str, attr)
    return views
drfviews = get_views()


class Inspector(object):

    def __init__(self, view_name):
        self.view_name = view_name

    def get_view(self):
        return drfviews[self.view_name]

    def get_ancestors(self):
        ancestors = []
        for ancestor in self.get_view().mro():
            if ancestor is object:
                break
            ancestors.append(ancestor.__name__)
        return ancestors

    def get_attributes(self):
        attrs = {}
        for attr_str in dir(self.get_view()):
            attr = getattr(self.get_view(), attr_str)
            if (not attr_str.startswith('_') and
                    not isinstance(attr, types.MethodType)):
                attrs[attr_str] = attr
        return attrs
