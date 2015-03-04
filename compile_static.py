#!/usr/bin/env python

import os
import errno

from rest_framework_ccbv.inspector import drfviews
from rest_framework_ccbv.page_generator import Generator
from rest_framework_ccbv.jinja_utils import templateEnv


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
        mkdir_p(os.path.join('public', view.__module__))
        generator.generate(filename=os.path.join('public', view.__module__,
                                                 view.__name__ + '.html'))
    template = templateEnv.get_template('home.html')
    views = sorted(drfviews.values(),
                   key=lambda x: (x.__module__, x.__name__))
    with open(os.path.join('public', 'index.html'), 'w') as f:
        f.write(template.render({'views': views}))

if __name__ == '__main__':
    main()
