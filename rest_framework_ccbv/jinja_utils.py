from jinja2 import contextfunction, FileSystemLoader, Environment


templateLoader = FileSystemLoader(searchpath="templates")
templateEnv = Environment(loader=templateLoader,
                          extensions=['jinja2.ext.with_'])


@contextfunction
def get_view_url(context, view):
    return '/{}/{}.html'.format(view.__module__, view.__name__)


@contextfunction
def get_view_docs(context, view):
    if view.__doc__ and view.__doc__.strip():
        return view.__doc__.strip()
    return ''

templateEnv.globals['get_view_url'] = get_view_url
templateEnv.globals['get_view_docs'] = get_view_docs
