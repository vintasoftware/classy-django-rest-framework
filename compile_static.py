#!/usr/bin/env python

import os
import errno

from rest_framework_ccbv.config import VERSION, REST_FRAMEWORK_VERSIONS
from rest_framework_ccbv.inspector import drfviews
from rest_framework_ccbv.page_generator import (DetailPageGenerator,
                                                IndexPageGenerator)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def main():
    for view in drfviews.values():
        generator = DetailPageGenerator(view.__name__, view.__module__)
        mkdir_p(os.path.join('public', VERSION, view.__module__))
        generator.generate(filename=os.path.join('public', VERSION,
                                                 view.__module__,
                                                 view.__name__ + '.html'))
    views = sorted(drfviews.values(),
                   key=lambda x: (x.__module__, x.__name__))

    generator = IndexPageGenerator(views)
    generator.generate(os.path.join('public', VERSION, 'index.html'))

    if VERSION == REST_FRAMEWORK_VERSIONS[-1]:
        generator.generate(os.path.join('public', 'index.html'))


if __name__ == '__main__':
    main()
