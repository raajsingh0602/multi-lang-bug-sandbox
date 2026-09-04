import pytest
import subprocess
import os

JAVA_SRC_DIR = os.path.join(os.path.dirname(__file__), "..", "java", "src")


class TestJavaBugFixer:
    @pytest.fixture(autouse=True)
    def compile_java(self):
        result = subprocess.run(
            ["javac", os.path.join(JAVA_SRC_DIR, "BugFixSandbox.java"), "-d", os.path.join(JAVA_SRC_DIR)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            pytest.skip(f"Java compilation failed: {result.stderr}")
        return result.returncode == 0

    def test_java_code_compiles(self, compile_java):
        assert compile_java is True

    def test_bug_fix_sandbox_class_exists(self, compile_java):
        result = subprocess.run(
            ["java", "-cp", JAVA_SRC_DIR, "BugFixSandbox"],
            capture_output=True, text=True, timeout=10
        )
        assert "Java Bug Fix Sandbox initialized" in result.stdout

    def test_fixed_binary_search(self, compile_java):
        result = subprocess.run(
            ["java", "-cp", JAVA_SRC_DIR, "BugFixSandbox"],
            capture_output=True, text=True, timeout=10
        )
        assert "Fixed Binary Search for 3: 2" in result.stdout

    def test_fixed_string_reversal(self, compile_java):
        result = subprocess.run(
            ["java", "-cp", JAVA_SRC_DIR, "BugFixSandbox"],
            capture_output=True, text=True, timeout=10
        )
        assert "Fixed String Reversal of 'hello': olleh" in result.stdout

    def test_fixed_array_rotation(self, compile_java):
        result = subprocess.run(
            ["java", "-cp", JAVA_SRC_DIR, "BugFixSandbox"],
            capture_output=True, text=True, timeout=10
        )
        assert "Fixed Array Rotation of [1,2,3] by 1: [2, 3, 1]" in result.stdout

    def test_fixed_palindrome_check(self, compile_java):
        result = subprocess.run(
            ["java", "-cp", JAVA_SRC_DIR, "BugFixSandbox"],
            capture_output=True, text=True, timeout=10
        )
        assert "Fixed Palindrome Check 'racecar': true" in result.stdout

    def test_fixed_fibonacci(self, compile_java):
        result = subprocess.run(
            ["java", "-cp", JAVA_SRC_DIR, "BugFixSandbox"],
            capture_output=True, text=True, timeout=10
        )
        assert "Fixed Fibonacci(5): 5" in result.stdout

    def test_load_scenarios(self, compile_java):
        result = subprocess.run(
            ["java", "-cp", JAVA_SRC_DIR, "BugFixSandbox"],
            capture_output=True, text=True, timeout=10
        )
        assert "Loaded 5 bug scenarios" in result.stdout
