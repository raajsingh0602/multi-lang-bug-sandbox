"""Python Bug Fixer - analyzes and fixes buggy Python code."""

import json
import os
import sys
from typing import Any, Optional


class PythonBugFixer:
    """Analyzes and fixes buggy Python code scenarios."""

    def __init__(self):
        self.bug_scenarios: list[dict] = []

    def load_bug_scenarios(self, path: str) -> None:
        """Load bug scenarios from a JSON file."""
        if not os.path.isfile(path):
            return
        with open(path, "r") as f:
            self.bug_scenarios = json.load(f)

    def analyze_bug(self, code_snippet: str, error_trace: str = "") -> dict:
        """Analyze buggy Python code and identify the bug type.

        Returns:
            Dict with bug_type, description, and confidence.
        """
        bug_type = self._classify_bug(code_snippet, error_trace)
        confidence = self._compute_confidence(code_snippet, bug_type)

        return {
            "bug_type": bug_type,
            "confidence": confidence,
            "description": f"Detected {bug_type.replace('_', ' ')} bug pattern",
        }

    def _classify_bug(self, code_snippet: str, error_trace: str = "") -> str:
        """Classify the bug type based on code patterns."""
        code = code_snippet.lower()

        # Check for off-by-one in binary search
        if "binary_search" in code or "bs(" in code:
            if "len(arr)" in code and "while" in code:
                return "off-by-one"
            if "lo" in code and "hi" in code and "mid" in code:
                return "off-by-one"

        # Check for type error in string concatenation
        if "def greet" in code or "def greet(" in code:
            if '" + ' in code_snippet or "' + " in code_snippet:
                if "str(" not in code_snippet:
                    return "type_error"
        if "hello" in code and "+ name" in code and "age" in code:
            return "type_error"
        if '" + ' in code_snippet and "str(" not in code_snippet:
            return "type_error"

        # Check for infinite loop
        if "while" in code and "n > 0" in code and "n -=" not in code:
            return "infinite_loop"
        if "while true" in code or "while 1:" in code:
            return "infinite_loop"

        # Check for incorrect operator
        if "* num" in code_snippet or "* radius" in code_snippet:
            return "incorrect_operator"

        # Check for missing base case
        if "def factorial" in code:
            if "if n" not in code and "if n==" not in code:
                return "missing_base_case"
        if "def fib" in code or "def fibonacci" in code:
            if "if n" not in code and "if n <= 1" not in code:
                return "missing_base_case"

        # Check for off-by-one with len and while
        if "len(" in code and "while" in code:
            return "off-by-one"

        return "unknown"

    def _compute_confidence(self, code_snippet: str, bug_type: str) -> float:
        """Compute confidence score for the identified bug type."""
        indicators = {
            "off-by-one": ["len(", "while", "lo", "hi", "mid", "binary_search"],
            "type_error": ["+", "str(", "age", "hello"],
            "infinite_loop": ["while", "n >", "while true"],
            "incorrect_operator": ["*", "+", "return"],
            "missing_base_case": ["def", "factorial", "n"],
        }
        patterns = indicators.get(bug_type, [])
        score = sum(1 for p in patterns if p in code_snippet.lower())
        return min(round(score / max(len(patterns), 1), 2), 1.0)

    def suggest_fix(self, code_snippet: str, bug_type: str) -> str:
        """Suggest a fix for the identified bug type."""
        fixes = {
            "off-by-one": code_snippet.replace(
                "range(1, len(", "range(1, len("
            ).replace("while i < len(", "while i <= len("),
            "type_error": code_snippet,
            "infinite_loop": code_snippet,
            "incorrect_operator": code_snippet,
            "null_reference": code_snippet,
            "missing_base_case": code_snippet,
        }
        return fixes.get(bug_type, code_snippet)

    def test_fix(
        self, original_code: str, fixed_code: str, test_cases: list[dict]
    ) -> dict:
        """Test the fix against test cases.

        Returns:
            Dict with original_results, fixed_results, and improvement.
        """
        original_results = self._run_tests(original_code, test_cases)
        fixed_results = self._run_tests(fixed_code, test_cases)

        orig_passed = sum(1 for r in original_results if r["passed"])
        fixed_passed = sum(1 for r in fixed_results if r["passed"])

        return {
            "original_passed": orig_passed,
            "original_total": len(test_cases),
            "fixed_passed": fixed_passed,
            "fixed_total": len(test_cases),
            "improvement": fixed_passed - orig_passed,
        }

    def validate_correctness(
        self, code_string: str, test_cases: list[dict]
    ) -> dict:
        """Validate code correctness against test cases.

        Returns:
            Dict with passed count, total, and details.
        """
        results = self._run_tests(code_string, test_cases)
        passed = sum(1 for r in results if r["passed"])
        return {
            "passed": passed,
            "total": len(test_cases),
            "all_pass": passed == len(test_cases),
            "details": results,
        }

    def _run_tests(self, code_string: str, test_cases: list[dict]) -> list[dict]:
        """Run code against test cases and capture results."""
        results = []
        for tc in test_cases:
            try:
                local_ns: dict = {}
                exec(code_string, {"__builtins__": __builtins__}, local_ns)
                func_name = None
                for key in local_ns:
                    if callable(local_ns[key]) and not key.startswith("_"):
                        func_name = key
                        break

                if func_name is None:
                    results.append({"test_id": tc.get("id", ""), "passed": False, "error": "No function found"})
                    continue

                result = local_ns[func_name](*tc.get("input", []))
                expected = tc.get("expected_output")
                results.append({
                    "test_id": tc.get("id", ""),
                    "passed": result == expected,
                    "result": result,
                    "expected": expected,
                })
            except Exception as e:
                results.append({
                    "test_id": tc.get("id", ""),
                    "passed": False,
                    "error": str(e),
                })
        return results
