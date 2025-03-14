#!/usr/bin/env python3

import pytest
import autoclasstoc
import parametrize_from_file as pff

with_autoclasstoc = pff.Namespace('from autoclasstoc import *')

class MockObj:
    data_attr = None
    _private_data_attr = None

    class InnerClass:
        pass
    
    def __init__(self):
        pass

    def method(self):
        pass

    def _private_method(self):
        pass

class EmptyObj:
    pass

@pytest.mark.parametrize(
        'name, pattern, expected', [
            ('', 'ab', False),
            ('ab', 'ab', True),
            ('ba', 'ab', False),

            ('', ['ab', 'cd'], False),
            ('ab', ['ab', 'cd'], True),
            ('ba', ['ab', 'cd'], False),
            ('cd', ['ab', 'cd'], True),
            ('dc', ['ab', 'cd'], False),
            ('abcd', ['ab', 'cd'], True),
            ('abdc', ['ab', 'cd'], True),
            ('bacd', ['ab', 'cd'], False),
            ('bacd', ['ab', '.*cd'], True),
            ('badc', ['ab', 'cd'], False),

            # Test some real-world patterns.
            ('__init__', '__', True),
            ('__len__', '__', True),
            ('foo', '__', False),
            ('_bar', '__', False),

            ('__init__', ['__', 'on'], True),
            ('__len__', ['__', 'on'], True),
            ('foo', ['__', 'on'], False),
            ('_bar', ['__', 'on'], False),
            ('on_off', ['__', 'on'], True),
            ('off_on', ['__', 'on'], False),
            ('off_on', ['__', '.*on'], True),
    ]
)
def test_does_match(name, pattern, expected):
    assert autoclasstoc.does_match(name, pattern) == expected


@pff.parametrize
def test_section_predicate(section, expected):
    # For the sake of making the expected values easy to predict, remove any 
    # attributes that python automatically adds to new classes.
    attrs = {
            k: v
            for k, v in MockObj.__dict__.items()
            if k not in EmptyObj.__dict__
    }
    section_cls = with_autoclasstoc.exec(section, get='MockSection')
    section = section_cls('state', 'cls')
    hits = autoclasstoc.utils.filter_attrs(attrs, section.predicate)
    assert set(hits) == set(expected)

