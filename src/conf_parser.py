from __future__ import annotations

from typing import Any

import bios

from src.argument import Argument
from src.exceptions.requried_argument_not_found_exception import RequiredArgumentNotFoundException


class ConfParse:
    def __init__(self, description=None, required=True, context='Main'):
        self.description = description
        self.arguments = []
        self.sub_sections = {}
        self.required = required
        self.context = context

    def add_argument(self, arg_name, arg_type=Any, default=None, description="", required=False):
        '''
        Add an expected argument to the configuration
        :param arg_name: the name of the argument- the "key" of the value
        :param arg_type: the type of the argument.
        :param default: default value for the argument
        :param description: description of the argument
        :param required: True if the configuration must have this argument
        :return: None
        '''
        arg = Argument(name=arg_name, argument_type=arg_type, default_value=default, description=description, required=required)
        self.arguments.append(arg)

    def add_sub_section(self, name: str, section: ConfParse) -> None:
        '''
        Add a subsection to the configuration.
        A subsection is a complex data of type ConfParser.
        :param name: name of the subsection.
        :param section: the sub section.
        :return: None
        '''
        section.context = name
        self.sub_sections[name] = section

    def _parse(self, values: dict) -> ConfParse:
        '''
        Ingest the values of arguments from python dictionary
        :param values: python dictionary representing the concrete configuration with values.
        :return: self
        '''
        for arg in self.arguments:
            val = values.get(arg.name, None)
            if not val and arg.required and not arg.default:
                raise RequiredArgumentNotFoundException(
                    f"Failed to find argument named {arg.name} in context {self.context}")
            arg.validate(val)
            setattr(self, arg.name, val)
        for sub_section_name, sub_section in self.sub_sections.items():
            if not sub_section.required and sub_section_name not in values.keys():
                continue
            parsed_sub_section = sub_section._parse(values[sub_section_name])
            setattr(self, sub_section_name, parsed_sub_section)
        return self

    def parse(self, path: str) -> ConfParse:
        '''
        Parse a configuration file based on the current ConfParse file.
        This function supports the types supported by the python package 'bios'- json, yaml, csv and others
        :param path: path of the configuration file
        :return: self
        '''
        values = bios.read(path)
        return self._parse(values)

    def _get_example_str_json(self, nesting=1) -> str:
        nesting_spaces = '    '
        s = nesting_spaces * (nesting - 1) + "{\n"
        lines = []
        for arg in self.arguments:
            lines.append(nesting_spaces * nesting + arg.example_str(doc_format='json'))
        for sub_section_name, sub_section in self.sub_sections.items():
            sub_section_text = sub_section._get_example_str_json(nesting=nesting + 1)
            lines.append(nesting_spaces * nesting + f'"{sub_section_name}":\n{sub_section_text}')
        s += ',\n'.join(lines)
        s += "\n" + nesting_spaces * (nesting - 1) + "}"
        return s

    def _get_example_str(self, doc_format='json') -> str:
        '''
        Get an example configuration file string
        :param doc_format:
        :return:
        '''
        if doc_format == 'json':
            return self._get_example_str_json()

    def save_example(self, path, doc_format='json'):
        '''
        Create an example configuration file.
        :param path: path where the example file will be saved.
        :param doc_format: the format of the doc file.
        :return: None
        '''
        with open(path, 'w') as f:
            f.write(self._get_example_str(doc_format=doc_format))
