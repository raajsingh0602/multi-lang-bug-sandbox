# Bug Scenarios Documentation

This document describes all bug scenarios used in the Multi-Language Bug Sandbox.

## Overview

We have **15+ bug scenarios** across **3 languages** (Java, Python, TypeScript) covering **5 bug categories**.

## Bug Categories

### 1. Off-by-One Errors
Index calculation errors that cause array bounds violations or incorrect results.

- **Python**: Binary search using `len(arr)` instead of `len(arr) - 1`
- **Java**: Binary search high bound, string reversal using `chars[n]` instead of `chars[n-1-i]`, palindrome check using `s.length()` instead of `s.length() - 1`
- **TypeScript**: Array flattening incorrect logic

### 2. Type Errors
Operations performed on incompatible types.

- **Python**: String concatenation with non-string items
- **Java**: Type coercion issues

### 3. Infinite Loops
Missing or incorrect termination conditions.

- **Python**: While loop missing decrement (`n -= 1`)
- **Java**: Recursion without proper base case

### 4. Incorrect Operators
Wrong arithmetic or logical operators.

- **Python**: Using `*` instead of `+` in average calculation
- **Java**: Wrong Fibonacci recurrence relation (`n - 3` instead of `n - 2`)

### 5. Missing Base Case
Recursion without proper termination.

- **Python**: Factorial without `if n <= 1` base case
- **TypeScript**: Tree traversal without recursion on children

## Detailed Scenario List

| ID | Language | Bug Type | Description | Method |
|----|----------|----------|-------------|--------|
| bug_001 | Python | Off-by-one | Binary search high bound | `binary_search` |
| bug_002 | Python | Type error | String concatenation | `concatenate_items` |
| bug_003 | Python | Infinite loop | While loop decrement | `countdown` |
| bug_004 | Python | Incorrect operator | Average calculation | `calculate_average` |
| bug_005 | Python | Missing base case | Factorial recursion | `factorial` |
| java_001 | Java | Off-by-one | Binary search | `buggyBinarySearch` |
| java_002 | Java | Wrong index | String reversal | `buggyStringReversal` |
| java_003 | Java | Wrong offset | Array rotation | `buggyArrayRotation` |
| java_004 | Java | Wrong comparison | Palindrome check | `buggyPalindromeCheck` |
| java_005 | Java | Wrong recurrence | Fibonacci | `buggyFibonacci` |
| ts_001 | TypeScript | Incorrect logic | Array flattening | `flatten` |
| ts_002 | TypeScript | Incorrect logic | Deep clone | `deepClone` |
| ts_003 | TypeScript | Incorrect flow | Promise chain | `chainPromises` |
| ts_004 | TypeScript | Missing timer | Debounce | `debounce` |
| ts_005 | TypeScript | Missing recursion | Tree traversal | `traverseTree` |

## Running Tests

```bash
# Run all Python bug scenario tests
pytest tests/test_python_bugfixer.py -v

# Run all Java bug scenario tests
pytest tests/test_java_bugfixer.py -v

# Run all TypeScript bug scenario tests
pytest tests/test_typescript_bugfixer.py -v

# Run complete sandbox
bash scripts/run_bug_sandbox.sh
```
