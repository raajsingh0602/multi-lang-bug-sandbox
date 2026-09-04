export interface TestResult {
    testName: string;
    passed: boolean;
    expected: any;
    actual: any;
    executionTimeMs: number;
}

export interface ScenarioResult {
    scenarioId: string;
    results: TestResult[];
    summary: { passed: number; failed: number; total: number };
}

export class TSTestRunner {
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
            lines.push(`[${status}] ${r.testName}`);
        }
        const passed = results.filter((r) => r.passed).length;
        lines.push(`\nPassed: ${passed}/${results.length}`);
        return lines.join("\n");
    }
}
