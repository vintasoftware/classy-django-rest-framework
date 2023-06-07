import logging

from decouple import config
from fabric import task

FOLDER = "public"
FOLDER = FOLDER.strip("/")

logging.basicConfig(level=logging.INFO)


@task
def deploy(c):
    AWS_BUCKET_NAME = config("AWS_BUCKET_NAME")
    AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
    c.run(
        "s3cmd sync {}/ s3://{} --acl-public --delete-removed "
        "--guess-mime-type --access_key={} --secret_key={}".format(
            FOLDER,
            AWS_BUCKET_NAME,
            AWS_ACCESS_KEY_ID,
            AWS_SECRET_ACCESS_KEY,
        )
    )


@task
def test(c):
    c.run("python runtests.py")


@task
def coverage(c):
    c.run("py.test --cov-report= --cov=rest_framework_ccbv tests/")


@task
def runserver(c):
    c.run("cd %s && python -m http.server" % FOLDER)


def clean(c):
    c.run("rm -f .klasses.json")
    c.run("rm -fr %s/*" % FOLDER)
    c.run("mkdir -p %s/static" % FOLDER)


def collect_static(c):
    c.run("cp -r static %s/" % FOLDER)


@task
def index(c):
    from build_tools.index_generator import main

    main()


@task
def version(c):
    from build_tools.compile_static import main

    main(out_folder=FOLDER)


@task
def build(c):
    clean(c)
    logging.info("collecting statics")
    collect_static(c)
    c.run("tox -c build.ini")
