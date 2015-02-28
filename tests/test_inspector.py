import unittest
import types

from inspector import Inspector
from rest_framework import generics


class TestOne(unittest.TestCase):
    def setUp(self):
        self.view = 'CreateAPIView'
        self.inspector = Inspector(self.view)

    def test_get_view(self):
        self.assertEquals(self.inspector.get_view(),
                          getattr(generics, self.view))

    def test_first_ancestor_is_itself(self):
        self.assertEquals(self.inspector.get_ancestors()[0], self.view)

    def test_ancestor(self):
        self.assertEquals(self.inspector.get_ancestors(),
                          [self.view, 'CreateModelMixin',
                          'GenericAPIView', 'APIView', 'View'])

    def test_attributes(self):
        self.assertIn('allowed_methods', self.inspector.get_attributes())
        for attr in self.inspector.get_attributes():
            self.assertFalse(attr.startswith('_'))
            self.assertFalse(isinstance(self.inspector.get_attributes()[attr],
                             types.MethodType))
