

class DjangoChoice:
    sort_value = 0

    def __init__(
        self,
        value=None,
        label=None,
        sort_value=None,
        **kwargs
    ):
        self.value = value
        self.label = label
        self.sort_value = int(
            sort_value
            if sort_value is not None else
            DjangoChoice.sort_value
        )
        DjangoChoice.sort_value += 1

        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def __str__(self):
        return str(self.value)


class DjangoChoiceMetaclass(type):
    # parameters are those expected by type.__init__
    def __init__(
        self,
        name,
        bases,
        attrs,
    ):
        # permits subclasses of subclasses
        super().__init__(name, bases, attrs)
        # get the new choices
        _choices = {
            attr: choice
            for attr, choice in attrs.items()
            if isinstance(choice, DjangoChoice)
        }
        for attr, choice in _choices.items():
            if choice.value is None:
                choice.value = attr.lower()
            # versus custom __*__ for every type (e.g. __int__, et cetera)
            # or requiring MyClass.MY_CONSTANT.value
            setattr(self, attr, choice.value)
            if choice.label is None:
                choice.label = attr.replace('_', ' ').title()
        # permit get_choice()
        self._choices = {
            **{
                choice.value: choice
                for choice in _choices.values()
            },
            **getattr(self, '_choices', {}),
        }
        # choices for Django field
        self.CHOICES = [
            (choice.value, choice.label, )
            for choice in sorted(
                (choice for choice in self._choices.values()),
                key=self.sort_by,
            )
        ]

    def __iter__(self):
        for choice in self.CHOICES:
            yield choice


class DjangoChoices(metaclass=DjangoChoiceMetaclass):
    @staticmethod
    def sort_by(choice):
        return choice.sort_value  # any DjangoChoice.attr (+ kwargs => attrs)

    @classmethod
    def from_value(
        cls,
        value,
    ):
        return cls._choices[value]
