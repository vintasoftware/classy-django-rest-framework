from jinja2 import contextfunction, FileSystemLoader, Environment
from config import VERSION

templateLoader = FileSystemLoader(searchpath="templates")
templateEnv = Environment(loader=templateLoader,
                          extensions=['jinja2.ext.with_'])


@contextfunction
def get_view_url(context, view):
    return '/{}/{}/{}.html'.format(VERSION, view.__module__, view.__name__)


@contextfunction
def get_version_url(context, version):
    return '/{}/index.html'.format(version)


@contextfunction
def get_view_docs(context, view):
    if view.__doc__ and view.__doc__.strip():
        return view.__doc__.strip()
    return ''


templateEnv.globals['get_view_url'] = get_view_url
templateEnv.globals['get_version_url'] = get_version_url
templateEnv.globals['get_view_docs'] = get_view_docs
