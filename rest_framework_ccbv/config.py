from rest_framework import VERSION as rest_framework_version


REST_FRAMEWORK_VERSIONS = [
    '2.1',
    '2.2',
    '2.3',
    '2.4',
    '3.0',
    '3.1'
]


VERSION = '.'.join(rest_framework_version.split('.')[:2])
