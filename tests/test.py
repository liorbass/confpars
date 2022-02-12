import pytest

from src.conf_parser import ConfParse
from src.exceptions.requried_argument_not_found_exception import RequiredArgumentNotFoundException


def test_simple():
    cp = ConfParse()
    cp.add_argument('arg1', arg_type=str)
    cp.add_argument('arg2', arg_type=str)
    parsed = cp.parse(path='test_files/simple_example.json')
    assert parsed.arg1 == 'val1'
    assert parsed.arg2 == 'val2'


def test_validation_error():
    cp = ConfParse()
    cp.add_argument('arg1', arg_type=int)
    cp.add_argument('arg2', arg_type=str)
    with pytest.raises(TypeError):
        parsed = cp.parse(path='test_files/simple_example.json')


def test_no_type():
    cp = ConfParse()
    cp.add_argument('arg1')
    cp.add_argument('arg2', arg_type=str)
    parsed = cp.parse(path='test_files/simple_example.json')
    assert parsed.arg1 == 'val1'


def test_required_argument_missing():
    cp = ConfParse()
    cp.add_argument('arg1', arg_type=str)
    cp.add_argument('arg2', arg_type=str)
    cp.add_argument('arg3', arg_type=int, required=True)
    with pytest.raises(RequiredArgumentNotFoundException):
        parsed = cp.parse(path='test_files/simple_example.json')


def test_nested_conf():
    cp = ConfParse()
    cp.add_argument('arg11', arg_type=str)
    cp_main = ConfParse()
    cp_main.add_argument('arg1', arg_type=str)
    cp_main.add_sub_section('sub_section1', cp)
    parsed = cp_main.parse('test_files/nested.json')
    assert parsed.arg1 == 'val1'

def test_non_required_subconf():
    cp = ConfParse(required=False)
    cp.add_argument('arg11', arg_type=str)
    cp_main = ConfParse()
    cp_main.add_argument('arg1', arg_type=str)
    cp_main.add_sub_section('sub_section2', cp)
    parsed = cp_main.parse('test_files/nested.json')
    assert parsed.arg1 == 'val1'

def test_save_example():
    cp=ConfParse()
    cp.add_argument('arg11', arg_type=str)
    cp_main = ConfParse()
    cp_main.add_argument('arg1', arg_type=str)
    cp_main.add_sub_section('sub_section1', cp)
    cp_main.save_example('test_save_example.json')