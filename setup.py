from setuptools import (
    find_packages,
    setup,
)


setup(
    name='django-choice',
    version='1.0.2',
    keyword='django choice field model form',
    description='Choices made simple for Django model and form fields',
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
