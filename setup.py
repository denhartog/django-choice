from setuptools import (
    find_packages,
    setup,
)


setup(
    name='django-choice',
    version='1.0.1',
    keyword='django model form field choice',
    description='Django field choices made simple',
    url='https://github.com/denhartog/django-choice/',
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python',
    ],
    packages=find_packages(
        exclude=[
            'docs',
            'tests',
        ],
    ),
)
