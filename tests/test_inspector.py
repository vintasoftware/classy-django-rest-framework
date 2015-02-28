import unittest
import types

from rest_framework_ccbv.inspector import Inspector
from rest_framework import generics

from rest_framework_ccbv.inspector import Attribute


class TestOne(unittest.TestCase):
    def setUp(self):
        self.view = 'GenericAPIView'
        self.module = 'rest_framework.generics'
        self.inspector = Inspector(self.view, self.module)

    def test_get_view(self):
        self.assertEquals(self.inspector.get_view(),
                          getattr(generics, self.view))

    def test_first_ancestor_is_itself(self):
        self.assertEquals(self.inspector.get_views_mro()[0].__name__, self.view)

    def test_ancestor(self):
        self.assertEquals([x.__name__ for x in self.inspector.get_views_mro()],
                          [self.view, 'APIView', 'View'])

    def test_attributes(self):
        self.assertIn(Attribute(name='serializer_class',
                                value=None,
                                classobject=None),
                      self.inspector.get_attributes())
        for attr in self.inspector.get_attributes():
            self.assertFalse(attr.name.startswith('_'))
            self.assertFalse(isinstance(attr, types.MethodType))
