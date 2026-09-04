import java.util.*;

public class BugFixSandbox {

    // Bug 1: Off-by-one in binary search
    public static int buggyBinarySearch(int[] arr, int target) {
        int lo = 0, hi = arr.length;
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (arr[mid] == target) return mid;
            else if (arr[mid] < target) lo = mid;
            else hi = mid;
        }
        return -1;
    }

    public static int fixedBinarySearch(int[] arr, int target) {
        int lo = 0, hi = arr.length - 1;
        while (lo <= hi) {
            int mid = (lo + hi) / 2;
            if (arr[mid] == target) return mid;
            else if (arr[mid] < target) lo = mid + 1;
            else hi = mid - 1;
        }
        return -1;
    }

    // Bug 2: Wrong index in string reversal
    public static String buggyReverse(String s) {
        char[] chars = s.toCharArray();
        for (int i = 0; i < chars.length; i++) {
            char temp = chars[i];
            chars[i] = chars[chars.length - i];
            chars[chars.length - i] = temp;
        }
        return new String(chars);
    }

    public static String fixedReverse(String s) {
        char[] chars = s.toCharArray();
        for (int i = 0; i < chars.length / 2; i++) {
            char temp = chars[i];
            chars[i] = chars[chars.length - 1 - i];
            chars[chars.length - 1 - i] = temp;
        }
        return new String(chars);
    }

    // Bug 3: Wrong offset in array rotation
    public static int[] buggyRotate(int[] arr, int k) {
        int n = arr.length;
        int[] result = new int[n];
        for (int i = 0; i < n; i++) {
            result[(i + k) % n] = arr[i];
        }
        return result;
    }

    public static int[] fixedRotate(int[] arr, int k) {
        int n = arr.length;
        k = k % n;
        int[] result = new int[n];
        for (int i = 0; i < n; i++) {
            result[i] = arr[(n - k + i) % n];
        }
        return result;
    }

    // Bug 4: Wrong comparison in palindrome check
    public static boolean buggyIsPalindrome(String s) {
        int left = 0, right = s.length();
        while (left < right) {
            if (s.charAt(left) != s.charAt(right)) return false;
            left++;
            right--;
        }
        return true;
    }

    public static boolean fixedIsPalindrome(String s) {
        int left = 0, right = s.length() - 1;
        while (left < right) {
            if (s.charAt(left) != s.charAt(right)) return false;
            left++;
            right--;
        }
        return true;
    }

    // Bug 5: Wrong recurrence in Fibonacci
    public static long buggyFibonacci(int n) {
        if (n <= 0) return 0;
        if (n == 1) return 1;
        return buggyFibonacci(n - 1) + buggyFibonacci(n - 2);
    }

    public static long fixedFibonacci(int n) {
        if (n <= 0) return 0;
        if (n == 1) return 1;
        long[] memo = new long[n + 1];
        memo[0] = 0;
        memo[1] = 1;
        for (int i = 2; i <= n; i++) {
            memo[i] = memo[i - 1] + memo[i - 2];
        }
        return memo[n];
    }

    public static void main(String[] args) {
        System.out.println("=== Bug Fix Sandbox ===");

        // Test binary search
        int[] arr = {1, 2, 3, 4, 5};
        System.out.println("Buggy BS: " + buggyBinarySearch(arr, 3));
        System.out.println("Fixed BS: " + fixedBinarySearch(arr, 3));

        // Test reverse
        System.out.println("Buggy Rev: " + buggyReverse("hello"));
        System.out.println("Fixed Rev: " + fixedReverse("hello"));

        // Test palindrome
        System.out.println("Buggy Pal: " + buggyIsPalindrome("racecar"));
        System.out.println("Fixed Pal: " + fixedIsPalindrome("racecar"));

        // Test fibonacci
        System.out.println("Buggy Fib(5): " + buggyFibonacci(5));
        System.out.println("Fixed Fib(5): " + fixedFibonacci(5));
    }
}
