export interface BugScenario {
    id: string;
    description: string;
    buggyCode: string;
    testCases: TestCase[];
    expectedFix: string;
}

export interface TestCase {
    id: string;
    input: any[];
    expectedOutput: any;
}

export interface TestResult {
    testName: string;
    passed: boolean;
    expected: any;
    actual: any;
    executionTimeMs: number;
}

export interface EvaluationResult {
    scenarioId: string;
    totalTests: number;
    passedTests: number;
    failedTests: number;
    results: TestResult[];
}

export class TSBugFixer {
    private scenarios: BugScenario[] = [];

    loadScenarios(): BugScenario[] {
        return this.scenarios;
    }

    analyze(code: string): { bugType: string; confidence: number } {
        const patterns: Record<string, string[]> = {
            "array-index": ["length", "[i]", "[arr.length]"],
            "async-error": ["async", "await", "Promise"],
            "type-coercion": ["==", "!=", "typeof"],
            "off-by-one": ["<=", ">=", "length - 1"],
            "closure-scope": ["let", "var", "const"],
        };

        let bestType = "unknown";
        let bestScore = 0;

        for (const [bugType, pats] of Object.entries(patterns)) {
            const score = pats.filter((p) => code.includes(p)).length;
            if (score > bestScore) {
                bestScore = score;
                bestType = bugType;
            }
        }

        return {
            bugType: bestType,
            confidence: Math.min(bestScore / 3, 1.0),
        };
    }

    suggestFix(code: string, bugType: string): string {
        return code;
    }

    testFix(
        originalCode: string,
        fixedCode: string,
        testCases: TestCase[]
    ): { original: EvaluationResult; fixed: EvaluationResult } {
        const original = this.validate(originalCode, testCases, "original");
        const fixed = this.validate(fixedCode, testCases, "fixed");
        return { original, fixed };
    }

    validate(
        code: string,
        testCases: TestCase[],
        scenarioId: string = "test"
    ): EvaluationResult {
        const results: TestResult[] = [];

        for (const tc of testCases) {
            const start = Date.now();
            try {
                const fn = new Function("return " + code)();
                const actual = fn(...tc.input);
                const elapsed = Date.now() - start;
                const passed = JSON.stringify(actual) === JSON.stringify(tc.expectedOutput);
                results.push({
                    testName: tc.id,
                    passed,
                    expected: tc.expectedOutput,
                    actual,
                    executionTimeMs: elapsed,
                });
            } catch (e: any) {
                results.push({
                    testName: tc.id,
                    passed: false,
                    expected: tc.expectedOutput,
                    actual: `Error: ${e.message}`,
                    executionTimeMs: Date.now() - start,
                });
            }
        }

        const passedCount = results.filter((r) => r.passed).length;
        return {
            scenarioId,
            totalTests: testCases.length,
            passedTests: passedCount,
            failedTests: testCases.length - passedCount,
            results,
        };
    }
}

export class TSTestRunner {
    private results: TestResult[] = [];

    runTests(
        code: string,
        testCases: { input: any[]; expected: any; name: string }[]
    ): TestResult[] {
        const results: TestResult[] = [];

        for (const tc of testCases) {
            const start = Date.now();
            try {
                const fn = new Function("return " + code)();
                const actual = fn(...tc.input);
                const elapsed = Date.now() - start;
                results.push({
                    testName: tc.name,
                    passed: JSON.stringify(actual) === JSON.stringify(tc.expected),
                    expected: tc.expected,
                    actual,
                    executionTimeMs: elapsed,
                });
            } catch (e: any) {
                results.push({
                    testName: tc.name,
                    passed: false,
                    expected: tc.expected,
                    actual: `Error: ${e.message}`,
                    executionTimeMs: Date.now() - start,
                });
            }
        }

        this.results = results;
        return results;
    }

    compareResults(results: TestResult[]): { passed: number; failed: number } {
        return {
            passed: results.filter((r) => r.passed).length,
            failed: results.filter((r) => !r.passed).length,
        };
    }

    generateReport(results: TestResult[]): string {
        const lines = ["=== TypeScript Test Report ===", ""];
        for (const r of results) {
            const status = r.passed ? "PASS" : "FAIL";
            lines.push(`[${status}] ${r.testName} - expected: ${r.expected}, actual: ${r.actual} (${r.executionTimeMs}ms)`);
        }
        const passed = results.filter((r) => r.passed).length;
        lines.push("");
        lines.push(`Passed: ${passed}/${results.length}`);
        return lines.join("\n");
    }
}
