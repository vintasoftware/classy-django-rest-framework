
from inspector import Inspector
from jinja_utils import templateEnv


class Generator(object):

    def __init__(self, view, module):
        self.view = view
        self.module = module
        self.inspector = Inspector(self.view, self.module)

    def get_context(self):
        ancestors = self.inspector.get_views_mro()
        attributes = self.inspector.get_attributes()
        methods = self.inspector.get_methods()
        return {'name': self.view, 'ancestors': ancestors,
                'attributes': attributes, 'methods': methods}

    def generate(self, filename):
        template = templateEnv.get_template('detail_view.html')
        context = self.get_context()
        with open(filename, 'w') as f:
            f.write(template.render(context))
