
from inspector import Inspector
from jinja_utils import templateEnv
from config import REST_FRAMEWORK_VERSIONS, VERSION


class BasePageGenerator(object):

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
                'other_versions': other_versions}


class DetailPageGenerator(BasePageGenerator):
    template_name = 'detail_view.html'

    def __init__(self, view, module):
        self.view = view
        self.module = module
        self.inspector = Inspector(self.view, self.module)

    def get_context(self):
        context = super(DetailPageGenerator, self).get_context()
        context['name'] = self.view
        context['ancestors'] = self.inspector.get_views_mro()
        context['attributes'] = self.inspector.get_attributes()
        context['methods'] = self.inspector.get_methods()
        return context


class IndexPageGenerator(BasePageGenerator):
    template_name = 'index.html'

    def __init__(self, views):
        self.views = views

    def get_context(self):
        context = super(IndexPageGenerator, self).get_context()
        context['views'] = self.views
        return context
