=============
django-choice
=============
Django field choices made simple

Why django-choice exists
========================
django-choice exists because the official Django "way" is clunky (See `Official Django Documentation`_)

.. _`Official Django Documentation`: https://docs.djangoproject.com/en/2.0/ref/models/fields/#choices

.. code:: python

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
django-choices works in two steps, first create a `Choice` object in `choices.py`

.. code:: python

    # choices
    from django_choice import DjangoChoice, DjangoChoices

    class StudentYearChoice(DjangoChoices):
        FRESHMAN = DjangoChoice('FR')
        SOPHOMORE = DjangoChoice('SO')
        JUNIOR = DjangoChoice('JR')
        SENIOR = DjangoChoice('SR')

and second, import your `Choice` into `models.py`

.. code:: python

    # models.py
    from django.db import models
    from .choices import StudentYearChoice

    class Student(models.Model):
    year_in_school = models.CharField(
        max_length=2,
        choices=StudentYearChoice.CHOICES,
        default=StudentYearChoice.FRESHMAN,
    )

because `StudentYearChoice.CHOICES` is

.. code:: python

    # shell
    >>> print(StudentYearChoice)
    [
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
    ]

and `StudentYearChoice.FRESHMAN` is

.. code:: python

    # shell
    >>> print(StudentYearChoice.FRESHMAN)
    FR

But wait! There's more!
=======================
Default behavior
----------------
By default, *django-choice* does five (5) things:
(1) Looks for class attributes that are instances of `DjangoChoice`

So while `GRADUATE` will persist, django-choice does not do anything special to `GRADUATE`

.. code:: python

    # choices
    from django_choice import DjangoChoice, DjangoChoices

    class StudentYearChoice(DjangoChoices):
        FRESHMAN = DjangoChoice()
        SOPHOMORE = DjangoChoice()
        JUNIOR = DjangoChoice()
        SENIOR = DjangoChoice()
        GRADUATE = True

(2) If no `value` is provided, the attribute itself is assigned as the value
(3) If no `label` is provided, the attribute itself is assigned as the label
- By default, underscores (`_`) in attributes are replaced with spaces (` `), and then titled cased using `title()`

.. code:: python

    # choices
    from django_choice import DjangoChoice, DjangoChoices

    class StudentYearChoice(DjangoChoices):
        FRESH_MAN = DjangoChoice()
        SOPHOMORE = DjangoChoice()
        JUNIOR = DjangoChoice()
        SENIOR = DjangoChoice()

    >>> print(StudentYearChoice.CHOICES)
    [
        ('fresh_man', 'Fresh Man'),
        ('sophomore', 'Sophomore'),
        ('junior', 'Junior'),
        ('senior', 'Senior'),
    ]

(4) If no `sort_value` is provided, the sort_value is auto-incremented by 1 resulting in `DjangoChoice` objects being sorted in the order in which they are defined
(5) By default, `CHOICES` is sorted by the value of `sort_value` (which, again, by default is the order in which they occur)
- However, defined `DjangoChoices` can define a single-argument `@staticmethod` named `sort_by` to modify this behavior

.. code:: python

    # choices
    from django_choice import DjangoChoice, DjangoChoices

    class StudentYearChoice(DjangoChoices):
        FRESHMAN = DjangoChoice('FR')
        SOPHOMORE = DjangoChoice('SO')
        JUNIOR = DjangoChoice('JR')
        SENIOR = DjangoChoice('SR')

        @staticmethod
        def sort_by(choice):
            # this can return ANY value
            # NOTE: this can access any kwarg turned attribute (which we cover later)
            return choice.value

    >>> print(StudentYearChoice.CHOICES)
    [
        ('FR', 'Freshman'),
        ('JR', 'Junior'),
        ('SO', 'Sophomore'),
        ('SR', 'Senior'),
    ]

Custom values
-------------
All examples have been using custom values (e.g. 'FR', 'SO', et cetera)

Custom labels
-------------

.. code:: python

    # choices
    from django_choice import DjangoChoice, DjangoChoices

    class StudentYearChoice(DjangoChoices):
        FRESHMAN = DjangoChoice('FR', 'Frosh')
        SOPHOMORE = DjangoChoice('SO', 'Soph')
        JUNIOR = DjangoChoice('JR')
        SENIOR = DjangoChoice('SR')

    # shell
    >>> print(StudentYearChoice.CHOICES)
    [
        ('JR', 'Junior'),
        ('SR', 'Senior'),
        ('FR', 'Frosh'),
        ('SO', 'Soph'),
    ]

Custom ordering
---------------

.. code:: python

    # choices
    from django_choice import DjangoChoice, DjangoChoices

    class StudentYearChoice(DjangoChoices):
        FRESHMAN = DjangoChoice('FR', 'Frosh', 3)
        SOPHOMORE = DjangoChoice('SO', 'Soph', 2)
        JUNIOR = DjangoChoice('JR', sort_value=1)
        SENIOR = DjangoChoice('SR', sort_value=0)

    # shell
    >>> print(StudentYearChoice.CHOICES)
    [
        ('SR', 'Senior'),
        ('JR', 'Junior'),
        ('SO', 'Soph'),
        ('FR', 'Frosh'),
    ]

Custom attributes
-----------------
Unnamed `__init__(**kwargs)` become attributes of `DjangoChoice` instances, which are accessible through `from_value`

.. code:: python

    # choices
    from django_choice import DjangoChoice, DjangoChoices

    class StudentYearChoice(DjangoChoices):
        FRESHMAN = DjangoChoice('FR', 'Frosh', 3)
        SOPHOMORE = DjangoChoice('SO', 'Soph', 2)
        JUNIOR = DjangoChoice('JR', sort_value=1, example=lambda x: x.upper())
        SENIOR = DjangoChoice('SR', sort_value=0, has_senioritis=True)

    # shell
    >>> print(StudentYearChoice.from_value(StudentYearChoice.JUNIOR).example('hi'))
    HI

    >>> print(StudentYearChoice.from_value(StudentYearChoice.SENIOR).has_senioritis)
    True

`from_value()` comes in handy when working with Django models and forms

.. code:: python

    # models
    from .choices import StudentYearChoice
    from .models import Student

    student = Student.objects.filter(year_in_school=StudentYearChoice.SENIOR)
    has_senioritis = StudentYearChoice.from_value(student.year_in_school).has_senioritis

    >>> print(has_senioritis)
    True

    # forms.py
    from django import forms
    from .choices import StudentYearChoice
    from .forms import StudentForm

    class StudentForm(forms.Form):
        year_in_school = forms.ChoiceField(
            choices=StudentYearChoice.CHOICES,
            initial=StudentYearChoice.FRESHMAN,
        )

        def clean_year_in_school(self):
            has_senioritis = StudentYearChoice.from_value(self.cleaned_data['year_in_school']).has_senioritis
            return

        def clean(self):
            has_senioritis = StudentYearChoice.from_value(self.cleaned_data['year_in_school']).has_senioritis
            return

Publishing
==========
PyPI
----

.. code::

    python setup.py sdist
    python setup.py bdist_wheel
    twine upload dist/*

GitHub
------

.. code::

    git add .
    git commit -m 'message'
    git push

Change Log
==========
1.0.0
-----
* initial release
