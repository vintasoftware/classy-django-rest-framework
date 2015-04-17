#!/usr/bin/env python

import os
import json

from itertools import groupby

from rest_framework_ccbv.config import VERSION
from rest_framework_ccbv.inspector import drfklasses


def main():
    d = {}
    d_version = {}
    klasses = sorted(drfklasses.values(), key=lambda x: x.__module__)

    for key, value in groupby(klasses, lambda x: x.__module__):
        d_version[key] = map(lambda x: x.__name__, list(value))

    if os.path.isfile('.klasses.json'):
        with open('.klasses.json', 'r') as f:
            d = json.loads(f.read())

    d[VERSION] = d_version
    with open('.klasses.json', 'w') as f:
        json.dump(d, f, indent=2)


if __name__ == '__main__':
    main()
