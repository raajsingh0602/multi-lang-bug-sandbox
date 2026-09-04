"""Tests for the Python Bug Fixer."""

import os
import sys
import json
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from python.src.bug_fixer import PythonBugFixer


@pytest.fixture
def fixer():
    return PythonBugFixer()


class TestPythonBugFixer:
    def test_analyze_off_by_one(self, fixer):
        code = "def bs(arr, target):\n    lo, hi = 0, len(arr)\n    while lo < hi:"
        result = fixer.analyze_bug(code)
        assert result["bug_type"] == "off-by-one"
        assert result["confidence"] > 0

    def test_analyze_type_error(self, fixer):
        code = 'def greet(name, age):\n    return "Hello " + name + ", age: " + age'
        result = fixer.analyze_bug(code)
        assert result["bug_type"] == "type_error"

    def test_load_scenarios(self, fixer):
        scenario_path = os.path.join(os.path.dirname(__file__), "..", "python", "src", "bug_scenarios.json")
        if os.path.isfile(scenario_path):
            fixer.load_bug_scenarios(scenario_path)
            assert len(fixer.bug_scenarios) == 5

    def test_validate_correctness_pass(self, fixer):
        code = "def add(a, b):\n    return a + b"
        test_cases = [
            {"id": "t1", "input": [1, 2], "expected_output": 3},
            {"id": "t2", "input": [0, 0], "expected_output": 0},
        ]
        result = fixer.validate_correctness(code, test_cases)
        assert result["all_pass"] is True
        assert result["passed"] == 2

    def test_validate_correctness_fail(self, fixer):
        code = "def subtract(a, b):\n    return a + b"
        test_cases = [
            {"id": "t1", "input": [5, 3], "expected_output": 2},
        ]
        result = fixer.validate_correctness(code, test_cases)
        assert result["all_pass"] is False

    def test_test_fix(self, fixer):
        buggy = "def add(a, b):\n    return a - b"
        fixed = "def add(a, b):\n    return a + b"
        test_cases = [
            {"id": "t1", "input": [1, 2], "expected_output": 3},
            {"id": "t2", "input": [5, 3], "expected_output": 8},
        ]
        result = fixer.test_fix(buggy, fixed, test_cases)
        assert result["improvement"] > 0
        assert result["fixed_passed"] == 2
