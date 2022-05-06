import json
import importlib
from collections import defaultdict

from .inspector import Inspector
from .jinja_utils import template_env
from .config import REST_FRAMEWORK_VERSIONS, VERSION, BASE_URL


class BasePageRenderer(object):

    def __init__(self, klasses):
        grouped_klasses = defaultdict(list)
        for klass in klasses:
            module = klass.__module__
            # Add here all modules that should be hidden on index/navbar
            if not module.split('.')[-1] in ['fields']:
                grouped_klasses[module].append(klass)
        self.grouped_klasses = dict(grouped_klasses)

    def render(self, filename):
        template = template_env.get_template(self.template_name)
        context = self.get_context()
        with open(filename, 'w') as f:
            f.write(template.render(context))

    def get_context(self):
        other_versions = list(REST_FRAMEWORK_VERSIONS)
        other_versions.remove(VERSION)
        return {
            'version_prefix': 'Django REST Framework',
            'version': VERSION,
            'versions': REST_FRAMEWORK_VERSIONS,
            'other_versions': other_versions,
            'grouped_klasses': self.grouped_klasses,
        }


class DetailPageRenderer(BasePageRenderer):
    template_name = 'detail_view.html'

    def __init__(self, klasses, klass_name, module_name):
        super(DetailPageRenderer, self).__init__(klasses)
        self.klass_name = klass_name
        self.module_name = module_name
        self.inspector = Inspector(self.klass_name, self.module_name)

    def get_context(self):
        context = super(DetailPageRenderer, self).get_context()
        available_versions = self.inspector.get_available_versions()

        context['other_versions'] = [
            version
            for version in context['other_versions']
            if version in available_versions]
        context['name'] = self.klass_name
        context['ancestors'] = self.inspector.get_klass_mro()
        context['direct_ancestors'] = self.inspector.get_direct_ancestors()
        context['attributes'] = self.inspector.get_attributes()
        context['methods'] = self.inspector.get_methods()

        context['this_module'] = self.module_name

        module = importlib.import_module(self.module_name)
        context['this_klass'] = getattr(module, self.klass_name)

        context['children'] = self.inspector.get_children()
        context['unavailable_methods'] = self.inspector.get_unavailable_methods()
        return context


class IndexPageRenderer(BasePageRenderer):
    template_name = 'index.html'


class LandPageRenderer(BasePageRenderer):
    template_name = 'home.html'


class ErrorPageRenderer(BasePageRenderer):
    template_name = 'error.html'


class SitemapRenderer(BasePageRenderer):
    template_name = 'sitemap.xml'

    def get_context(self):
        context = {}
        with open('.klasses.json', 'r') as f:
            klasses = json.load(f)

        context['klasses'] = klasses
        context['latest_version'] = REST_FRAMEWORK_VERSIONS[-1]
        context['base_url'] = BASE_URL
        return context
