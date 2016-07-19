import unittest

from mock import mock_open, patch
from rest_framework.generics import ListAPIView

from rest_framework_ccbv.renderers import (
    BasePageRenderer, IndexPageRenderer, LandPageRenderer, ErrorPageRenderer,
    SitemapRenderer,
)


class TestBasePageRenderer(unittest.TestCase):
    def setUp(self):
        self.renderer = BasePageRenderer([ListAPIView])
        self.renderer.template_name = 'base.html'

    @patch('rest_framework_ccbv.renderers.BasePageRenderer.get_context', return_value={'foo': 'bar'})
    @patch('rest_framework_ccbv.renderers.templateEnv.get_template')
    @patch('rest_framework_ccbv.renderers.open', new_callable=mock_open)
    def test_render(self, mock_open, get_template_mock, get_context_mock):
        self.renderer.render('foo')
        mock_open.assert_called_once_with('foo', 'w')
        handle = mock_open()
        handle.write.assert_called_once()
        get_template_mock.assert_called_with('base.html')
        get_template_mock.return_value.render.assert_called_with({'foo': 'bar'})

    @patch('rest_framework_ccbv.renderers.templateEnv.get_template')
    @patch('rest_framework_ccbv.renderers.open', mock_open())
    def test_context(self, get_template_mock):
        self.renderer.render('foo')
        context = get_template_mock.return_value.render.call_args_list[0][0][0]
        assert context['version_prefix'] == 'Django REST Framework'
        assert context['version']
        assert context['versions']
        assert context['other_versions']
        assert context['klasses'] == [ListAPIView]


class TestStaticPagesRenderered(unittest.TestCase):
    def setUp(self):
        self.rendererIndex = IndexPageRenderer([ListAPIView])
        self.rendererLandPage = LandPageRenderer([ListAPIView])
        self.rendererErrorPage = ErrorPageRenderer([ListAPIView])

    @patch('rest_framework_ccbv.renderers.templateEnv.get_template')
    @patch('rest_framework_ccbv.renderers.open', mock_open())
    def test_template_name(self, get_template_mock):
        self.rendererIndex.render('foo')
        get_template_mock.assert_called_with('index.html')
        self.rendererLandPage.render('foo')
        get_template_mock.assert_called_with('home.html')
        self.rendererErrorPage.render('foo')
        get_template_mock.assert_called_with('error.html')


class TestSitemapRenderer(unittest.TestCase):
    def setUp(self):
        self.renderer = SitemapRenderer([ListAPIView])

    @patch('rest_framework_ccbv.renderers.templateEnv.get_template')
    @patch('rest_framework_ccbv.renderers.open', mock_open(read_data='{}'))
    def test_context(self, get_template_mock):
        self.renderer.render('foo')
        context = get_template_mock.return_value.render.call_args_list[0][0][0]
        assert context['latest_version']
        assert context['base_url']
        assert context['klasses'] == {}
