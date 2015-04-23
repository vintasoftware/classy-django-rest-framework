
import logging

from decouple import config
from fabric.api import local

FOLDER = 'public'
FOLDER = FOLDER.strip('/')

logging.basicConfig(level=logging.INFO)


def deploy():
    AWS_BUCKET_NAME = config('AWS_BUCKET_NAME')
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    local("s3cmd sync {}/ s3://{} --acl-public --delete-removed "
          "--guess-mime-type --access_key={} --secret_key={}".format(
            FOLDER,
            AWS_BUCKET_NAME,
            AWS_ACCESS_KEY_ID,
            AWS_SECRET_ACCESS_KEY
            )
          )


def test():
    local("python runtests.py")


def runserver():
    local("cd %s && python -m SimpleHTTPServer" % FOLDER)


def clean():
    local("rm -f .klasses.json")
    local("rm -fr %s/*" % FOLDER)
    local("mkdir -p %s/static" % FOLDER)


def collect_static():
    local("cp -r static %s/" % FOLDER)


def build_local():
    clean()
    collect_static()
    index_generator_for_version()
    build_for_version()


def index_generator_for_version():
    from build_tools.index_generator import main
    main()


def build_for_version():
    from build_tools.compile_static import main
    main(out_folder=FOLDER)


def build():
    clean()
    logging.info("collecting statics")
    collect_static()
    local("tox -c build.ini")
