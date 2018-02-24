=============
django-choice
=============
Choices made simple for Django model and form fields

Installing
==========

.. code::

    pip install django-choice

Why django-choice exists
========================
**django-choice** exists because the official Django "way" is clunky (taken verbatim from the `Official Django Documentation`_)

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

        def is_upperclass(self):
            return self.year_in_school in (self.JUNIOR, self.SENIOR)

How django-choice works
=======================
**django-choice** works in two (2) steps, first create a :code:`Choices` object in :code:`choices.py`

.. code:: python

    # choices.py
    from django_choice import DjangoChoice, DjangoChoices

    class StudentYearChoice(DjangoChoices):
        FRESHMAN = DjangoChoice('FR')
        SOPHOMORE = DjangoChoice('SO')
        JUNIOR = DjangoChoice('JR')
        SENIOR = DjangoChoice('SR')

and second, import your :code:`Choices` object into :code:`models.py`

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

    def is_upperclass(self):
        return self.year_in_school in (
            StudentYearChoice.JUNIOR,
            StudentYearChoice.SENIOR,
        )

because :code:`StudentYearChoice.CHOICES` is

.. code:: python

    # shell
    >>> print(StudentYearChoiceself.CHOICES)
    [
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
    ]

and :code:`StudentYearChoice.FRESHMAN` is

.. code:: python

    # shell
    >>> print(StudentYearChoice.FRESHMAN)
    FR

which results in the same basic behavior as the default Django way, but now choices are objectified, encapsulated, and can be easily extended

But wait! There's more!
=======================
Default behavior
----------------

By default, **django-choice** does five (5) things:

(1) Looks for class attributes that are instances of :code:`DjangoChoice`

So while :code:`GRADUATE` will persist, **django-choice** does not do anything special to :code:`GRADUATE` (meaning default Python class attribute behaviors apply)

.. code:: python

    # choices.py
    from django_choice import DjangoChoice, DjangoChoices

    class StudentYearChoice(DjangoChoices):
        FRESHMAN = DjangoChoice()
        SOPHOMORE = DjangoChoice()
        JUNIOR = DjangoChoice()
        SENIOR = DjangoChoice()
        GRADUATE = True

    # shell
    >>> print(StudentYearChoice.GRADUATE)
    True

(2) If no :code:`value` is provided, the attribute itself is assigned as the value, and then lowercased using :code:`lower()`

(3) If no :code:`label` is provided, the attribute itself is assigned as the label

    * By default, underscores (`_`) in attributes are replaced with spaces, and then title cased using :code:`title()`

.. code:: python

    # choices.py
    from django_choice import DjangoChoice, DjangoChoices

    class StudentYearChoice(DjangoChoices):
        FRESH_MAN = DjangoChoice()
        SOPHOMORE = DjangoChoice()
        JUNIOR = DjangoChoice()
        SENIOR = DjangoChoice()

    # shell
    >>> print(StudentYearChoice.CHOICES)
    [
        ('fresh_man', 'Fresh Man'),
        ('sophomore', 'Sophomore'),
        ('junior', 'Junior'),
        ('senior', 'Senior'),
    ]

(4) If no :code:`sort_value` is provided, the sort_value is auto-incremented by 1; resulting in :code:`DjangoChoice` objects being sorted in the order in which they are defined

(5) By default, :code:`CHOICES` is sorted by the value of :code:`sort_value` (which, again, by default is the order in which they occur)

    * However, defined :code:`DjangoChoices` can define a single-argument :code:`@staticmethod` named :code:`sort_by` to modify this behavior

.. code:: python

    # choices.py
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

    # shell
    >>> print(StudentYearChoice.CHOICES)
    [
        ('FR', 'Freshman'),
        ('JR', 'Junior'),
        ('SO', 'Sophomore'),
        ('SR', 'Senior'),
    ]

Custom values
-------------
Most examples thus far have been using custom values (e.g. 'FR', 'SO', et cetera)

Custom labels
-------------

.. code:: python

    # choices.py
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

    # choices.py
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
Unnamed :code:`__init__(**kwargs)` become attributes of :code:`DjangoChoice` instances

.. code:: python

    # choices.py
    from django_choice import DjangoChoice, DjangoChoices

    class StudentYearChoice(DjangoChoices):
        FRESHMAN = DjangoChoice('FR', 'Frosh', 3)
        SOPHOMORE = DjangoChoice('SO', 'Soph', 2)
        JUNIOR = DjangoChoice('JR', sort_value=1, example=lambda x: x.upper())
        SENIOR = DjangoChoice('SR', sort_value=0, has_senioritis=True)

and are accessible through :code:`from_value`

.. code:: python

    # shell
    >>> print(StudentYearChoice.from_value(StudentYearChoice.JUNIOR).example('hi'))
    HI

    >>> print(StudentYearChoice.from_value(StudentYearChoice.SENIOR).has_senioritis)
    True

from_value()
------------
:code:`from_value()` comes in handy when working with Django models and forms

.. code:: python

    # shell
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

Why I created django-choice
---------------------------
Because I often found myself mapping field choices to python objects, but now I can encapsulate that relationship in the choice itself

.. code:: python

    # choices.py
    from django_choice import DjangoChoice, DjangoChoices
    from .example import ThingFR, ThingSO, ThingJR, ThingSR

    class StudentYearChoice(DjangoChoices):
        FRESHMAN = DjangoChoice('FR', 'Frosh', to_python=ThingFR)
        SOPHOMORE = DjangoChoice('SO', 'Soph', to_python=ThingSO)
        JUNIOR = DjangoChoice('JR', to_python=ThingJR)
        SENIOR = DjangoChoice('SR', to_python=ThingSR)

    # forms.py
    from .choices import StudentYearChoice

    class StudentForm(forms.Form):
        year_in_school = forms.ChoiceField(
            choices=StudentYearChoice.CHOICES,
            initial=StudentYearChoice.FRESHMAN,
        )

        def clean_year_in_school(self):
            return StudentYearChoice.from_value(self.cleaned_data['year_in_school']).to_python

where I used to have to do something like this:

.. code:: python

    # forms.py
    def clean_year_in_school(self):
        mapping = {
            StudentYearChoice.FRESHMAN: ThingFR,
            StudentYearChoice.SOPHOMORE: ThingSO,
            StudentYearChoice.JUNIOR: ThingJR,
            StudentYearChoice.SENIOR: ThingSR,
        }
        return mapping[self.cleaned_data['year_in_school']]

but I would create a :code:`mappings.py` file because this mapping was used in multiple places where I would have to import both :code:`mappings` and :code:`choices`

Quick References
================

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

reStructuredText
----------------
http://docutils.sourceforge.net/docs/user/rst/quickref.html

Change Log
==========
1.0.3
-----
* fixed DjangoChoiceMetaclass :code:`setattr()` bug with default :code:`value`

1.0.2
-----
* set default auto-increment behavior for :code:`sort_value`

1.0.1
-----
* renamed python module

1.0.0
-----
* initial release
