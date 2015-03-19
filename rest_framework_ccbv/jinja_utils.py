import inspect

from jinja2 import contextfunction, FileSystemLoader, Environment
from config import VERSION, EXACT_VERSION

templateLoader = FileSystemLoader(searchpath="templates")
templateEnv = Environment(loader=templateLoader,
                          extensions=['jinja2.ext.with_'])


@contextfunction
def get_view_url(context, view, version=VERSION):
    return '/{}/{}/{}.html'.format(version, view.__module__, view.__name__)


@contextfunction
def get_version_url(context, version):
    if 'this_klass' in context:
        return get_view_url(context, context['this_klass'], version)
    return '/{}/index.html'.format(version)


@contextfunction
def get_view_docs(context, view):
    if view.__doc__ and view.__doc__.strip():
        return view.__doc__.strip()
    return ''


@contextfunction
def get_doc_link(context, view):
    if VERSION.split('.')[0] == '2':
        base_path = "http://tomchristie.github.io/rest-framework-2-docs"
    else:
        base_path = "http://www.django-rest-framework.org"
    return (base_path + "/api-guide/"
            "generic-views#" + view.__name__.lower())


@contextfunction
def get_src_link(context, view):
    base_url = "https://github.com/tomchristie/django-rest-framework/blob"
    version_path = '/{}/'.format(EXACT_VERSION)
    local_path = inspect.getsourcefile(view)
    index = local_path.rindex('/rest_framework/') + 1
    lineno = inspect.getsourcelines(view)[-1]
    return base_url + version_path + local_path[index:] + '#L' + str(lineno)


templateEnv.globals['get_view_url'] = get_view_url
templateEnv.globals['get_version_url'] = get_version_url
templateEnv.globals['get_view_docs'] = get_view_docs
templateEnv.globals['get_doc_link'] = get_doc_link
templateEnv.globals['get_src_link'] = get_src_link
