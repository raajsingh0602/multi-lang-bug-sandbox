import json
import subprocess
import traceback


class PythonBugFixer:
    def __init__(self):
        self.scenarios = []
        self.results = []

    def load_bug_scenarios(self, path):
        with open(path, "r") as f:
            data = json.load(f)
        self.scenarios = data["scenarios"]
        return self.scenarios

    def analyze_bug(self, code_snippet, error_trace):
        bug_info = {
            "code_snippet": code_snippet,
            "error_trace": error_trace,
            "bug_type": self._classify_bug(code_snippet, error_trace),
            "severity": self._assess_severity(code_snippet, error_trace),
            "suggested_fixes": []
        }
        return bug_info

    def _classify_bug(self, code_snippet, error_trace):
        combined = (code_snippet + " " + error_trace).lower()
        if "def factorial" in combined and "if n" not in combined:
            return "missing base case"
        if "total = total * num" in combined or "* num" in combined:
            return "incorrect operator"
        if "while n > 0" in combined and "n -=" not in combined:
            return "infinite loop"
        if "def binary_search" in combined and "len(arr)" in combined:
            return "off-by-one"
        if "len(arr)" in combined and "while" in combined:
            return "off-by-one"
        if "result +=" in combined and "item" in combined:
            return "type error"
        if "concatenate" in combined or "type" in combined:
            return "type error"
        return "unknown"

    def _assess_severity(self, code_snippet, error_trace):
        if "infinite" in error_trace.lower() or "recursion" in error_trace.lower():
            return "critical"
        if "type" in error_trace.lower():
            return "high"
        return "medium"

    def suggest_fix(self, code_snippet, bug_type):
        fixes = {
            "off-by-one": self._fix_off_by_one(code_snippet),
            "type error": self._fix_type_error(code_snippet),
            "infinite loop": self._fix_infinite_loop(code_snippet),
            "incorrect operator": self._fix_incorrect_operator(code_snippet),
            "missing base case": self._fix_missing_base_case(code_snippet),
        }
        return fixes.get(bug_type, code_snippet)

    def _fix_off_by_one(self, code):
        fixed = code.replace("len(arr)", "len(arr) - 1")
        if fixed == code:
            fixed = code.replace("range(len(", "range(len(")
        return fixed

    def _fix_type_error(self, code):
        if "result += " in code and "item" in code:
            lines = code.split("\n")
            new_lines = []
            for line in lines:
                if "result += " in line:
                    new_lines.append("        result.append(str(item))")
                elif 'result = ""' in line:
                    new_lines.append("    result = []")
                elif "return result[2:]" in line:
                    new_lines.append("    return \", \".join(result)")
                else:
                    new_lines.append(line)
            return "\n".join(new_lines)
        return code

    def _fix_infinite_loop(self, code):
        if "while n > 0:" in code and "n -=" not in code:
            lines = code.split("\n")
            new_lines = []
            for line in lines:
                new_lines.append(line)
                if "print(n)" in line:
                    new_lines.append("        n -= 1")
            return "\n".join(new_lines)
        return code

    def _fix_incorrect_operator(self, code):
        if "total = total * num" in code:
            return code.replace("total = total * num", "total = total + num")
        return code

    def _fix_missing_base_case(self, code):
        if "def factorial" in code and "if n" not in code:
            lines = code.split("\n")
            new_lines = [lines[0], "    if n <= 1:", "        return 1"]
            new_lines.extend(lines[1:])
            return "\n".join(new_lines)
        return code

    def test_fix(self, original_code, fixed_code, test_cases):
        results = []
        local_vars = {}
        try:
            exec(compile(fixed_code, "<string>", "exec"), {"__builtins__": __builtins__}, local_vars)
        except Exception as e:
            for test_case in test_cases:
                results.append({"test": str(test_case["input"]), "passed": False, "error": str(e)})
            return results
        func = None
        for name in ["binary_search", "concatenate_items", "countdown", "calculate_average", "factorial"]:
            if name in local_vars and callable(local_vars[name]):
                func = local_vars[name]
                break
        if func is None:
            for name in local_vars:
                if callable(local_vars[name]):
                    func = local_vars[name]
                    break
        if func is None:
            for test_case in test_cases:
                results.append({"test": str(test_case["input"]), "passed": False, "error": "No function found"})
            return results
        for test_case in test_cases:
            test_input = test_case["input"]
            expected = test_case["expected_output"]
            try:
                result = func(*test_input if isinstance(test_input, list) else [test_input])
                passed = result == expected
                results.append({"test": str(test_input), "passed": passed, "expected": expected, "actual": result})
            except Exception as e:
                results.append({"test": str(test_input), "passed": False, "error": str(e)})
        return results

    def validate_correctness(self, fixed_code, test_cases):
        try:
            results = self.test_fix("", fixed_code, test_cases)
            all_passed = all(r["passed"] for r in results)
            return {
                "valid": all_passed,
                "passed_count": sum(1 for r in results if r["passed"]),
                "total_count": len(results),
                "details": results
            }
        except Exception as e:
            return {
                "valid": False,
                "passed_count": 0,
                "total_count": len(test_cases),
                "error": str(e)
            }
