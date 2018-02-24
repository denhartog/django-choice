# PYTHON
from unittest import TestCase

# MODULE
from django_choice import (
    DjangoChoice,
    DjangoChoices,
)


class TestChoice(DjangoChoices):
    TEST_ATTR = DjangoChoice()


class Test1Choice(DjangoChoices):
    TEST_ATTR_1 = DjangoChoice(1)


class Test2Choice(Test1Choice):
    TEST_ATTR_2 = DjangoChoice(2, 'Custom label')


class Test3Choice(Test2Choice):
    TEST_ATTR_3 = DjangoChoice(3, sort_order=4)


class Test4Choice(Test3Choice):
    TEST_ATTR_4 = DjangoChoice(4, sort_order=2, custom_attr='rawr')


class DjangoChoicesTestCase(TestCase):
    def test_choice(self):
        self.assertEqual(TestChoice.TEST_ATTR, 'test_attr')
        self.assertEqual(len(TestChoice.CHOICES), 1)
        choice = TestChoice.from_value(TestChoice.TEST_ATTR)
        self.assertEqual(choice.value, 'test_attr')
        self.assertEqual(choice.label, 'Test Attr')
        self.assertEqual(choice.sort_order, choice.label)
