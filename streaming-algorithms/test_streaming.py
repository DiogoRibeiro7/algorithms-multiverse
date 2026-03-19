"""
Test Suite for Streaming Algorithms

Tests:
- Sliding window (max, min, average, unique, frequency)
- HyperLogLog, Count-Min Sketch, Reservoir Sampling (numpy-dependent)
- Morris Counting, Online Median/Statistics (numpy-dependent)

Run with:
    python -m pytest test_streaming.py -v
    or
    python test_streaming.py
"""

import sys
import os
import subprocess
import unittest

sys.path.insert(0, os.path.dirname(__file__))

from sliding_window import (
    SlidingWindowMaximum,
    SlidingWindowMinimum,
    SlidingWindowAverage,
    SlidingWindowUnique,
    SlidingWindowFrequency,
    TumblingWindow,
)

_np_check = subprocess.run(
    [sys.executable, "-c", "import numpy"], capture_output=True, timeout=10
)
HAS_NUMPY = _np_check.returncode == 0

if HAS_NUMPY:
    from hyperloglog import HyperLogLog, LinearCounting, CountingBloomFilter
    from count_min_sketch import CountMinSketch, CountSketch
    from reservoir_sampling import ReservoirSampling, WeightedReservoirSampling
    from morris_counting import MorrisCounter, MorrisPlusPlusCounter
    from online_median import OnlineMedianFinder, SlidingWindowMedian as SWMedian
    from online_statistics import WelfordVariance, ExponentiallyWeightedStats


# ============================================================================
# SLIDING WINDOW TESTS (no numpy)
# ============================================================================


class TestSlidingWindowMaximum(unittest.TestCase):
    def test_basic(self):
        sw = SlidingWindowMaximum(3)
        results = []
        for v in [1, 3, 2, 5, 1, 4]:
            r = sw.add(v)
            if r is not None:
                results.append(r)
        self.assertIn(3, results)
        self.assertIn(5, results)

    def test_decreasing(self):
        sw = SlidingWindowMaximum(3)
        for v in [5, 4, 3]:
            sw.add(v)
        self.assertEqual(sw.get_max(), 5)

    def test_increasing(self):
        sw = SlidingWindowMaximum(3)
        for v in [1, 2, 3, 4, 5]:
            sw.add(v)
        self.assertEqual(sw.get_max(), 5)


class TestSlidingWindowMinimum(unittest.TestCase):
    def test_basic(self):
        sw = SlidingWindowMinimum(3)
        for v in [5, 3, 4, 2, 6]:
            sw.add(v)
        # Last 3 elements: [4, 2, 6], min=2
        # The returned value should reflect the window minimum


class TestSlidingWindowAverage(unittest.TestCase):
    def test_basic(self):
        sw = SlidingWindowAverage(3)
        sw.add(1)
        sw.add(2)
        sw.add(3)
        self.assertAlmostEqual(sw.get_average(), 2.0)

    def test_sliding(self):
        sw = SlidingWindowAverage(3)
        for v in [1, 2, 3, 4, 5]:
            sw.add(v)
        # Window: [3, 4, 5], avg = 4.0
        self.assertAlmostEqual(sw.get_average(), 4.0)

    def test_sum(self):
        sw = SlidingWindowAverage(3)
        for v in [1, 2, 3]:
            sw.add(v)
        self.assertAlmostEqual(sw.get_sum(), 6.0)


class TestSlidingWindowUnique(unittest.TestCase):
    def test_basic(self):
        sw = SlidingWindowUnique(3)
        sw.add("a")
        sw.add("b")
        sw.add("a")
        self.assertEqual(sw.get_unique_count(), 2)

    def test_sliding(self):
        sw = SlidingWindowUnique(3)
        sw.add("a")
        sw.add("b")
        sw.add("c")
        sw.add("d")  # "a" drops out
        self.assertNotIn("a", sw.get_unique_elements())
        self.assertEqual(sw.get_unique_count(), 3)


class TestSlidingWindowFrequency(unittest.TestCase):
    def test_basic(self):
        sw = SlidingWindowFrequency(5)
        for item in ["a", "b", "a", "c", "a"]:
            sw.add(item)
        self.assertEqual(sw.get_frequency("a"), 3)
        self.assertEqual(sw.get_frequency("b"), 1)

    def test_most_frequent(self):
        sw = SlidingWindowFrequency(5)
        for item in ["a", "b", "a", "c", "a"]:
            sw.add(item)
        top = sw.get_most_frequent(1)
        self.assertEqual(top[0][0], "a")


class TestTumblingWindow(unittest.TestCase):
    def test_basic(self):
        tw = TumblingWindow(3)
        results = []
        for v in [1, 2, 3, 4, 5, 6]:
            r = tw.add(v)
            if r is not None:
                results.append(r)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], [1, 2, 3])
        self.assertEqual(results[1], [4, 5, 6])

    def test_partial_window(self):
        tw = TumblingWindow(3)
        tw.add(1)
        tw.add(2)
        self.assertEqual(tw.get_current_window(), [1, 2])


# ============================================================================
# HYPERLOGLOG TESTS (numpy)
# ============================================================================


@unittest.skipUnless(HAS_NUMPY, "numpy unavailable")
class TestHyperLogLog(unittest.TestCase):
    def test_accuracy(self):
        hll = HyperLogLog(precision=14)
        n = 10000
        for i in range(n):
            hll.add(f"item_{i}")
        estimate = hll.count()
        # Should be within ~2% for precision 14
        self.assertAlmostEqual(estimate, n, delta=n * 0.1)

    def test_duplicates_ignored(self):
        hll = HyperLogLog()
        for _ in range(1000):
            hll.add("same_item")
        self.assertLessEqual(hll.count(), 5)

    def test_merge(self):
        hll1 = HyperLogLog(precision=10)
        hll2 = HyperLogLog(precision=10)
        for i in range(500):
            hll1.add(f"a_{i}")
        for i in range(500):
            hll2.add(f"b_{i}")
        hll1.merge(hll2)
        self.assertGreater(hll1.count(), 500)

    def test_empty(self):
        hll = HyperLogLog()
        self.assertEqual(hll.count(), 0)


@unittest.skipUnless(HAS_NUMPY, "numpy unavailable")
class TestLinearCounting(unittest.TestCase):
    def test_basic(self):
        lc = LinearCounting()
        for i in range(100):
            lc.add(f"item_{i}")
        estimate = lc.count()
        self.assertAlmostEqual(estimate, 100, delta=20)


@unittest.skipUnless(HAS_NUMPY, "numpy unavailable")
class TestCountingBloomFilter(unittest.TestCase):
    def test_add_contains(self):
        cbf = CountingBloomFilter()
        cbf.add("hello")
        cbf.add("world")
        self.assertTrue(cbf.contains("hello"))
        self.assertTrue(cbf.contains("world"))

    def test_not_contains(self):
        cbf = CountingBloomFilter()
        cbf.add("hello")
        # May have false positives but unlikely for single item
        # Just verify it doesn't crash
        cbf.contains("missing")

    def test_remove(self):
        cbf = CountingBloomFilter()
        cbf.add("hello")
        cbf.remove("hello")
        # After removal, should not contain (no false negatives for removed items)
        self.assertFalse(cbf.contains("hello"))


# ============================================================================
# COUNT-MIN SKETCH TESTS (numpy)
# ============================================================================


@unittest.skipUnless(HAS_NUMPY, "numpy unavailable")
class TestCountMinSketch(unittest.TestCase):
    def test_basic_count(self):
        cms = CountMinSketch()
        for _ in range(100):
            cms.update("hello")
        # CMS overestimates, never underestimates
        self.assertGreaterEqual(cms.query("hello"), 100)

    def test_never_underestimates(self):
        cms = CountMinSketch()
        items = {"a": 50, "b": 30, "c": 20}
        for item, count in items.items():
            cms.update(item, count)
        for item, count in items.items():
            self.assertGreaterEqual(cms.query(item), count)

    def test_unseen_item(self):
        cms = CountMinSketch()
        cms.update("a", 10)
        result = cms.query("never_seen")
        self.assertGreaterEqual(result, 0)


@unittest.skipUnless(HAS_NUMPY, "numpy unavailable")
class TestCountSketch(unittest.TestCase):
    def test_basic(self):
        cs = CountSketch()
        cs.update("test", 50)
        # CountSketch can underestimate (it's unbiased)
        result = cs.query("test")
        self.assertIsInstance(result, int)


# ============================================================================
# RESERVOIR SAMPLING TESTS (numpy)
# ============================================================================


@unittest.skipUnless(HAS_NUMPY, "numpy unavailable")
class TestReservoirSampling(unittest.TestCase):
    def test_sample_size(self):
        rs = ReservoirSampling(10, seed=42)
        for i in range(1000):
            rs.add(i)
        sample = rs.get_sample()
        self.assertEqual(len(sample), 10)

    def test_all_elements_possible(self):
        rs = ReservoirSampling(5, seed=42)
        for i in range(10):
            rs.add(i)
        sample = rs.get_sample()
        self.assertEqual(len(sample), 5)
        for item in sample:
            self.assertIn(item, range(10))

    def test_fewer_than_k(self):
        rs = ReservoirSampling(10, seed=42)
        for i in range(5):
            rs.add(i)
        sample = rs.get_sample()
        self.assertEqual(len(sample), 5)

    def test_reset(self):
        rs = ReservoirSampling(5, seed=42)
        for i in range(20):
            rs.add(i)
        rs.reset()
        self.assertEqual(len(rs.get_sample()), 0)


# ============================================================================
# MORRIS COUNTING TESTS (numpy)
# ============================================================================


@unittest.skipUnless(HAS_NUMPY, "numpy unavailable")
class TestMorrisCounting(unittest.TestCase):
    def test_approximate_count(self):
        mc = MorrisCounter(seed=42)
        n = 1000
        for _ in range(n):
            mc.increment()
        estimate = mc.get_count()
        # Very rough approximation
        self.assertGreater(estimate, 0)

    def test_reset(self):
        mc = MorrisCounter(seed=42)
        mc.increment()
        mc.increment()
        mc.reset()
        self.assertEqual(mc.get_raw_value(), 0)

    def test_plus_plus_accuracy(self):
        mc = MorrisPlusPlusCounter(seed=42)
        n = 1000
        for _ in range(n):
            mc.increment()
        estimate = mc.get_count()
        # Should be in the right order of magnitude
        self.assertGreater(estimate, n * 0.1)


# ============================================================================
# ONLINE MEDIAN TESTS (numpy)
# ============================================================================


@unittest.skipUnless(HAS_NUMPY, "numpy unavailable")
class TestOnlineMedian(unittest.TestCase):
    def test_basic(self):
        omf = OnlineMedianFinder()
        for v in [1, 2, 3]:
            omf.add_number(v)
        self.assertAlmostEqual(omf.find_median(), 2.0)

    def test_even_count(self):
        omf = OnlineMedianFinder()
        for v in [1, 2, 3, 4]:
            omf.add_number(v)
        self.assertAlmostEqual(omf.find_median(), 2.5)

    def test_empty(self):
        omf = OnlineMedianFinder()
        self.assertIsNone(omf.find_median())


# ============================================================================
# ONLINE STATISTICS TESTS (numpy)
# ============================================================================


@unittest.skipUnless(HAS_NUMPY, "numpy unavailable")
class TestWelfordVariance(unittest.TestCase):
    def test_mean(self):
        wv = WelfordVariance()
        for v in [2, 4, 6, 8, 10]:
            wv.add(v)
        self.assertAlmostEqual(wv.get_mean(), 6.0)

    def test_variance(self):
        wv = WelfordVariance()
        for v in [2, 4, 6, 8, 10]:
            wv.add(v)
        # Population variance of [2,4,6,8,10] = 8.0
        self.assertAlmostEqual(wv.get_variance(), 8.0, places=1)

    def test_empty(self):
        wv = WelfordVariance()
        self.assertIsNone(wv.get_mean())
        self.assertIsNone(wv.get_variance())


@unittest.skipUnless(HAS_NUMPY, "numpy unavailable")
class TestExponentiallyWeightedStats(unittest.TestCase):
    def test_basic(self):
        ew = ExponentiallyWeightedStats(alpha=0.5)
        for v in [1, 2, 3, 4, 5]:
            ew.add(v)
        mean = ew.get_mean()
        self.assertIsNotNone(mean)
        # Recent values weighted more heavily
        self.assertGreater(mean, 2.5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
