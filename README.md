# Classy Django REST Framework. 
[![Build Status](https://github.com/vintasoftware/classy-django-rest-framework/actions/workflows/build.yml/badge.svg)](https://github.com/vintasoftware/classy-django-rest-framework/actions/workflows/build.yml) [![Coverage Status](https://coveralls.io/repos/github/vintasoftware/classy-django-rest-framework/badge.svg?branch=develop)](https://coveralls.io/github/vintasoftware/classy-django-rest-framework?branch=develop)

## What is this?

[Django REST framework](https://www.django-rest-framework.org) is a powerful and flexible toolkit that makes it easy to build Web APIs. It provides class based generic API views and serializers. We've taken all the attributes and methods that every view/serializer defines or inherits, and flattened all that information onto one comprehensive page per class. This project is heavily based on [Classy Class-Based Views](https://ccbv.co.uk) and was developed by [Vinta Software Studio](https://www.vinta.com.br).

## Dependencies
* Classy Django REST Framework is ready for development with [Dev Container](https://code.visualstudio.com/docs/devcontainers/tutorial). After downloading the code you just need to use "Reopen in Container" option and after building run `pip install -r requirements-test.txt` just once.


## Building

`fab build`

The first build will take a while.

## Run locally:

`fab runserver`

## Deployment

- Run the github action [release](https://github.com/vintasoftware/classy-django-rest-framework/actions/workflows/build-deploy.yml)

## Tests

`fab test`

## Adding a new version

1. Add the version to `rest_framework_ccbv.config.py::REST_FRAMEWORK_VERSIONS`
2. In `build.ini`:
    - Add the version to envlist
    - Add the deps to the version, use the latest supported django version (check deps314)
    - Add the index generation (check testenv:drf314)
    - Add the doc generation (check testenv:drfbuild314)
3. Update `requirements-test.txt` to use the latest supported DRF version and its latest supported Django version

## Commercial Support

[![alt text](https://avatars2.githubusercontent.com/u/5529080?s=80&v=4 "Vinta Logo")](https://www.vinta.com.br/)

This project is maintained by [Vinta Software](https://www.vinta.com.br/) and is used in products of Vinta's clients. We are always looking for exciting work, so if you need any commercial support, feel free to get in touch: contact@vinta.com.br

