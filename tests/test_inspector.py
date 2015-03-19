import unittest
import types

from rest_framework_ccbv.inspector import Inspector, Attribute, Method
from rest_framework import generics


class TestInspector(unittest.TestCase):
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

    def test_children(self):
        self.view = 'ListModelMixin'
        self.module = 'rest_framework.mixins'
        self.inspector = Inspector(self.view, self.module)
        self.assertItemsEqual([x.__name__ for x in
                               self.inspector.get_children()],
                              ['ListCreateAPIView',
                               'ListAPIView'])


class TestMethod(unittest.TestCase):
    def setUp(self):
        class A(object):
            def method(self, *args, **kwargs):
                pass

            def method1(self, *args):
                pass

            def method2(self, **kwargs):
                pass

            def method3(self, a, b, **kwargs):
                pass

            def method4(self, a, b, *args):
                pass

            def method5(self, a, b, *args, **kwargs):
                pass

            def method6(self, a, b=3):
                pass

            def method7(self, a, b=3, *args):
                pass

            def method8(self, a=2, b=3, **kwargs):
                pass
        self.method = Method('method', A.method, A)
        self.method1 = Method('method1', A.method1, A)
        self.method2 = Method('method2', A.method2, A)
        self.method3 = Method('method3', A.method3, A)
        self.method4 = Method('method4', A.method4, A)
        self.method5 = Method('method5', A.method5, A)
        self.method6 = Method('method6', A.method6, A)
        self.method7 = Method('method7', A.method7, A)
        self.method8 = Method('method8', A.method8, A)

    def test_method(self):
        self.assertEqual(self.method.params_string(), 'self, *args, **kwargs')

    def test_method1(self):
        self.assertEqual(self.method1.params_string(), 'self, *args')

    def test_method2(self):
        self.assertEqual(self.method2.params_string(), 'self, **kwargs')

    def test_method3(self):
        self.assertEqual(self.method3.params_string(), 'self, a, b, **kwargs')

    def test_method4(self):
        self.assertEqual(self.method4.params_string(), 'self, a, b, *args')

    def test_method5(self):
        self.assertEqual(self.method5.params_string(), 'self, a, b, *args,'
                         ' **kwargs')

    def test_method6(self):
        self.assertEqual(self.method6.params_string(), 'self, a, b=3')

    def test_method7(self):
        self.assertEqual(self.method7.params_string(), 'self, a, b=3, *args')

    def test_method8(self):
        self.assertEqual(self.method8.params_string(), 'self, a=2, b=3,'
                         ' **kwargs')
