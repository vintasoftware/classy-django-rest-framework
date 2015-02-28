#!/usr/bin/env python

import os, errno

from rest_framework_ccbv.inspector import drfviews
from rest_framework_ccbv.page_generator import Generator


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def main():
    for view in drfviews.values():
        generator = Generator(view.__name__, view.__module__)
        mkdir_p(os.path.join('static', view.__module__))
        generator.generate(filename=os.path.join('static', view.__module__,
                                                 view.__name__ + '.html'))


if __name__ == '__main__':
    main()
