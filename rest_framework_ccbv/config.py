from rest_framework import VERSION as rest_framework_version


REST_FRAMEWORK_VERSIONS = [
    "3.1",
    "3.2",
    "3.3",
    "3.4",
    "3.5",
    "3.6",
    "3.7",
    "3.8",
    "3.9",
    "3.10",
    "3.11",
    "3.12",
    "3.13",
]


VERSION = ".".join(rest_framework_version.split(".")[:2])
EXACT_VERSION = rest_framework_version
BASE_URL = "https://www.cdrf.co"
