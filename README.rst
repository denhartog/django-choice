=============
django-choice
=============
--------------------------------
Django field choices made simple
--------------------------------

Why django-choice exists
========================
django-choice exists because the official Django "way" is clunky (See .. _Official Django Documentation: https://docs.djangoproject.com/en/2.0/ref/models/fields/#choices)::
    # models.py
    from django.db import models

    class Student(models.Model):
        FRESHMAN = 'FR'
        SOPHOMORE = 'SO'
        JUNIOR = 'JR'
        SENIOR = 'SR'
        YEAR_IN_SCHOOL_CHOICES = (
            (FRESHMAN, 'Freshman'),
            (SOPHOMORE, 'Sophomore'),
            (JUNIOR, 'Junior'),
            (SENIOR, 'Senior'),
        )
        year_in_school = models.CharField(
            max_length=2,
            choices=YEAR_IN_SCHOOL_CHOICES,
            default=FRESHMAN,
        )

How django-choice works
=======================
django-choices works in two steps, first create a `Choice` object in `choices.py`::
    # choices
    from django_choice import DjangoChoice, DjangoChoices

    class ClassChoice(DjangoChoices):
        FRESHMAN = DjangoChoice('FR')

and second, import your `Choice` into `models.py`::
    # models.py
    from django.db import models
    from .choices import ClassChoice

    class Student(models.Model):
    year_in_school = models.CharField(
        max_length=2,
        choices=ClassChoice,
        default=ClassChoice.FRESHMAN,
    )


Publishing
==========
PyPI::
----
    python setup.py sdist
    python setup.py bdist_wheel
    twine upload dist/*

GitHub::
------
    git add .
    git commit -m 'message'
    git push

Change Log
==========
1.0.0
-----
* initial release
