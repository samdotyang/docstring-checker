from __future__ import annotations

from docstring_checker import main
from testing.util import get_resource_path

def test_failing_func():
    ret = main([get_resource_path('function_without_docstring')])
    assert ret == 1

def test_passing_func():
    ret = main([get_resource_path('function_with_docstring')])
    assert ret == 0