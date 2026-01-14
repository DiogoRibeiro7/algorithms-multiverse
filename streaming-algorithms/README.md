# Streaming & Online Algorithms

A comprehensive collection of algorithms for processing data streams with limited memory, including cardinality estimation, sampling, statistics computation, and sliding window operations.

## 📚 Table of Contents

- [Overview](#overview)
- [Implemented Algorithms](#implemented-algorithms)
- [Installation](#installation)
- [Algorithm Categories](#algorithm-categories)
- [Usage Examples](#usage-examples)
- [Performance Comparison](#performance-comparison)
- [Applications](#applications)
- [References](#references)

## 🎯 Overview

Streaming algorithms are designed to process large or infinite data streams using sublinear space (much less memory than the size of the input). These algorithms make a single pass (or few passes) over the data and provide approximate answers with provable error bounds.

### Key Properties

- **Limited Memory**: O(log n) or O(polylog n) space for streams of size n
- **Single Pass**: Most algorithms see each element only once
- **Approximate Answers**: Trade accuracy for efficiency
- **Real-time Processing**: Constant or logarithmic update time

## 📊 Implemented Algorithms

### 1. Cardinality Estimation (`hyperloglog.py`)

| Algorithm | Description | Space | Error |
|-----------|-------------|-------|-------|
| **HyperLogLog** | Standard cardinality estimation | O(m) | ±1.04/√m |
| **HyperLogLog++** | Enhanced with bias correction | O(m) | Better for small sets |
| **Linear Counting** | Simple bitmap approach | O(n) | Exact for small sets |
| **Flajolet-Martin** | Historical algorithm | O(log n) | Higher variance |
| **Morris Counting** | Approximate counting | O(log log n) | ±ε |
| **Counting Bloom Filter** | Frequency + membership | O(m) | False positive rate |

### 2. Sampling Algorithms (`reservoir_sampling.py`)

| Algorithm | Description | Space | Properties |
|-----------|-------------|-------|------------|
| **Reservoir Sampling** | Uniform random sample | O(k) | Each item prob k/n |
| **Weighted Reservoir** | Probability ∝ weight | O(k) | Weighted sampling |
| **Stratified Sampling** | Balanced across strata | O(k×s) | Ensures diversity |
| **Priority Sampling** | Unbiased sum estimates | O(k) | VarOpt sampling |
| **Sliding Window Sampling** | Sample from recent items | O(k) | Time-sensitive |
| **Distributed Sampling** | Merge parallel samples | O(k×p) | Scalable |

### 3. Online Statistics (`online_statistics.py`)

| Algorithm | Description | Space | Update Time |
|-----------|-------------|-------|-------------|
| **Online Median** | Two-heap approach | O(n) | O(log n) |
| **Sliding Median** | Window-based median | O(k) | O(log k) |
| **Greenwald-Khanna** | Quantile estimation | O(log εn) | O(log εn) |
| **T-Digest** | Accurate extreme quantiles | O(δ) | O(1) |
| **P-Square** | Single quantile tracking | O(1) | O(1) |
| **Welford's Algorithm** | Mean and variance | O(1) | O(1) |
| **EWMA** | Exponentially weighted stats | O(1) | O(1) |

### 4. Sliding Window (`sliding_window.py`)

| Algorithm | Description | Space | Query Time |
|-----------|-------------|-------|------------|
| **Sliding Max/Min** | Monotonic deque | O(k) | O(1) |
| **Sliding Average** | Running sum/count | O(1) | O(1) |
| **Sliding Unique** | Distinct elements | O(k) | O(1) |
| **SWAG** | General aggregation | O(k) | O(1) amortized |
| **Exponential Histogram** | Bit counting | O(log W/ε) | O(log W/ε) |
| **Time-based Window** | Temporal windows | O(k) | O(1) |
| **Session Window** | Activity-based | O(k) | O(1) |

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/algorithms-multiverse.git
cd algorithms-multiverse/streaming-algorithms

# No external dependencies for basic functionality
# For enhanced features, install numpy
pip install numpy
```

## 💻 Usage Examples

### Example 1: Cardinality Estimation with HyperLogLog

```python
from hyperloglog import HyperLogLog

# Create HyperLogLog with precision 14 (16384 buckets)
hll = HyperLogLog(precision=14)

# Add items to stream
for user_id in user_stream:
    hll.add(user_id)

# Get cardinality estimate
unique_users = hll.count()
print(f"Estimated unique users: {unique_users}")

# Merge multiple HLLs (for distributed systems)
hll1 = HyperLogLog(14)
hll2 = HyperLogLog(14)
# ... add items to each ...
hll1.merge(hll2)
total_unique = hll1.count()
```

### Example 2: Reservoir Sampling

```python
from reservoir_sampling import ReservoirSampling, WeightedReservoirSampling

# Uniform sampling
sampler = ReservoirSampling(k=100)  # Keep 100 samples

for item in huge_stream:
    sampler.add(item)

sample = sampler.get_sample()  # Get uniform random sample

# Weighted sampling
weighted_sampler = WeightedReservoirSampling(k=100)

for item, importance in scored_stream:
    weighted_sampler.add(item, weight=importance)

weighted_sample = weighted_sampler.get_sample()
```

### Example 3: Online Statistics

```python
from online_statistics import OnlineMedian, TDigest, WelfordVariance

# Online median
median_finder = OnlineMedian()
for value in stream:
    median_finder.add(value)
    current_median = median_finder.get_median()

# Quantile estimation with T-Digest
tdigest = TDigest(delta=100)
for value in stream:
    tdigest.add(value)

p99 = tdigest.get_quantile(0.99)  # 99th percentile
p999 = tdigest.get_quantile(0.999)  # 99.9th percentile

# Online mean and variance
welford = WelfordVariance()
for value in stream:
    welford.add(value)

mean = welford.get_mean()
stddev = welford.get_stddev()
```

### Example 4: Sliding Window Operations

```python
from sliding_window import SlidingWindowMaximum, SWAG

# Sliding window maximum
sw_max = SlidingWindowMaximum(k=100)

for price in stock_prices:
    window_max = sw_max.add(price)
    print(f"100-period high: {window_max}")

# General sliding window aggregation
# Example: sliding window product
sw_product = SWAG(
    k=10,
    identity=1,
    combine=lambda a, b: a * b
)

for value in stream:
    sw_product.add(value)
    product = sw_product.query()
```

## 📈 Performance Comparison

### Cardinality Estimation Accuracy vs Memory

| Algorithm | Memory (bytes) | Error @ 1M items | Error @ 1B items |
|-----------|---------------|------------------|------------------|
| Exact Set | 40M / 40B | 0% | 0% |
| HLL(10) | 1,024 | ~3.3% | ~3.3% |
| HLL(14) | 16,384 | ~0.8% | ~0.8% |
| HLL(16) | 65,536 | ~0.4% | ~0.4% |
| Linear Counting | 1.25M | ~2% | Fails |

### Quantile Estimation Comparison

| Algorithm | Memory | Update Time | Query Time | Best For |
|-----------|--------|-------------|------------|----------|
| Sorted List | O(n) | O(n) | O(1) | Small data |
| GK Quantiles | O(log εn) | O(log εn) | O(log εn) | General |
| T-Digest | O(δ) | O(1) | O(log δ) | Extremes |
| P-Square | O(1) | O(1) | O(1) | Single quantile |

### Sampling Methods Trade-offs

| Method | Memory | Bias | Use Case |
|--------|--------|------|----------|
| Reservoir | O(k) | None | General uniform |
| Weighted | O(k) | None | Importance sampling |
| Priority | O(k) | None | Sum estimation |
| Window | O(k) | Recency | Time-sensitive |

## 🎯 Applications

### Real-World Use Cases

#### 1. **Web Analytics**
- Unique visitor counting (HyperLogLog)
- Session analysis (Session Windows)
- Real-time statistics dashboards

#### 2. **Network Monitoring**
- DDoS detection (Sliding window frequency)
- Traffic sampling (Reservoir sampling)
- Anomaly detection (Online statistics)

#### 3. **Database Systems**
- Query optimization (Approximate counts)
- Distinct value estimation
- Histogram maintenance

#### 4. **Distributed Systems**
- Distributed counting (HLL merge)
- Load balancing (Consistent hashing)
- Monitoring at scale

#### 5. **Financial Systems**
- Real-time risk metrics (Sliding windows)
- High-frequency trading (Online statistics)
- Fraud detection (Frequency counting)

#### 6. **Machine Learning**
- Online learning (Incremental statistics)
- Feature hashing (Count-Min Sketch)
- Data preprocessing (Sampling)

## 🔧 Advanced Features

### Memory-Accuracy Trade-offs

```python
# Example: Choosing HyperLogLog precision
def choose_hll_precision(expected_cardinality, max_error_rate):
    """
    Choose optimal HLL precision based on requirements.

    Standard error = 1.04 / sqrt(m) where m = 2^precision
    """
    import math

    for precision in range(4, 17):
        m = 2 ** precision
        error = 1.04 / math.sqrt(m)
        memory_bytes = m

        if error <= max_error_rate:
            return precision, memory_bytes, error

    return 16, 65536, 1.04 / math.sqrt(65536)

# 1% error tolerance
precision, memory, error = choose_hll_precision(1000000, 0.01)
print(f"Use precision={precision}, Memory={memory} bytes, Error≈{error*100:.2f}%")
```

### Distributed Stream Processing

```python
# Example: Parallel HyperLogLog
def distributed_cardinality(streams):
    """Compute cardinality across multiple streams."""
    hlls = []

    # Process streams in parallel
    for stream in streams:
        hll = HyperLogLog(precision=14)
        for item in stream:
            hll.add(item)
        hlls.append(hll)

    # Merge results
    merged = hlls[0]
    for hll in hlls[1:]:
        merged.merge(hll)

    return merged.count()
```

### Adaptive Algorithms

```python
# Example: Adaptive sampling rate
class AdaptiveSampler:
    def __init__(self, target_memory):
        self.target_memory = target_memory
        self.seen = 0
        self.sampler = None

    def add(self, item):
        self.seen += 1

        # Adjust sample size based on stream rate
        if self.seen % 1000 == 0:
            expected_total = self.seen * 10  # Projection
            sample_size = min(
                self.target_memory // 8,  # 8 bytes per item
                expected_total // 100  # 1% sample
            )

            if self.sampler is None or sample_size != self.sampler.k:
                self.sampler = ReservoirSampling(sample_size)

        if self.sampler:
            self.sampler.add(item)
```

## 📊 Theoretical Guarantees

### Error Bounds

| Algorithm | Guarantee | Confidence |
|-----------|-----------|------------|
| HyperLogLog | ε ≤ 1.04/√m | 65% (1σ) |
| GK Quantiles | rank error ≤ εn | 100% |
| Count-Min Sketch | count ≤ actual + ε‖a‖₁ | 1-δ |
| Reservoir Sampling | P(i ∈ S) = k/n | 100% |

### Space Complexity

- **Cardinality**: O(log log n) to O(log n)
- **Quantiles**: O(log n) to O(1/ε log εn)
- **Frequency**: O(1/ε log 1/δ)
- **Sampling**: O(k) for k samples

## 📚 References

### Papers
- Flajolet et al. (2007) - "HyperLogLog: the analysis of a near-optimal cardinality estimation algorithm"
- Vitter (1985) - "Random Sampling with a Reservoir"
- Greenwald & Khanna (2001) - "Space-Efficient Online Computation of Quantile Summaries"
- Dunning & Ertl (2019) - "Computing Extremely Accurate Quantiles Using t-Digests"
- Cormode & Muthukrishnan (2005) - "An Improved Data Stream Summary: The Count-Min Sketch"

### Books
- "Data Streams: Algorithms and Applications" - Muthukrishnan
- "Synopses for Massive Data" - Cormode et al.
- "Mining of Massive Datasets" - Leskovec, Rajaraman, Ullman

## ⚠️ Important Notes

1. **Approximate Nature**: These algorithms trade accuracy for efficiency
2. **Parameter Tuning**: Performance depends heavily on parameters
3. **Use Cases**: Choose algorithms based on specific requirements
4. **Distributed Systems**: Many algorithms support merging for parallel processing
5. **Memory Bounds**: Always consider worst-case memory usage

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional streaming algorithms (AMS Sketch, F2 estimation)
- GPU implementations for parallel processing
- Integration with stream processing frameworks
- Visualization tools
- More real-world examples

---

**Part of the Algorithms Multiverse** - A comprehensive collection of algorithms across multiple domains.

**Last Updated**: January 2026