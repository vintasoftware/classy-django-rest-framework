from rest_framework import VERSION as rest_framework_version


REST_FRAMEWORK_VERSIONS = [
    '3.12',
]


VERSION = '.'.join(rest_framework_version.split('.')[:2])
EXACT_VERSION = rest_framework_version
BASE_URL = 'http://www.cdrf.co'
