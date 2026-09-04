import java.util.*;

public class TestRunner {

    public static class TestResult {
        public final String testName;
        public final boolean passed;
        public final Object expected;
        public final Object actual;
        public final long executionTimeMs;

        public TestResult(String testName, boolean passed, Object expected, Object actual, long executionTimeMs) {
            this.testName = testName;
            this.passed = passed;
            this.expected = expected;
            this.actual = actual;
            this.executionTimeMs = executionTimeMs;
        }

        @Override
        public String toString() {
            String status = passed ? "PASS" : "FAIL";
            return String.format("[%s] %s (expected=%s, actual=%s, time=%dms)",
                    status, testName, expected, actual, executionTimeMs);
        }
    }

    public static TestResult runTest(String testName, Runnable testBody) {
        long start = System.nanoTime();
        try {
            testBody.run();
            long elapsed = (System.nanoTime() - start) / 1_000_000;
            return new TestResult(testName, true, "no exception", "no exception", elapsed);
        } catch (AssertionError e) {
            long elapsed = (System.nanoTime() - start) / 1_000_000;
            return new TestResult(testName, false, "no exception", e.getMessage(), elapsed);
        } catch (Exception e) {
            long elapsed = (System.nanoTime() - start) / 1_000_000;
            return new TestResult(testName, false, "no exception", "Exception: " + e.getMessage(), elapsed);
        }
    }

    public static String generateReport(List<TestResult> results) {
        StringBuilder sb = new StringBuilder();
        sb.append("=== Test Report ===\n");
        sb.append(String.format("Total: %d\n", results.size()));

        long passed = results.stream().filter(r -> r.passed).count();
        long failed = results.size() - passed;

        sb.append(String.format("Passed: %d\n", passed));
        sb.append(String.format("Failed: %d\n", failed));
        sb.append(String.format("Pass Rate: %.1f%%\n", (passed * 100.0 / results.size())));
        sb.append("\n");

        for (TestResult result : results) {
            sb.append(result.toString()).append("\n");
        }

        return sb.toString();
    }
}
