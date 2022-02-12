from typing_validation import validate


class Argument:
    def __init__(self, name, argument_type, description, default_value, required):
        self.name = name
        self.type = argument_type
        self.description = description
        self.default_value = default_value
        self.required = required

    def validate(self, value):
        validate(value, self.type)

    def example_str(self, doc_format='json'):
        return f'"{self.name}": "{self.default_value}"  # required-{self.required}, type- {self.type}, description- {self.description}'

    def __str__(self):
        return f'{self.name}:{self.type}'
