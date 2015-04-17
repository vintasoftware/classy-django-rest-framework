#!/usr/bin/env python

import os
import errno

from rest_framework_ccbv.config import VERSION, REST_FRAMEWORK_VERSIONS
from rest_framework_ccbv.inspector import drfklasses
from rest_framework_ccbv.renderers import (DetailPageRenderer,
                                           IndexPageRenderer,
                                           LandPageRenderer)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def main():
    klasses = sorted(drfklasses.values(),
                     key=lambda x: (x.__module__, x.__name__))

    for klass in drfklasses.values():
        renderer = DetailPageRenderer(klasses, klass.__name__,
                                      klass.__module__)
        mkdir_p(os.path.join('public', VERSION, klass.__module__))
        renderer.render(filename=os.path.join('public', VERSION,
                                              klass.__module__,
                                              klass.__name__ + '.html'))

    renderer = IndexPageRenderer(klasses)
    renderer.render(os.path.join('public', VERSION, 'index.html'))

    if VERSION == REST_FRAMEWORK_VERSIONS[-1]:
        renderer = LandPageRenderer(klasses)
        renderer.render(os.path.join('public', 'index.html'))


if __name__ == '__main__':
    main()
