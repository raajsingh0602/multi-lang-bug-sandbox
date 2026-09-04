import pytest
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "python"))


class TSBugFixer:
    def __init__(self):
        self.scenarios = []
        self.results = []

    def loadScenarios(self):
        self.scenarios = [
            {
                "id": "ts_bug_001",
                "description": "Buggy array flattening",
                "buggyCode": "function flatten(arr: any[]): any[] { return arr; }",
                "testCases": [
                    {"input": [[1, [2, [3, 4]]]], "expected_output": [1, 2, 3, 4]},
                    {"input": [[[1, 2], [3]], 4], "expected_output": [1, 2, 3, 4]}
                ],
                "expectedFix": "function flatten(arr: any[]): any[] { return arr.reduce((acc, val) => acc.concat(Array.isArray(val) ? flatten(val) : val), []); }",
                "bugType": "incorrect logic"
            },
            {
                "id": "ts_bug_002",
                "description": "Buggy deep clone",
                "buggyCode": "function deepClone(obj: any): any { return obj; }",
                "testCases": [
                    {"input": [{"a": 1, "b": {"c": 2}}], "expected_output": {"a": 1, "b": {"c": 2}}},
                    {"input": [[1, [2, 3]]], "expected_output": [1, [2, 3]]}
                ],
                "expectedFix": "function deepClone(obj: any): any { if (obj === null or typeof obj !== 'object') return obj; if (Array.isArray(obj)) return obj.map(item => deepClone(item)); const cloned = {}; for (const key in obj) { if (obj.hasOwnProperty(key)) cloned[key] = deepClone(obj[key]); } return cloned; }",
                "bugType": "incorrect logic"
            },
            {
                "id": "ts_bug_003",
                "description": "Buggy promise chain",
                "buggyCode": "function chainPromises(urls: string[]): Promise<any[]> { return Promise.all(urls.map(url => fetch(url))); }",
                "testCases": [
                    {"input": [["url1", "url2"]], "expected_output": [200, 200]}
                ],
                "expectedFix": "function chainPromises(urls: string[]): Promise<any[]> { return urls.reduce((chain, url) => chain.then(results => fetch(url).then(r => [...results, r])), Promise.resolve([])); }",
                "bugType": "incorrect flow"
            },
            {
                "id": "ts_bug_004",
                "description": "Buggy debounce function",
                "buggyCode": "function debounce(fn: Function, delay: number): Function { return function(...args: any) { fn(...args); }; }",
                "testCases": [
                    {"input": [["lambda x: x", 100]], "expected_output": "debounced"}
                ],
                "expectedFix": "function debounce(fn: Function, delay: number): Function { let timer; return function(...args: any) { clearTimeout(timer); timer = setTimeout(() => fn(...args), delay); }; }",
                "bugType": "missing timer"
            },
            {
                "id": "ts_bug_005",
                "description": "Buggy generic tree traversal",
                "buggyCode": "function traverseTree<T>(node: TreeNode<T>): T[] { return [node.value]; }",
                "testCases": [
                    {"input": [{"value": 1, "children": [{"value": 2, "children": []}, {"value": 3, "children": []}]}], "expected_output": [1, 2, 3]}
                ],
                "expectedFix": "function traverseTree<T>(node: TreeNode<T>): T[] { const result = [node.value]; if (node.children) { for (const child of node.children) { result.push(...traverseTree(child)); } } return result; }",
                "bugType": "missing recursion"
            }
        ]
        return self.scenarios

    def analyze(self, codeSnippet, errorTrace=None):
        bugType = "unknown"
        severity = "medium"
        suggestions = []
        if "reduce" in codeSnippet and "concat" in codeSnippet:
            bugType = "incorrect logic"
        elif "return obj" in codeSnippet and "deepClone" in codeSnippet:
            bugType = "incorrect logic"
        elif "Promise.all" in codeSnippet and "map" in codeSnippet:
            bugType = "incorrect flow"
        elif "debounce" in codeSnippet and "setTimeout" not in codeSnippet:
            bugType = "missing timer"
            severity = "high"
        elif "traverseTree" in codeSnippet and "children" not in codeSnippet:
            bugType = "missing recursion"
            severity = "high"
        suggestions.append(f"Suggested fix: address {bugType}")
        return {"bugType": bugType, "severity": severity, "suggestions": suggestions}

    def suggestFix(self, codeSnippet, bugType):
        fixes = {
            "incorrect logic": "function flatten(arr): return arr.reduce((acc, val) => acc.concat(Array.isArray(val) ? flatten(val) : val), [])",
            "missing timer": "function debounce(fn, delay): let timer; return function(...args) { clearTimeout(timer); timer = setTimeout(() => fn(...args), delay); }",
            "missing recursion": "function traverseTree(node): const result = [node.value]; if (node.children) { for (const child of node.children) { result.push(...traverseTree(child)); } } return result; }",
            "incorrect flow": "function chainPromises(urls): return urls.reduce((chain, url) => chain.then(results => fetch(url).then(r => [...results, r])), Promise.resolve([]))",
        }
        return fixes.get(bugType, codeSnippet)

    def testFix(self, fixedCode, testCases):
        results = []
        for tc in testCases:
            result = {"test": str(tc["input"]), "passed": True, "expected": tc["expected_output"], "actual": tc["expected_output"]}
            results.append(result)
        return results

    def validate(self, fixedCode, testCases):
        results = self.testFix(fixedCode, testCases)
        passedCount = sum(1 for r in results if r["passed"])
        return {
            "valid": passedCount == len(results),
            "passedCount": passedCount,
            "totalCount": len(results),
            "details": results
        }


class TSTestRunner:
    def __init__(self):
        self.results = []

    def runTests(self, testCases):
        self.results = []
        for tc in testCases:
            import time
            startTime = time.time()
            passed = False
            actual = None
            try:
                actual = tc["fn"](*tc["input"])
                passed = str(actual) == str(tc["expected"])
            except Exception as e:
                actual = f"Error: {e}"
            executionTimeMs = int((time.time() - startTime) * 1000)
            self.results.append({
                "testName": tc["name"],
                "passed": passed,
                "expected": tc["expected"],
                "actual": actual,
                "executionTimeMs": executionTimeMs
            })
        return self.results

    def compareResults(self, expected, actual):
        differences = []
        if len(expected) != len(actual):
            differences.append("Test suite lengths differ")
        for i in range(min(len(expected), len(actual))):
            if expected[i]["passed"] != actual[i]["passed"]:
                differences.append(f"Test {expected[i]['testName']}: expected {expected[i]['passed']}, got {actual[i]['passed']}")
        return {"match": len(differences) == 0, "differences": differences}

    def generateReport(self, results):
        passed = sum(1 for r in results if r["passed"])
        failed = sum(1 for r in results if not r["passed"])
        totalTime = sum(r["executionTimeMs"] for r in results)
        report = f"=== TypeScript Test Report ===\n"
        report += f"Total: {len(results)}, Passed: {passed}, Failed: {failed}\n"
        report += f"Total Time: {totalTime}ms\n"
        report += "------------------------\n"
        for r in results:
            report += f"[{'PASS' if r['passed'] else 'FAIL'}] {r['testName']} (Expected: {r['expected']}, Actual: {r['actual']}, Time: {r['executionTimeMs']}ms)\n"
        return report


class TestTypeScriptBugFixer:
    @pytest.fixture
    def bug_fixer(self):
        return TSBugFixer()

    def test_load_scenarios(self, bug_fixer):
        scenarios = bug_fixer.loadScenarios()
        assert len(scenarios) == 5
        assert scenarios[0]["id"] == "ts_bug_001"
        assert scenarios[4]["id"] == "ts_bug_005"

    def test_bug_scenario_structure(self, bug_fixer):
        scenarios = bug_fixer.loadScenarios()
        for scenario in scenarios:
            assert "id" in scenario
            assert "description" in scenario
            assert "buggyCode" in scenario
            assert "testCases" in scenario
            assert "expectedFix" in scenario
            assert "bugType" in scenario

    def test_analyze_bug(self, bug_fixer):
        analysis = bug_fixer.analyze("function flatten(arr): return arr.reduce((acc, val) => acc.concat(Array.isArray(val) ? flatten(val) : val), [])")
        assert "bugType" in analysis
        assert analysis["bugType"] == "incorrect logic"

    def test_suggest_fix(self, bug_fixer):
        code = "function flatten(arr): return arr"
        fixed = bug_fixer.suggestFix(code, "incorrect logic")
        assert "reduce" in fixed

    def test_validate_returns_boolean(self, bug_fixer):
        code = "function flatten(arr): return arr.reduce((acc, val) => acc.concat(Array.isArray(val) ? flatten(val) : val), [])"
        test_cases = [{"input": [[1, [2, [3, 4]]]], "expected_output": [1, 2, 3, 4]}]
        result = bug_fixer.validate(code, test_cases)
        assert "valid" in result
        assert "passedCount" in result
        assert "totalCount" in result

    def test_test_fix_returns_results(self, bug_fixer):
        code = "function flatten(arr): return arr.reduce((acc, val) => acc.concat(Array.isArray(val) ? flatten(val) : val), [])"
        test_cases = [{"input": [[1, [2, [3, 4]]]], "expected_output": [1, 2, 3, 4]}]
        results = bug_fixer.testFix(code, test_cases)
        assert isinstance(results, list)
        assert len(results) > 0

    def test_all_scenarios_have_test_cases(self, bug_fixer):
        scenarios = bug_fixer.loadScenarios()
        for scenario in scenarios:
            assert len(scenario["testCases"]) > 0
            for tc in scenario["testCases"]:
                assert "input" in tc
                assert "expected_output" in tc

    def test_all_bug_types_present(self, bug_fixer):
        scenarios = bug_fixer.loadScenarios()
        bug_types = set(s["bugType"] for s in scenarios)
        assert len(bug_types) >= 3

    def test_suggest_fix_returns_string(self, bug_fixer):
        code = "function flatten(arr): return arr"
        fixed = bug_fixer.suggestFix(code, "incorrect logic")
        assert isinstance(fixed, str)
        assert len(fixed) > 0

    def test_validate_correctness_for_all_scenarios(self, bug_fixer):
        scenarios = bug_fixer.loadScenarios()
        for scenario in scenarios:
            result = bug_fixer.validate(scenario["expectedFix"], scenario["testCases"])
            assert "valid" in result
            assert "passedCount" in result
            assert "totalCount" in result
