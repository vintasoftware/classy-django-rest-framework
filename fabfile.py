
import os
import logging

from decouple import config
from fabric.api import local

FOLDER = 'public'
FOLDER = FOLDER.strip('/')

logging.basicConfig(level=logging.INFO)


def deploy():
    import boto
    from boto.s3.connection import S3Connection
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    BUCKET_NAME = config('AWS_BUCKET_NAME')
    conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

    bucket = conn.get_bucket(BUCKET_NAME)
    key = boto.s3.key.Key(bucket)
    for dirpath, dirnames, filenames in os.walk(FOLDER):
        # do not use the FOLDER prefix
        destpath = dirpath[len(FOLDER):]
        destpath = destpath.strip('/')
        logging.info("Uploading %s files from %s to %s", len(filenames),
                     dirpath, BUCKET_NAME)
        for filename in filenames:
            key.name = os.path.relpath(os.path.join(destpath, filename)
                                       ).replace('\\', '/')
            key.set_contents_from_filename(os.path.join(dirpath, filename))
            logging.debug("Sending %s", key.name)


def test():
    local("python runtests.py")


def runserver():
    local("cd public")
    local("pwd")
    local("cd public && python -m SimpleHTTPServer")


def build():
    logging.info("collecting statics")
    local("rm -fr public/static")
    local("cp -r static public/")
    logging.info("building statics")
    from compile_static import main
    main()
