from rest_framework import VERSION as rest_framework_version


REST_FRAMEWORK_VERSIONS = [
    "3.9",
    "3.10",
    "3.11",
    "3.12",
    "3.13",
    "3.14",
    "3.15",
    "3.16",
]


VERSION = ".".join(rest_framework_version.split(".")[:2])
EXACT_VERSION = rest_framework_version
BASE_URL = "https://www.cdrf.co"
