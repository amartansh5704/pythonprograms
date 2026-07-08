#!/usr/bin/env python3
"""
=============================================================================
DEBUGGING AND PROFILING DEMONSTRATION PROGRAM
=============================================================================
This program demonstrates:
    - Intentional bugs and how to find them
    - Multiple profiling techniques
    - Memory profiling
    - CPU profiling
    - Line-by-line profiling
    - Logging/debugging techniques
    - Performance comparisons between good and bad implementations
=============================================================================
"""

import cProfile
import pstats
import io
import time
import logging
import traceback
import tracemalloc
import pdb
import sys
import random
import statistics
from functools import wraps
from memory_profiler import profile as memory_profile


# =============================================================================
# LOGGING SETUP
# =============================================================================

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)-8s | %(funcName)-30s | %(message)s',
    handlers=[
        logging.FileHandler("debug_log.txt"),   # Log to file
        logging.StreamHandler(sys.stdout)        # Log to console
    ]
)
logger = logging.getLogger(__name__)


# =============================================================================
# DECORATOR UTILITIES (Timing + Tracing)
# =============================================================================

def timer(func):
    """Decorator: measures and prints how long a function takes."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        elapsed = (end - start) * 1000
        logger.info(f"TIMER >> {func.__name__} took {elapsed:.4f} ms")
        return result
    return wrapper


def trace(func):
    """Decorator: logs function entry, exit, arguments, and return value."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"ENTER >> {func.__name__} | args={args[:2]} kwargs={kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"EXIT  >> {func.__name__} | returned={str(result)[:50]}")
            return result
        except Exception as e:
            logger.error(f"ERROR >> {func.__name__} | exception={e}")
            raise
    return wrapper


# =============================================================================
# SECTION 1: INTENTIONAL BUGS (for debugging demo)
# =============================================================================

class BuggyCalculator:
    """
    This class has several intentional bugs.
    We will use different debugging techniques to find them.
    """

    def buggy_average(self, numbers):
        """
        BUG: Off-by-one error in loop range.
        This skips the FIRST element of the list.
        """
        logger.debug(f"buggy_average called with: {numbers}")
        total = 0
        # BUG IS HERE: range starts at 1, skipping index 0
        for i in range(1, len(numbers)):
            total += numbers[i]
        average = total / len(numbers)
        logger.debug(f"buggy_average result: {average}")
        return average

    def fixed_average(self, numbers):
        """
        FIXED version of the average function.
        """
        logger.debug(f"fixed_average called with: {numbers}")
        total = 0
        # FIXED: range starts at 0
        for i in range(0, len(numbers)):
            total += numbers[i]
        average = total / len(numbers)
        logger.debug(f"fixed_average result: {average}")
        return average

    def buggy_binary_search(self, arr, target):
        """
        BUG: Infinite loop when target is not found.
        mid calculation is wrong causing infinite loop in some cases.
        """
        left = 0
        right = len(arr) - 1

        while left <= right:
            # BUG IS HERE: should be (left + right) // 2
            mid = left + right  # This is wrong! Goes out of bounds
            logger.debug(f"binary_search: left={left}, right={right}, mid={mid}")

            if mid >= len(arr):  # Safety guard so we don't crash
                logger.error(f"mid={mid} is out of bounds! BUG DETECTED.")
                return -1

            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return -1

    def fixed_binary_search(self, arr, target):
        """
        FIXED version of binary search.
        """
        left = 0
        right = len(arr) - 1

        while left <= right:
            mid = (left + right) // 2  # FIXED
            logger.debug(f"binary_search: left={left}, right={right}, mid={mid}")

            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return -1

    def buggy_divide(self, a, b):
        """
        BUG: No handling of division by zero.
        This will raise ZeroDivisionError.
        """
        logger.debug(f"buggy_divide: {a} / {b}")
        return a / b  # BUG: no check for b == 0

    def fixed_divide(self, a, b):
        """
        FIXED: Handles division by zero gracefully.
        """
        logger.debug(f"fixed_divide: {a} / {b}")
        if b == 0:
            logger.warning("Division by zero attempted. Returning None.")
            return None
        return a / b

    def buggy_find_max(self, numbers):
        """
        BUG: Uses wrong comparison operator.
        This returns the MINIMUM, not the maximum.
        """
        if not numbers:
            return None
        max_val = numbers[0]
        for n in numbers[1:]:
            if n < max_val:    # BUG: should be >
                max_val = n
        logger.debug(f"buggy_find_max result: {max_val}")
        return max_val

    def fixed_find_max(self, numbers):
        """FIXED version."""
        if not numbers:
            return None
        max_val = numbers[0]
        for n in numbers[1:]:
            if n > max_val:    # FIXED
                max_val = n
        logger.debug(f"fixed_find_max result: {max_val}")
        return max_val


# =============================================================================
# SECTION 2: PERFORMANCE COMPARISONS (for profiling demo)
# =============================================================================

class SlowAlgorithms:
    """Collection of intentionally slow algorithms to profile."""

    @timer
    def slow_find_duplicates(self, numbers):
        """
        O(n²) approach to finding duplicates.
        Compares every element with every other element.
        """
        logger.info("Running SLOW duplicate finder O(n²)")
        duplicates = []
        n = len(numbers)
        for i in range(n):
            for j in range(i + 1, n):       # Nested loop = O(n²)
                if numbers[i] == numbers[j]:
                    if numbers[i] not in duplicates:
                        duplicates.append(numbers[i])
        return duplicates

    @timer
    def slow_string_concat(self, words):
        """
        Slow string concatenation using + operator.
        Creates a new string object every iteration = O(n²) memory.
        """
        logger.info("Running SLOW string concat")
        result = ""
        for word in words:
            result = result + word + " "    # Creates new string every time!
        return result.strip()

    @timer
    def slow_fibonacci(self, n):
        """
        Exponential O(2^n) recursive Fibonacci.
        Recalculates the same values over and over.
        """
        logger.info(f"Running SLOW Fibonacci for n={n}")
        if n <= 1:
            return n
        return self.slow_fibonacci(n - 1) + self.slow_fibonacci(n - 2)

    @timer
    def slow_is_prime(self, n):
        """
        Naive prime checker O(n) - checks all numbers up to n.
        """
        if n < 2:
            return False
        for i in range(2, n):               # Checks ALL numbers up to n
            if n % i == 0:
                return False
        return True

    @timer
    def slow_sort_search(self, data, targets):
        """
        Searches for each target in unsorted list using linear scan.
        O(n * m) where n=data size, m=targets size.
        """
        logger.info("Running SLOW sort+search")
        results = []
        for target in targets:
            found = False
            for item in data:               # Linear search each time
                if item == target:
                    found = True
                    break
            results.append(found)
        return results


class FastAlgorithms:
    """Optimized versions of the slow algorithms above."""

    @timer
    def fast_find_duplicates(self, numbers):
        """
        O(n) approach using a hash set.
        Single pass through the data.
        """
        logger.info("Running FAST duplicate finder O(n)")
        seen = set()
        duplicates = set()
        for num in numbers:
            if num in seen:
                duplicates.add(num)
            seen.add(num)
        return list(duplicates)

    @timer
    def fast_string_concat(self, words):
        """
        Fast string joining using join().
        Builds the string in one operation.
        """
        logger.info("Running FAST string concat")
        return " ".join(words)              # Single operation, O(n)

    @timer
    def fast_fibonacci(self, n):
        """
        O(n) iterative Fibonacci with memoization concept.
        Each value is calculated only once.
        """
        logger.info(f"Running FAST Fibonacci for n={n}")
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

    @timer
    def fast_is_prime(self, n):
        """
        O(√n) prime checker - only checks up to square root.
        """
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n**0.5) + 1, 2):  # Only up to √n
            if n % i == 0:
                return False
        return True

    @timer
    def fast_sort_search(self, data, targets):
        """
        O((n + m) log n) using a hash set for O(1) lookups.
        """
        logger.info("Running FAST sort+search")
        data_set = set(data)                # O(n) to build
        return [target in data_set for target in targets]  # O(1) per lookup


# =============================================================================
# SECTION 3: MEMORY LEAK DEMONSTRATION
# =============================================================================

class MemoryLeakDemo:
    """Demonstrates common memory leak patterns."""

    def __init__(self):
        self.leaky_cache = {}          # Unbounded cache - will grow forever
        self.event_listeners = []       # Listeners never removed

    def leaky_function(self, n):
        """
        Simulates a memory leak by storing data in an unbounded cache.
        """
        logger.info(f"leaky_function: storing {n} items in cache")
        for i in range(n):
            # Cache grows and is NEVER cleaned up
            key = f"key_{i}_{time.time()}"
            self.leaky_cache[key] = [random.random() for _ in range(100)]
        logger.debug(f"Cache now has {len(self.leaky_cache)} entries")

    def fixed_function(self, n, max_cache_size=1000):
        """
        Fixed version with bounded cache using LRU-like eviction.
        """
        logger.info(f"fixed_function: storing {n} items with max_size={max_cache_size}")
        for i in range(n):
            key = f"key_{i}"
            self.leaky_cache[key] = [random.random() for _ in range(100)]

            # Evict old entries when cache is too large
            if len(self.leaky_cache) > max_cache_size:
                oldest_key = next(iter(self.leaky_cache))
                del self.leaky_cache[oldest_key]
                logger.debug("Cache eviction performed")


# =============================================================================
# SECTION 4: MEMORY PROFILED FUNCTIONS
# =============================================================================

@memory_profile
def memory_intensive_operation():
    """
    This function is decorated with @memory_profile.
    Running it will show memory usage line by line.
    """
    logger.info("Starting memory intensive operation...")

    # Allocate a large list
    big_list = [i for i in range(1_000_000)]              # ~8 MB
    logger.debug(f"Created big_list with {len(big_list)} elements")

    # Allocate another large structure
    big_dict = {str(i): i * 2 for i in range(500_000)}   # ~50 MB
    logger.debug(f"Created big_dict with {len(big_dict)} elements")

    # Do some computation
    total = sum(big_list)
    logger.debug(f"Sum of big_list: {total}")

    # Delete the list (memory should drop)
    del big_list
    logger.debug("Deleted big_list")

    # Create another structure
    nested = [[j for j in range(100)] for _ in range(1000)]  # ~800 KB
    logger.debug("Created nested list")

    result = sum(sum(row) for row in nested)
    logger.debug(f"Nested sum: {result}")

    del big_dict
    del nested
    logger.debug("Cleaned up all allocations")

    return result


# =============================================================================
# SECTION 5: TRACEMALLOC - SNAPSHOT MEMORY ANALYSIS
# =============================================================================

def run_tracemalloc_demo():
    """
    Uses tracemalloc to find where memory is being allocated.
    Shows top memory allocation sites in the code.
    """
    print("\n" + "="*70)
    print("TRACEMALLOC MEMORY ANALYSIS")
    print("="*70)

    tracemalloc.start()

    # Code that allocates memory
    data = []
    for _ in range(10000):
        data.append({
            'values': [random.random() for _ in range(50)],
            'name': f'item_{random.randint(0, 1000)}',
            'score': random.uniform(0, 100)
        })

    # Compute some stats
    scores = [d['score'] for d in data]
    mean_score = statistics.mean(scores)
    logger.info(f"Mean score: {mean_score:.2f}")

    # Take snapshot
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')

    print("\nTop 10 memory allocation sites:")
    print("-" * 60)
    for i, stat in enumerate(top_stats[:10], 1):
        print(f"{i:2}. {stat}")

    tracemalloc.stop()
    del data


# =============================================================================
# SECTION 6: CPU PROFILING WITH cProfile
# =============================================================================

def run_cpu_profile_demo():
    """
    Profiles a set of functions using cProfile.
    Shows which functions take the most CPU time.
    """
    print("\n" + "="*70)
    print("CPU PROFILING WITH cProfile")
    print("="*70)

    slow = SlowAlgorithms()
    fast = FastAlgorithms()

    # Generate test data
    test_numbers = [random.randint(1, 1000) for _ in range(3000)]
    test_words   = [f"word{i}" for i in range(10000)]
    test_targets = random.sample(test_numbers, 50)

    def workload_slow():
        slow.slow_find_duplicates(test_numbers)
        slow.slow_string_concat(test_words)
        slow.slow_sort_search(test_numbers, test_targets)

    def workload_fast():
        fast.fast_find_duplicates(test_numbers)
        fast.fast_string_concat(test_words)
        fast.fast_sort_search(test_numbers, test_targets)

    # --- Profile SLOW workload ---
    print("\n[ Profiling SLOW workload ]")
    profiler = cProfile.Profile()
    profiler.enable()
    workload_slow()
    profiler.disable()

    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats('cumulative')
    stats.print_stats(15)
    print(stream.getvalue())

    # --- Profile FAST workload ---
    print("\n[ Profiling FAST workload ]")
    profiler2 = cProfile.Profile()
    profiler2.enable()
    workload_fast()
    profiler2.disable()

    stream2 = io.StringIO()
    stats2 = pstats.Stats(profiler2, stream=stream2)
    stats2.sort_stats('cumulative')
    stats2.print_stats(15)
    print(stream2.getvalue())

    # Save profiles to files for external analysis
    profiler.dump_stats("slow_profile.prof")
    profiler2.dump_stats("fast_profile.prof")
    logger.info("Profiles saved to slow_profile.prof and fast_profile.prof")


# =============================================================================
# SECTION 7: FIBONACCI COMPARISON (Profiling Recursive vs Iterative)
# =============================================================================

def run_fibonacci_comparison():
    """
    Directly compares slow (recursive) vs fast (iterative) Fibonacci.
    """
    print("\n" + "="*70)
    print("FIBONACCI: RECURSIVE vs ITERATIVE COMPARISON")
    print("="*70)

    slow = SlowAlgorithms()
    fast = FastAlgorithms()

    fib_input = 30  # Recursive gets very slow above ~35

    print(f"\nCalculating Fibonacci({fib_input}):")

    # Profile recursive
    pr1 = cProfile.Profile()
    pr1.enable()
    result_slow = slow.slow_fibonacci(fib_input)
    pr1.disable()

    # Profile iterative
    pr2 = cProfile.Profile()
    pr2.enable()
    result_fast = fast.fast_fibonacci(fib_input)
    pr2.disable()

    assert result_slow == result_fast, "Results should match!"
    print(f"\nBoth return: {result_slow}")

    print("\n--- SLOW (Recursive) Profile ---")
    s1 = io.StringIO()
    ps1 = pstats.Stats(pr1, stream=s1)
    ps1.sort_stats('calls')
    ps1.print_stats(10)
    print(s1.getvalue())

    print("\n--- FAST (Iterative) Profile ---")
    s2 = io.StringIO()
    ps2 = pstats.Stats(pr2, stream=s2)
    ps2.sort_stats('calls')
    ps2.print_stats(10)
    print(s2.getvalue())


# =============================================================================
# SECTION 8: BUG DEMONSTRATION AND FIX COMPARISON
# =============================================================================

def run_bug_demonstrations():
    """
    Runs each buggy function alongside its fixed version.
    Shows the difference in output and catches errors.
    """
    print("\n" + "="*70)
    print("BUG DEMONSTRATIONS")
    print("="*70)

    calc = BuggyCalculator()
    test_data = [10, 20, 30, 40, 50]

    # --- Bug 1: Off-by-one in average ---
    print("\n[BUG 1] Off-by-one error in average calculation")
    print(f"  Input data: {test_data}")
    print(f"  Expected average: {sum(test_data) / len(test_data)}")
    buggy_result = calc.buggy_average(test_data)
    fixed_result = calc.fixed_average(test_data)
    print(f"  Buggy result:  {buggy_result}  <-- WRONG (skipped first element)")
    print(f"  Fixed result:  {fixed_result}  <-- CORRECT")

    # --- Bug 2: Wrong comparison in find_max ---
    print("\n[BUG 2] Wrong comparison operator in find_max")
    print(f"  Input data: {test_data}")
    print(f"  Expected max: {max(test_data)}")
    buggy_max = calc.buggy_find_max(test_data)
    fixed_max = calc.fixed_find_max(test_data)
    print(f"  Buggy result:  {buggy_max}  <-- WRONG (returns min instead!)")
    print(f"  Fixed result:  {fixed_max}  <-- CORRECT")

    # --- Bug 3: Division by zero ---
    print("\n[BUG 3] Division by zero")
    print("  Attempting 10 / 0:")
    try:
        result = calc.buggy_divide(10, 0)
        print(f"  Buggy result: {result}")
    except ZeroDivisionError as e:
        print(f"  Buggy version CRASHED: ZeroDivisionError: {e}")
        logger.error(f"Caught expected crash: {e}")
        logger.debug(traceback.format_exc())
    fixed_result = calc.fixed_divide(10, 0)
    print(f"  Fixed result:  {fixed_result}  <-- Returns None safely")

    # --- Bug 4: Binary search ---
    print("\n[BUG 4] Wrong binary search mid calculation")
    sorted_arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    target = 7
    print(f"  Searching for {target} in {sorted_arr}")
    buggy_idx = calc.buggy_binary_search(sorted_arr, target)
    fixed_idx = calc.fixed_binary_search(sorted_arr, target)
    print(f"  Buggy result:  index={buggy_idx}  <-- Incorrect/broken")
    print(f"  Fixed result:  index={fixed_idx}  "
          f"<-- CORRECT (value={sorted_arr[fixed_idx] if fixed_idx != -1 else 'N/A'})")


# =============================================================================
# SECTION 9: INTERACTIVE PDB DEBUGGING DEMO
# =============================================================================

def run_pdb_demo():
    """
    Demonstrates using pdb for interactive debugging.
    When pdb starts, use these commands:
        n   - next line (step over)
        s   - step into function
        c   - continue to next breakpoint
        p variable_name  - print a variable
        pp variable_name - pretty print a variable
        l   - list source code
        w   - show call stack (where)
        q   - quit debugger
        b 10 - set breakpoint at line 10
        h   - help
    """
    print("\n" + "="*70)
    print("INTERACTIVE PDB DEBUGGING DEMO")
    print("(Type 'c' and press Enter to continue past each breakpoint)")
    print("="*70)

    data = [5, 3, 8, 1, 9, 2, 7, 4, 6]
    target = 7

    print(f"\nWe are going to sort {data} and search for {target}")
    print("PDB breakpoint set - you can inspect variables now!\n")

    # ---- PDB BREAKPOINT ----
    pdb.set_trace()
    # At the pdb prompt, try these:
    # p data
    # p target
    # p len(data)
    # n (to step to next line)
    # c (to continue)
    # ---- END BREAKPOINT ----

    sorted_data = sorted(data)
    logger.debug(f"Sorted data: {sorted_data}")

    # Another breakpoint after sorting
    pdb.set_trace()
    # At the pdb prompt, try:
    # p sorted_data
    # p sorted_data[0], sorted_data[-1]
    # n
    # c

    # Binary search
    left, right = 0, len(sorted_data) - 1
    found_index = -1

    while left <= right:
        mid = (left + right) // 2
        if sorted_data[mid] == target:
            found_index = mid
            break
        elif sorted_data[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    print(f"\nSearch complete: {target} found at index {found_index} "
          f"in sorted array {sorted_data}")


# =============================================================================
# SECTION 10: ASSERTION-BASED DEBUGGING
# =============================================================================

def run_assertion_demo():
    """
    Shows how assertions can catch bugs at runtime.
    """
    print("\n" + "="*70)
    print("ASSERTION-BASED DEBUGGING")
    print("="*70)

    def process_age(age):
        # Guard against invalid input
        assert isinstance(age, int), f"Age must be int, got {type(age)}"
        assert 0 <= age <= 150, f"Age {age} is not a valid human age"
        logger.debug(f"Processing valid age: {age}")
        return f"Age category: {'minor' if age < 18 else 'adult'}"

    def safe_sqrt(n):
        assert n >= 0, f"Cannot take sqrt of negative number: {n}"
        return n ** 0.5

    # Valid cases
    print("\nValid assertions (should pass):")
    print(f"  {process_age(25)}")
    print(f"  {process_age(17)}")
    print(f"  sqrt(16) = {safe_sqrt(16)}")

    # Invalid cases that trigger assertions
    print("\nInvalid cases (assertions will catch bugs):")

    # Wrong type
    try:
        process_age("twenty-five")
    except AssertionError as e:
        print(f"  AssertionError caught: {e}")

    # Out of range
    try:
        process_age(200)
    except AssertionError as e:
        print(f"  AssertionError caught: {e}")

    # Negative sqrt
    try:
        safe_sqrt(-4)
    except AssertionError as e:
        print(f"  AssertionError caught: {e}")

    print("\nAssertions are a powerful first line of defense!")


# =============================================================================
# SECTION 11: MEMORY LEAK DEMO WITH TRACEMALLOC
# =============================================================================

def run_memory_leak_demo():
    """
    Demonstrates detecting a memory leak using tracemalloc.
    Compares leaky vs fixed implementations.
    """
    print("\n" + "="*70)
    print("MEMORY LEAK DETECTION DEMO")
    print("="*70)

    demo = MemoryLeakDemo()

    # --- Leaky version ---
    print("\n[LEAKY] Running leaky function 5 times...")
    tracemalloc.start()
    snapshot_before = tracemalloc.take_snapshot()

    for i in range(5):
        demo.leaky_function(200)
        current, peak = tracemalloc.get_traced_memory()
        print(f"  Iteration {i+1}: current={current/1024:.1f} KB, "
              f"peak={peak/1024:.1f} KB, "
              f"cache_size={len(demo.leaky_cache)}")

    snapshot_after = tracemalloc.take_snapshot()
    top_stats = snapshot_after.compare_to(snapshot_before, 'lineno')

    print("\nTop memory growth sites (leaky):")
    for stat in top_stats[:5]:
        print(f"  {stat}")

    tracemalloc.stop()

    # --- Fixed version ---
    demo2 = MemoryLeakDemo()
    print("\n[FIXED] Running fixed function 5 times (max cache=500)...")
    tracemalloc.start()
    snapshot_before2 = tracemalloc.take_snapshot()

    for i in range(5):
        demo2.fixed_function(200, max_cache_size=500)
        current, peak = tracemalloc.get_traced_memory()
        print(f"  Iteration {i+1}: current={current/1024:.1f} KB, "
              f"peak={peak/1024:.1f} KB, "
              f"cache_size={len(demo2.leaky_cache)}")

    snapshot_after2 = tracemalloc.take_snapshot()
    top_stats2 = snapshot_after2.compare_to(snapshot_before2, 'lineno')

    print("\nTop memory growth sites (fixed):")
    for stat in top_stats2[:5]:
        print(f"  {stat}")

    tracemalloc.stop()


# =============================================================================
# SECTION 12: PRIME NUMBER PROFILING
# =============================================================================

def run_prime_comparison():
    """
    Profiles slow O(n) vs fast O(√n) prime checker.
    """
    print("\n" + "="*70)
    print("PRIME CHECKER: O(n) vs O(√n) COMPARISON")
    print("="*70)

    slow = SlowAlgorithms()
    fast = FastAlgorithms()

    test_primes = [9999991, 999983, 104729]

    print("\nChecking prime status of large numbers:")
    for num in test_primes:
        print(f"\n  Number: {num}")

        # Time slow version
        t0 = time.perf_counter()
        result_slow = slow.slow_is_prime(num)
        t1 = time.perf_counter()

        # Time fast version
        t2 = time.perf_counter()
        result_fast = fast.fast_is_prime(num)
        t3 = time.perf_counter()

        slow_ms = (t1 - t0) * 1000
        fast_ms = (t3 - t2) * 1000
        speedup = slow_ms / fast_ms if fast_ms > 0 else float('inf')

        assert result_slow == result_fast, "Results don't match!"

        print(f"    Slow: {slow_ms:.2f} ms | Fast: {fast_ms:.4f} ms | "
              f"Speedup: {speedup:.1f}x | Is prime: {result_fast}")


# =============================================================================
# MAIN MENU
# =============================================================================

def print_separator():
    print("\n" + "="*70 + "\n")


def main():
    print("="*70)
    print("  DEBUGGING AND PROFILING DEMONSTRATION PROGRAM")
    print("="*70)
    print("""
Choose a demo to run:

  1  - Bug Demonstrations (off-by-one, wrong operator, div/zero, bad search)
  2  - Assertion-Based Debugging
  3  - CPU Profiling (slow vs fast algorithms with cProfile)
  4  - Fibonacci Profiling (recursive O(2^n) vs iterative O(n))
  5  - Prime Number Profiling (O(n) vs O(√n))
  6  - Memory Profiling (line-by-line with @memory_profile)
  7  - Memory Leak Detection (tracemalloc)
  8  - Tracemalloc Allocation Analysis
  9  - Interactive PDB Debugger (you type commands!)
  10 - Run ALL demos (except PDB)
  q  - Quit
    """)

    while True:
        choice = input("Enter choice: ").strip().lower()

        if choice == '1':
            run_bug_demonstrations()

        elif choice == '2':
            run_assertion_demo()

        elif choice == '3':
            run_cpu_profile_demo()

        elif choice == '4':
            run_fibonacci_comparison()

        elif choice == '5':
            run_prime_comparison()

        elif choice == '6':
            print("\n" + "="*70)
            print("MEMORY PROFILE (line-by-line)")
            print("="*70)
            memory_intensive_operation()

        elif choice == '7':
            run_memory_leak_demo()

        elif choice == '8':
            run_tracemalloc_demo()

        elif choice == '9':
            run_pdb_demo()

        elif choice == '10':
            run_bug_demonstrations()
            print_separator()
            run_assertion_demo()
            print_separator()
            run_cpu_profile_demo()
            print_separator()
            run_fibonacci_comparison()
            print_separator()
            run_prime_comparison()
            print_separator()
            run_memory_leak_demo()
            print_separator()
            run_tracemalloc_demo()
            print_separator()
            memory_intensive_operation()
            print("\nAll demos complete! Check debug_log.txt for full logs.")

        elif choice == 'q':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Enter 1-10 or q.")

        print_separator()


if __name__ == "__main__":
    main()