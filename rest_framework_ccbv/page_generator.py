
from inspector import Inspector
from jinja_utils import templateEnv
from config import REST_FRAMEWORK_VERSIONS, VERSION
from itertools import ifilter


class BasePageGenerator(object):

    def __init__(self, views):
        self.views = views

    def generate(self, filename):
        template = templateEnv.get_template(self.template_name)
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
            'views': self.views}


class DetailPageGenerator(BasePageGenerator):
    template_name = 'detail_2.html'

    def __init__(self, views, view, module):
        super(DetailPageGenerator, self).__init__(views)
        self.view = view
        self.module = module
        self.inspector = Inspector(self.view, self.module)

    def get_context(self):
        context = super(DetailPageGenerator, self).get_context()
        context['name'] = self.view
        context['ancestors'] = self.inspector.get_views_mro()
        context['attributes'] = self.inspector.get_attributes()
        context['methods'] = self.inspector.get_methods()
        context['this_klass'] = next(ifilter(lambda x: x.__name__ == self.view,
                                             self.views))
        context['children'] = self.inspector.get_children()
        context['this_module'] = context['this_klass'].__module__
        return context


class IndexPageGenerator(BasePageGenerator):
    template_name = 'index.html'
