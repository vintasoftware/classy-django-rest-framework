import inspect

from rest_framework.serializers import BaseSerializer
from rest_framework.compat import View
from jinja2 import contextfunction, FileSystemLoader, Environment

from .config import VERSION, EXACT_VERSION

templateLoader = FileSystemLoader(searchpath="templates")
templateEnv = Environment(loader=templateLoader,
                          extensions=['jinja2.ext.with_'])


@contextfunction
def get_klass_url(context, klass, version=VERSION):
    if klass.__module__.split('.')[0] == 'django':
        return 'http://ccbv.co.uk/{}'.format(klass.__name__)
    return '/{}/{}/{}.html'.format(version, klass.__module__, klass.__name__)


@contextfunction
def get_version_url(context, version):
    if 'this_klass' in context:
        return get_klass_url(context, context['this_klass'], version)
    return '/{}/index.html'.format(version)


@contextfunction
def get_klass_docs(context, klass):
    if klass.__doc__ and klass.__doc__.strip():
        return klass.__doc__.strip()
    return ''


@contextfunction
def get_doc_link(context, klass):
    if VERSION.split('.')[0] == '2':
        base_path = "http://tomchristie.github.io/rest-framework-2-docs"
    else:
        base_path = "http://www.django-rest-framework.org"
    if issubclass(klass, View):
        category = 'generic-views'
    elif issubclass(klass, BaseSerializer):
        category = 'serializers'
    else:
        return None
    return (base_path + "/api-guide/" + category + "#" +
            klass.__name__.lower())


@contextfunction
def get_src_link(context, klass):
    base_url = "https://github.com/tomchristie/django-rest-framework/blob"
    version_path = '/{}/'.format(EXACT_VERSION)
    local_path = inspect.getsourcefile(klass)
    index = local_path.rindex('/rest_framework/') + 1
    lineno = inspect.getsourcelines(klass)[-1]
    return base_url + version_path + local_path[index:] + '#L' + str(lineno)


templateEnv.globals['get_klass_url'] = get_klass_url
templateEnv.globals['get_version_url'] = get_version_url
templateEnv.globals['get_klass_docs'] = get_klass_docs
templateEnv.globals['get_doc_link'] = get_doc_link
templateEnv.globals['get_src_link'] = get_src_link
