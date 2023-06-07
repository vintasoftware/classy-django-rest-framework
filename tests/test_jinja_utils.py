import unittest
import inspect

from django.views.generic import DetailView
from rest_framework.generics import ListAPIView

from rest_framework_ccbv.jinja_utils import template_env
from rest_framework_ccbv.config import EXACT_VERSION


class TestJinjaUtils(unittest.TestCase):
    def get_context_function(self, name):
        return template_env.globals[name]

    def test_get_klass_url_with_django_view(self):
        get_klass_url = self.get_context_function("get_klass_url")
        assert get_klass_url({}, DetailView) == "https://ccbv.co.uk/DetailView"

    def test_get_klass_url_with_drf_view(self):
        get_klass_url = self.get_context_function("get_klass_url")
        assert (
            get_klass_url({}, ListAPIView, 0.1)
            == "/0.1/rest_framework.generics/ListAPIView.html"
        )

    def test_get_version_url_without_klass(self):
        get_version_url = self.get_context_function("get_version_url")
        assert get_version_url({}, 0.1) == "/0.1/index.html"

    def test_get_version_url_with_klass(self):
        get_version_url = self.get_context_function("get_version_url")
        assert (
            get_version_url({"this_klass": ListAPIView}, 0.1)
            == "/0.1/rest_framework.generics/ListAPIView.html"
        )

    def test_get_klass_docs(self):
        get_klass_docs = self.get_context_function("get_klass_docs")
        assert get_klass_docs({}, ListAPIView.__doc__.strip())

    def test_get_doc_link(self):
        get_doc_link = self.get_context_function("get_doc_link")
        assert (
            get_doc_link({}, ListAPIView)
            == "https://www.django-rest-framework.org/api-guide/generic-views#listapiview"
        )

    def test_get_src_link(self):
        get_src_link = self.get_context_function("get_src_link")
        lineno = str(inspect.getsourcelines(ListAPIView)[-1])
        assert get_src_link({}, ListAPIView) == (
            "https://github.com/tomchristie/django-rest-framework/blob/"
            + EXACT_VERSION
            + "/rest_framework/generics.py#L"
            + lineno
        )
