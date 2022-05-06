import inspect

from rest_framework.serializers import BaseSerializer
from rest_framework.compat import View
from jinja2 import pass_context, FileSystemLoader, Environment

from .config import VERSION, EXACT_VERSION

template_loader = FileSystemLoader(searchpath="templates")
template_env = Environment(loader=template_loader)


@pass_context
def get_klass_url(context, klass, version=VERSION):
    if klass.__module__.split(".")[0] == "django":
        return "https://ccbv.co.uk/{}".format(klass.__name__)
    return "/{}/{}/{}.html".format(version, klass.__module__, klass.__name__)


@pass_context
def get_version_url(context, version):
    if "this_klass" in context:
        return get_klass_url(context, context["this_klass"], version)
    return "/{}/index.html".format(version)


@pass_context
def get_klass_docs(context, klass):
    if klass.__doc__ and klass.__doc__.strip():
        return klass.__doc__.strip()
    return ""


@pass_context
def get_doc_link(context, klass):
    if VERSION.split(".")[0] == "2":
        base_path = "https://tomchristie.github.io/rest-framework-2-docs"
    else:
        base_path = "https://www.django-rest-framework.org"
    if issubclass(klass, View):
        category = "generic-views"
    elif issubclass(klass, BaseSerializer):
        category = "serializers"
    else:
        return None
    return base_path + "/api-guide/" + category + "#" + klass.__name__.lower()


@pass_context
def get_src_link(context, klass):
    base_url = "https://github.com/tomchristie/django-rest-framework/blob"
    version_path = "/{}/".format(EXACT_VERSION)
    local_path = inspect.getsourcefile(klass)
    index = local_path.rindex("/rest_framework/") + 1
    lineno = inspect.getsourcelines(klass)[-1]
    return base_url + version_path + local_path[index:] + "#L" + str(lineno)


template_env.globals["get_klass_url"] = get_klass_url
template_env.globals["get_version_url"] = get_version_url
template_env.globals["get_klass_docs"] = get_klass_docs
template_env.globals["get_doc_link"] = get_doc_link
template_env.globals["get_src_link"] = get_src_link
