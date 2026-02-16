"""
Sliding Window Algorithms for Stream Processing
===============================================

Implementations of algorithms for maintaining statistics and solving
problems over sliding windows in data streams.

Includes:
- Sliding Window Maximum/Minimum
- Sliding Window Average/Sum
- Sliding Window Unique Elements
- Sliding Window Frequency
- SWAG (Sliding Window Aggregation)
- Exponential Histograms
- Time-based Windows

Author: Claude
Date: January 2026
"""

import heapq
from collections import deque, defaultdict, Counter
from typing import Any, List, Optional, Tuple, Callable, Generic, TypeVar
import time
import bisect
import math


T = TypeVar('T')


class SlidingWindowMaximum:
    """
    Sliding Window Maximum using Monotonic Deque.

    Maintains the maximum element in a sliding window of size k.
    Time complexity: O(1) amortized per operation
    Space complexity: O(k)
    """

    def __init__(self, k: int):
        """
        Initialize sliding window maximum.

        Args:
            k: Window size
        """
        self.k = k
        self.window = deque()  # Stores (value, index) pairs
        self.current_index = 0

    def add(self, value: float) -> Optional[float]:
        """
        Add value and return maximum in current window.

        Args:
            value: Value to add

        Returns:
            Maximum in current window
        """
        # Remove elements outside window
        while self.window and self.window[0][1] <= self.current_index - self.k:
            self.window.popleft()

        # Remove elements smaller than current (they can't be maximum)
        while self.window and self.window[-1][0] <= value:
            self.window.pop()

        # Add current element
        self.window.append((value, self.current_index))
        self.current_index += 1

        # Return maximum (front of deque)
        return self.window[0][0] if self.window else None

    def get_max(self) -> Optional[float]:
        """Get current window maximum."""
        # Clean expired elements
        while self.window and self.window[0][1] <= self.current_index - self.k - 1:
            self.window.popleft()

        return self.window[0][0] if self.window else None


class SlidingWindowMinimum:
    """
    Sliding Window Minimum using Monotonic Deque.

    Similar to maximum but maintains minimum element.
    """

    def __init__(self, k: int):
        """Initialize sliding window minimum."""
        self.k = k
        self.window = deque()  # Stores (value, index) pairs
        self.current_index = 0

    def add(self, value: float) -> Optional[float]:
        """Add value and return minimum in current window."""
        # Remove elements outside window
        while self.window and self.window[0][1] <= self.current_index - self.k:
            self.window.popleft()

        # Remove elements larger than current
        while self.window and self.window[-1][0] >= value:
            self.window.pop()

        # Add current element
        self.window.append((value, self.current_index))
        self.current_index += 1

        return self.window[0][0] if self.window else None


class SlidingWindowAverage:
    """
    Sliding Window Average with O(1) updates.

    Maintains sum and count for efficient average calculation.
    """

    def __init__(self, k: int):
        """
        Initialize sliding window average.

        Args:
            k: Window size
        """
        self.k = k
        self.window = deque(maxlen=k)
        self.sum = 0.0
        self.count = 0

    def add(self, value: float) -> float:
        """
        Add value and return average of current window.

        Args:
            value: Value to add

        Returns:
            Average of current window
        """
        if len(self.window) == self.k:
            # Remove oldest value
            old_value = self.window[0]
            self.sum -= old_value
            self.count -= 1

        # Add new value
        self.window.append(value)
        self.sum += value
        self.count += 1

        return self.sum / self.count if self.count > 0 else 0.0

    def get_average(self) -> float:
        """Get current window average."""
        return self.sum / self.count if self.count > 0 else 0.0

    def get_sum(self) -> float:
        """Get current window sum."""
        return self.sum


class SlidingWindowUnique:
    """
    Sliding Window Unique Elements Counter.

    Tracks number of unique elements in sliding window.
    """

    def __init__(self, k: int):
        """
        Initialize unique counter.

        Args:
            k: Window size
        """
        self.k = k
        self.window = deque(maxlen=k)
        self.counts = defaultdict(int)
        self.unique_count = 0

    def add(self, item: Any) -> int:
        """
        Add item and return unique count.

        Args:
            item: Item to add

        Returns:
            Number of unique elements in window
        """
        # Add new item
        self.counts[item] += 1
        if self.counts[item] == 1:
            self.unique_count += 1

        # Remove old item if window is full
        if len(self.window) == self.k:
            old_item = self.window[0]
            self.counts[old_item] -= 1
            if self.counts[old_item] == 0:
                self.unique_count -= 1
                del self.counts[old_item]

        self.window.append(item)
        return self.unique_count

    def get_unique_count(self) -> int:
        """Get current unique count."""
        return self.unique_count

    def get_unique_elements(self) -> set:
        """Get set of unique elements."""
        return set(self.counts.keys())


class SlidingWindowFrequency:
    """
    Sliding Window Frequency Counter.

    Maintains frequency of each element in sliding window.
    Supports queries for most/least frequent elements.
    """

    def __init__(self, k: int):
        """
        Initialize frequency counter.

        Args:
            k: Window size
        """
        self.k = k
        self.window = deque(maxlen=k)
        self.freq = Counter()
        self.freq_to_items = defaultdict(set)

    def add(self, item: Any):
        """Add item to window."""
        # Remove old item if window is full
        if len(self.window) == self.k:
            old_item = self.window[0]
            old_freq = self.freq[old_item]

            # Update frequency mappings
            self.freq_to_items[old_freq].discard(old_item)
            if not self.freq_to_items[old_freq]:
                del self.freq_to_items[old_freq]

            self.freq[old_item] -= 1
            if self.freq[old_item] == 0:
                del self.freq[old_item]
            else:
                self.freq_to_items[self.freq[old_item]].add(old_item)

        # Add new item
        old_freq = self.freq.get(item, 0)
        if old_freq > 0:
            self.freq_to_items[old_freq].discard(item)
            if not self.freq_to_items[old_freq]:
                del self.freq_to_items[old_freq]

        self.freq[item] += 1
        self.freq_to_items[self.freq[item]].add(item)
        self.window.append(item)

    def get_frequency(self, item: Any) -> int:
        """Get frequency of specific item."""
        return self.freq.get(item, 0)

    def get_most_frequent(self, n: int = 1) -> List[Tuple[Any, int]]:
        """Get n most frequent items."""
        return self.freq.most_common(n)

    def get_max_frequency(self) -> int:
        """Get maximum frequency."""
        if not self.freq_to_items:
            return 0
        return max(self.freq_to_items.keys())


class SWAG(Generic[T]):
    """
    Sliding Window Aggregation (SWAG).

    General framework for sliding window aggregation with any associative operation.
    Uses two stacks to achieve amortized O(1) operations.
    """

    def __init__(self, k: int, identity: T, combine: Callable[[T, T], T]):
        """
        Initialize SWAG.

        Args:
            k: Window size
            identity: Identity element for the operation
            combine: Associative binary operation
        """
        self.k = k
        self.identity = identity
        self.combine = combine

        # Two stacks with aggregated values
        self.front_stack = []  # (value, aggregated)
        self.back_stack = []   # (value, aggregated)
        self.window_size = 0

    def add(self, value: T):
        """Add value to window."""
        # Add to back stack
        if self.back_stack:
            aggregated = self.combine(self.back_stack[-1][1], value)
        else:
            aggregated = value

        self.back_stack.append((value, aggregated))
        self.window_size += 1

        # Remove oldest if window is full
        if self.window_size > self.k:
            self._remove_oldest()

    def _remove_oldest(self):
        """Remove oldest element from window."""
        if not self.front_stack:
            # Move all from back to front
            self._rebalance()

        if self.front_stack:
            self.front_stack.pop()
            self.window_size -= 1

    def _rebalance(self):
        """Move elements from back stack to front stack."""
        if not self.back_stack:
            return

        # Rebuild front stack
        values = []
        while self.back_stack:
            val, _ = self.back_stack.pop()
            values.append(val)

        # Build front stack with reverse aggregation
        for val in reversed(values):
            if self.front_stack:
                aggregated = self.combine(val, self.front_stack[-1][1])
            else:
                aggregated = val
            self.front_stack.append((val, aggregated))

    def query(self) -> T:
        """Get aggregated value of current window."""
        front_agg = self.front_stack[-1][1] if self.front_stack else self.identity
        back_agg = self.back_stack[-1][1] if self.back_stack else self.identity

        if self.front_stack and self.back_stack:
            return self.combine(front_agg, back_agg)
        elif self.front_stack:
            return front_agg
        elif self.back_stack:
            return back_agg
        else:
            return self.identity


class ExponentialHistogram:
    """
    Exponential Histogram for counting 1s in sliding window.

    Space-efficient algorithm for counting bits in a sliding window.
    Provides (1 + epsilon)-approximation using O(log W / epsilon) space.
    """

    def __init__(self, window_size: int, epsilon: float = 0.5):
        """
        Initialize exponential histogram.

        Args:
            window_size: Size of sliding window
            epsilon: Error bound (0 < epsilon < 1)
        """
        self.window_size = window_size
        self.epsilon = epsilon
        self.k = int(1.0 / epsilon) + 1  # Max buckets per size

        # Buckets: list of (size, timestamp) pairs
        self.buckets = []
        self.current_time = 0
        self.last_bucket_time = 0

    def add(self, bit: int):
        """
        Add bit to stream.

        Args:
            bit: 0 or 1
        """
        self.current_time += 1

        # Remove expired buckets
        while self.buckets and self.buckets[0][1] <= self.current_time - self.window_size:
            self.buckets.pop(0)

        if bit == 1:
            # Add new bucket of size 1
            self.buckets.append((1, self.current_time))
            self._merge_buckets()

    def _merge_buckets(self):
        """Merge buckets to maintain invariant."""
        # Count buckets of each size
        size_counts = defaultdict(list)
        for i, (size, timestamp) in enumerate(self.buckets):
            size_counts[size].append(i)

        # Merge if too many buckets of same size
        merged = False
        for size in sorted(size_counts.keys()):
            indices = size_counts[size]
            if len(indices) > self.k:
                # Merge two oldest buckets of this size
                i, j = indices[0], indices[1]
                if j < len(self.buckets):
                    # Create new bucket of double size
                    new_bucket = (size * 2, self.buckets[j][1])

                    # Remove old buckets and add new one
                    self.buckets = (self.buckets[:i] +
                                  self.buckets[i+1:j] +
                                  [new_bucket] +
                                  self.buckets[j+1:])
                    merged = True
                    break

        # Recursively merge if needed
        if merged:
            self._merge_buckets()

    def count(self) -> int:
        """
        Estimate count of 1s in current window.

        Returns:
            Approximate count
        """
        if not self.buckets:
            return 0

        # Sum all buckets except last (which might be partially outside window)
        total = sum(size for size, _ in self.buckets[:-1])

        # Add half of last bucket
        if self.buckets:
            total += self.buckets[-1][0] // 2

        return total


class TimeBasedSlidingWindow:
    """
    Time-based Sliding Window.

    Maintains window based on time duration rather than count.
    """

    def __init__(self, duration_seconds: float):
        """
        Initialize time-based window.

        Args:
            duration_seconds: Window duration in seconds
        """
        self.duration = duration_seconds
        self.window = deque()  # (timestamp, value) pairs

    def add(self, value: Any, timestamp: Optional[float] = None):
        """
        Add value with timestamp.

        Args:
            value: Value to add
            timestamp: Unix timestamp (uses current time if None)
        """
        if timestamp is None:
            timestamp = time.time()

        # Remove expired elements
        cutoff = timestamp - self.duration
        while self.window and self.window[0][0] < cutoff:
            self.window.popleft()

        # Add new element
        self.window.append((timestamp, value))

    def get_window(self, current_time: Optional[float] = None) -> List[Any]:
        """
        Get current window values.

        Args:
            current_time: Current time (uses system time if None)

        Returns:
            List of values in window
        """
        if current_time is None:
            current_time = time.time()

        cutoff = current_time - self.duration
        self._clean_expired(cutoff)

        return [value for _, value in self.window]

    def _clean_expired(self, cutoff: float):
        """Remove expired elements."""
        while self.window and self.window[0][0] < cutoff:
            self.window.popleft()

    def count(self) -> int:
        """Count elements in current window."""
        self._clean_expired(time.time() - self.duration)
        return len(self.window)

    def aggregate(self, func: Callable, current_time: Optional[float] = None):
        """
        Apply aggregation function to window.

        Args:
            func: Aggregation function
            current_time: Current time

        Returns:
            Aggregated result
        """
        values = self.get_window(current_time)
        return func(values) if values else None


class TumblingWindow:
    """
    Tumbling (Fixed) Window.

    Non-overlapping windows of fixed size.
    """

    def __init__(self, window_size: int):
        """
        Initialize tumbling window.

        Args:
            window_size: Size of each window
        """
        self.window_size = window_size
        self.current_window = []
        self.completed_windows = []

    def add(self, value: Any) -> Optional[List[Any]]:
        """
        Add value to window.

        Returns:
            Completed window if one is ready, None otherwise
        """
        self.current_window.append(value)

        if len(self.current_window) == self.window_size:
            completed = self.current_window
            self.current_window = []
            self.completed_windows.append(completed)
            return completed

        return None

    def get_current_window(self) -> List[Any]:
        """Get current incomplete window."""
        return self.current_window.copy()


class SessionWindow:
    """
    Session Window.

    Dynamic windows based on gaps in activity.
    """

    def __init__(self, gap_threshold: float):
        """
        Initialize session window.

        Args:
            gap_threshold: Maximum gap between events in same session
        """
        self.gap_threshold = gap_threshold
        self.sessions = []
        self.current_session = []
        self.last_timestamp = None

    def add(self, value: Any, timestamp: float) -> Optional[List[Any]]:
        """
        Add event to session.

        Args:
            value: Event value
            timestamp: Event timestamp

        Returns:
            Completed session if gap detected, None otherwise
        """
        if self.last_timestamp is not None:
            gap = timestamp - self.last_timestamp
            if gap > self.gap_threshold:
                # End current session
                completed = self.current_session
                self.sessions.append(completed)
                self.current_session = [value]
                self.last_timestamp = timestamp
                return completed

        self.current_session.append(value)
        self.last_timestamp = timestamp
        return None

    def close_session(self) -> Optional[List[Any]]:
        """Force close current session."""
        if self.current_session:
            completed = self.current_session
            self.sessions.append(completed)
            self.current_session = []
            self.last_timestamp = None
            return completed
        return None


def example_usage():
    """Demonstrate sliding window algorithms."""
    print("=" * 60)
    print("SLIDING WINDOW ALGORITHMS")
    print("=" * 60)

    # Example 1: Sliding Window Maximum
    print("\n1. Sliding Window Maximum:")
    print("-" * 40)

    data = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    sw_max = SlidingWindowMaximum(k)

    print(f"Data: {data}")
    print(f"Window size: {k}")
    print("Window maximums:")

    for i, val in enumerate(data):
        max_val = sw_max.add(val)
        if i >= k - 1:
            window = data[max(0, i-k+1):i+1]
            print(f"  Window {window}: max = {max_val}")

    # Example 2: Sliding Window Average
    print("\n2. Sliding Window Average:")
    print("-" * 40)

    sw_avg = SlidingWindowAverage(k=5)
    stream = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    print(f"Stream: {stream}")
    print("Moving average (window=5):")

    for i, val in enumerate(stream):
        avg = sw_avg.add(val)
        print(f"  After {val}: average = {avg:.2f}")

    # Example 3: Sliding Window Unique Elements
    print("\n3. Sliding Window Unique Elements:")
    print("-" * 40)

    items = ['a', 'b', 'c', 'a', 'b', 'd', 'c', 'a']
    sw_unique = SlidingWindowUnique(k=4)

    print(f"Stream: {items}")
    print(f"Window size: 4")

    for i, item in enumerate(items):
        unique_count = sw_unique.add(item)
        if i >= 3:
            window = items[i-3:i+1]
            unique = sw_unique.get_unique_elements()
            print(f"  Window {window}: {unique_count} unique elements {unique}")

    # Example 4: Sliding Window Frequency
    print("\n4. Sliding Window Frequency:")
    print("-" * 40)

    sw_freq = SlidingWindowFrequency(k=5)
    stream = ['a', 'b', 'a', 'c', 'a', 'b', 'd', 'a']

    print(f"Stream: {stream}")
    for item in stream:
        sw_freq.add(item)

    print(f"Final window: {stream[-5:]}")
    print(f"Most frequent: {sw_freq.get_most_frequent(3)}")
    print(f"Frequency of 'a': {sw_freq.get_frequency('a')}")
    print(f"Max frequency: {sw_freq.get_max_frequency()}")

    # Example 5: SWAG (Sliding Window Aggregation)
    print("\n5. SWAG - General Sliding Window Aggregation:")
    print("-" * 40)

    # Example: sliding window sum
    swag_sum = SWAG(k=3, identity=0, combine=lambda a, b: a + b)

    # Example: sliding window max
    swag_max = SWAG(k=3, identity=float('-inf'), combine=max)

    data = [1, 3, 2, 5, 4, 2]
    print(f"Data: {data}")
    print(f"Window size: 3")

    print("\nSliding window sum:")
    for val in data:
        swag_sum.add(val)
        if swag_sum.window_size >= 3:
            print(f"  Window sum: {swag_sum.query()}")

    print("\nSliding window max:")
    for val in data:
        swag_max.add(val)
        if swag_max.window_size >= 3:
            print(f"  Window max: {swag_max.query()}")

    # Example 6: Exponential Histogram
    print("\n6. Exponential Histogram (Bit Counting):")
    print("-" * 40)

    exp_hist = ExponentialHistogram(window_size=10, epsilon=0.25)
    bit_stream = [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1]

    print(f"Bit stream: {bit_stream}")
    print(f"Window size: 10, Epsilon: 0.25")

    for i, bit in enumerate(bit_stream):
        exp_hist.add(bit)
        if i >= 9:
            window = bit_stream[i-9:i+1]
            actual = sum(window)
            estimate = exp_hist.count()
            print(f"  Window {i-9}-{i}: Actual={actual}, Estimate={estimate}")

    # Example 7: Time-based Window
    print("\n7. Time-based Sliding Window:")
    print("-" * 40)

    time_window = TimeBasedSlidingWindow(duration_seconds=2.0)

    # Simulate events with timestamps
    events = [
        (0.0, "event1"),
        (0.5, "event2"),
        (1.0, "event3"),
        (1.5, "event4"),
        (2.0, "event5"),
        (2.5, "event6"),
        (3.0, "event7")
    ]

    print("Events with timestamps:")
    for timestamp, event in events:
        time_window.add(event, timestamp)
        window = time_window.get_window(timestamp)
        print(f"  t={timestamp}: Window = {window}")

    # Example 8: Tumbling Window
    print("\n8. Tumbling Window:")
    print("-" * 40)

    tumbling = TumblingWindow(window_size=4)
    stream = list(range(1, 11))

    print(f"Stream: {stream}")
    print(f"Tumbling window size: 4")

    for val in stream:
        completed = tumbling.add(val)
        if completed:
            print(f"  Completed window: {completed}, Sum = {sum(completed)}")

    if tumbling.get_current_window():
        print(f"  Incomplete window: {tumbling.get_current_window()}")

    # Example 9: Session Window
    print("\n9. Session Window:")
    print("-" * 40)

    session_window = SessionWindow(gap_threshold=2.0)

    # Events with varying gaps
    events = [
        (0.0, "click1"),
        (0.5, "click2"),
        (1.0, "click3"),
        (4.0, "click4"),  # Gap > 2.0, new session
        (4.2, "click5"),
        (4.5, "click6"),
        (8.0, "click7")   # Gap > 2.0, new session
    ]

    print(f"Session gap threshold: 2.0 seconds")
    print("Events:")

    for timestamp, event in events:
        session = session_window.add(event, timestamp)
        if session:
            print(f"  Session ended: {session}")

    # Close final session
    final_session = session_window.close_session()
    if final_session:
        print(f"  Final session: {final_session}")

    # Performance comparison
    print("\n10. Performance Comparison:")
    print("-" * 40)

    import time as time_module

    test_size = 100000
    window_size = 100
    test_data = list(range(test_size))

    algorithms = [
        ("Sliding Max", SlidingWindowMaximum(window_size)),
        ("Sliding Avg", SlidingWindowAverage(window_size)),
        ("Sliding Unique", SlidingWindowUnique(window_size))
    ]

    print(f"Stream size: {test_size:,}")
    print(f"Window size: {window_size}")

    for name, algo in algorithms:
        start = time_module.time()

        for val in test_data:
            algo.add(val)

        elapsed = time_module.time() - start
        print(f"  {name:15s}: {elapsed*1000:.2f} ms")

    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("- Monotonic deque for O(1) min/max queries")
    print("- SWAG generalizes to any associative operation")
    print("- Exponential histograms for space-efficient counting")
    print("- Time-based windows for temporal data")
    print("- Session windows for activity-based segmentation")
    print("=" * 60)


if __name__ == "__main__":
    example_usage()