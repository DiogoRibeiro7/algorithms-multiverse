/**
 * Streaming Algorithms Module
 * Real-time data processing and online algorithms
 */

// ============================================
// Reservoir Sampling
// ============================================

/**
 * Basic Reservoir Sampling (Algorithm R)
 * Maintains a uniform random sample of k items from a stream
 */
export class ReservoirSampler {
    constructor(k) {
        this.k = k; // Reservoir size
        this.reservoir = [];
        this.count = 0;
    }

    /**
     * Add an item to the stream
     */
    add(item) {
        this.count++;

        if (this.reservoir.length < this.k) {
            // Reservoir not full, add item
            this.reservoir.push(item);
        } else {
            // Randomly decide whether to include item
            const j = Math.floor(Math.random() * this.count);
            if (j < this.k) {
                this.reservoir[j] = item;
            }
        }
    }

    /**
     * Add multiple items
     */
    addAll(items) {
        for (const item of items) {
            this.add(item);
        }
    }

    /**
     * Get current sample
     */
    getSample() {
        return [...this.reservoir];
    }

    /**
     * Reset the sampler
     */
    reset() {
        this.reservoir = [];
        this.count = 0;
    }

    /**
     * Get statistics
     */
    getStats() {
        return {
            sampleSize: this.reservoir.length,
            totalSeen: this.count,
            isFull: this.reservoir.length === this.k
        };
    }
}

/**
 * Weighted Reservoir Sampling (Algorithm A-Res)
 * Samples items with probability proportional to their weight
 */
export class WeightedReservoirSampler {
    constructor(k) {
        this.k = k;
        this.reservoir = [];
        this.keys = [];
        this.count = 0;
    }

    /**
     * Add weighted item to stream
     */
    add(item, weight) {
        this.count++;
        const key = Math.pow(Math.random(), 1 / weight);

        if (this.reservoir.length < this.k) {
            this.reservoir.push(item);
            this.keys.push(key);
        } else {
            // Find minimum key
            let minIdx = 0;
            let minKey = this.keys[0];
            for (let i = 1; i < this.k; i++) {
                if (this.keys[i] < minKey) {
                    minKey = this.keys[i];
                    minIdx = i;
                }
            }

            // Replace if new key is larger
            if (key > minKey) {
                this.reservoir[minIdx] = item;
                this.keys[minIdx] = key;
            }
        }
    }

    /**
     * Get current sample
     */
    getSample() {
        return [...this.reservoir];
    }

    reset() {
        this.reservoir = [];
        this.keys = [];
        this.count = 0;
    }
}

/**
 * Stratified Reservoir Sampling
 * Maintains separate reservoirs for different strata
 */
export class StratifiedReservoirSampler {
    constructor(k, stratumExtractor = (item) => 'default') {
        this.k = k; // Total reservoir size
        this.stratumExtractor = stratumExtractor;
        this.strata = new Map();
        this.totalCount = 0;
    }

    /**
     * Add item to appropriate stratum
     */
    add(item) {
        this.totalCount++;
        const stratum = this.stratumExtractor(item);

        if (!this.strata.has(stratum)) {
            this.strata.set(stratum, {
                reservoir: [],
                count: 0
            });
        }

        const stratumData = this.strata.get(stratum);
        stratumData.count++;

        // Allocate space proportionally
        const stratumK = Math.max(1, Math.floor(this.k * stratumData.count / this.totalCount));

        if (stratumData.reservoir.length < stratumK) {
            stratumData.reservoir.push(item);
        } else {
            const j = Math.floor(Math.random() * stratumData.count);
            if (j < stratumK) {
                stratumData.reservoir[j] = item;
            }
        }
    }

    /**
     * Get combined sample
     */
    getSample() {
        const sample = [];
        for (const stratumData of this.strata.values()) {
            sample.push(...stratumData.reservoir);
        }

        // Limit to k items if necessary
        if (sample.length > this.k) {
            // Random sample from combined
            const finalSample = [];
            const indices = new Set();
            while (finalSample.length < this.k) {
                const idx = Math.floor(Math.random() * sample.length);
                if (!indices.has(idx)) {
                    indices.add(idx);
                    finalSample.push(sample[idx]);
                }
            }
            return finalSample;
        }

        return sample;
    }

    /**
     * Get per-stratum statistics
     */
    getStrataStats() {
        const stats = {};
        for (const [stratum, data] of this.strata) {
            stats[stratum] = {
                sampleSize: data.reservoir.length,
                totalSeen: data.count,
                proportion: data.count / this.totalCount
            };
        }
        return stats;
    }
}

// ============================================
// Streaming Statistics
// ============================================

/**
 * Online Mean and Variance (Welford's algorithm)
 */
export class StreamingStats {
    constructor() {
        this.count = 0;
        this.mean = 0;
        this.m2 = 0; // Sum of squared differences from mean
        this.min = Infinity;
        this.max = -Infinity;
        this.sum = 0;
    }

    /**
     * Add a value to the stream
     */
    add(value) {
        this.count++;
        this.sum += value;

        // Update min/max
        if (value < this.min) this.min = value;
        if (value > this.max) this.max = value;

        // Welford's online algorithm
        const delta = value - this.mean;
        this.mean += delta / this.count;
        const delta2 = value - this.mean;
        this.m2 += delta * delta2;
    }

    /**
     * Add multiple values
     */
    addAll(values) {
        for (const value of values) {
            this.add(value);
        }
    }

    /**
     * Get current mean
     */
    getMean() {
        return this.count > 0 ? this.mean : 0;
    }

    /**
     * Get variance
     */
    getVariance() {
        if (this.count < 2) return 0;
        return this.m2 / (this.count - 1);
    }

    /**
     * Get standard deviation
     */
    getStdDev() {
        return Math.sqrt(this.getVariance());
    }

    /**
     * Get all statistics
     */
    getStats() {
        return {
            count: this.count,
            mean: this.getMean(),
            variance: this.getVariance(),
            stdDev: this.getStdDev(),
            min: this.count > 0 ? this.min : null,
            max: this.count > 0 ? this.max : null,
            sum: this.sum
        };
    }

    /**
     * Reset statistics
     */
    reset() {
        this.count = 0;
        this.mean = 0;
        this.m2 = 0;
        this.min = Infinity;
        this.max = -Infinity;
        this.sum = 0;
    }
}

/**
 * Exponentially Weighted Moving Average (EWMA)
 */
export class EWMA {
    constructor(alpha = 0.1, initialValue = null) {
        this.alpha = alpha; // Smoothing factor (0 < alpha < 1)
        this.value = initialValue;
        this.initialized = initialValue !== null;
        this.count = 0;
    }

    /**
     * Update with new value
     */
    update(value) {
        this.count++;

        if (!this.initialized) {
            this.value = value;
            this.initialized = true;
        } else {
            this.value = this.alpha * value + (1 - this.alpha) * this.value;
        }

        return this.value;
    }

    /**
     * Get current EWMA value
     */
    getValue() {
        return this.value;
    }

    /**
     * Reset
     */
    reset(initialValue = null) {
        this.value = initialValue;
        this.initialized = initialValue !== null;
        this.count = 0;
    }
}

/**
 * Streaming Quantiles using P² algorithm
 */
export class StreamingQuantiles {
    constructor(quantiles = [0.25, 0.5, 0.75]) {
        this.quantiles = quantiles.sort((a, b) => a - b);
        this.markers = [];
        this.positions = [];
        this.desired = [];
        this.count = 0;
        this.buffer = [];
        this.bufferSize = 5;
    }

    /**
     * Add value to stream
     */
    add(value) {
        this.count++;

        // Initial phase: collect first few observations
        if (this.buffer.length < this.bufferSize) {
            this.buffer.push(value);

            if (this.buffer.length === this.bufferSize) {
                this.initialize();
            }
            return;
        }

        // Update markers
        this.updateMarkers(value);
    }

    /**
     * Initialize P² algorithm
     */
    initialize() {
        this.buffer.sort((a, b) => a - b);

        // Initialize marker positions and values
        const n = this.bufferSize;
        for (let i = 0; i < n; i++) {
            this.markers[i] = this.buffer[i];
            this.positions[i] = i + 1;
        }

        // Calculate desired positions
        for (let i = 0; i < n; i++) {
            if (i === 0) {
                this.desired[i] = 1;
            } else if (i === n - 1) {
                this.desired[i] = this.count;
            } else {
                const q = this.quantiles[Math.min(i - 1, this.quantiles.length - 1)];
                this.desired[i] = 1 + (n - 1) * q;
            }
        }
    }

    /**
     * Update markers with new observation
     */
    updateMarkers(value) {
        // Find cell k
        let k = 0;
        if (value < this.markers[0]) {
            this.markers[0] = value;
            k = 0;
        } else if (value >= this.markers[this.markers.length - 1]) {
            this.markers[this.markers.length - 1] = value;
            k = this.markers.length - 1;
        } else {
            for (let i = 1; i < this.markers.length; i++) {
                if (value < this.markers[i]) {
                    k = i - 1;
                    break;
                }
            }
        }

        // Update positions
        for (let i = k + 1; i < this.positions.length; i++) {
            this.positions[i]++;
        }

        // Update desired positions
        for (let i = 1; i < this.desired.length - 1; i++) {
            const q = this.quantiles[Math.min(i - 1, this.quantiles.length - 1)];
            this.desired[i] += q;
        }
        this.desired[this.desired.length - 1] = this.count;

        // Adjust markers
        for (let i = 1; i < this.markers.length - 1; i++) {
            const d = this.desired[i] - this.positions[i];
            if ((d >= 1 && this.positions[i + 1] - this.positions[i] > 1) ||
                (d <= -1 && this.positions[i - 1] - this.positions[i] < -1)) {
                const sign = d > 0 ? 1 : -1;

                // Parabolic interpolation
                const qi = this.parabolicInterpolation(i, sign);
                if (this.markers[i - 1] < qi && qi < this.markers[i + 1]) {
                    this.markers[i] = qi;
                } else {
                    // Linear interpolation
                    this.markers[i] = this.linearInterpolation(i, sign);
                }
                this.positions[i] += sign;
            }
        }
    }

    /**
     * Parabolic interpolation
     */
    parabolicInterpolation(i, sign) {
        const qi = this.markers[i];
        const qim1 = this.markers[i - 1];
        const qip1 = this.markers[i + 1];
        const ni = this.positions[i];
        const nim1 = this.positions[i - 1];
        const nip1 = this.positions[i + 1];

        const a = (ni - nim1 + sign) * (qip1 - qi) / (nip1 - ni) +
                 (nip1 - ni - sign) * (qi - qim1) / (ni - nim1);
        const b = (nip1 - ni);

        return qi + sign * a / b;
    }

    /**
     * Linear interpolation
     */
    linearInterpolation(i, sign) {
        const qi = this.markers[i];
        const qj = this.markers[i + sign];
        const ni = this.positions[i];
        const nj = this.positions[i + sign];

        return qi + sign * (qj - qi) / (nj - ni);
    }

    /**
     * Get estimated quantiles
     */
    getQuantiles() {
        if (this.buffer.length < this.bufferSize) {
            // Not enough data yet
            if (this.buffer.length === 0) return {};

            const sorted = [...this.buffer].sort((a, b) => a - b);
            const result = {};
            for (const q of this.quantiles) {
                const idx = Math.floor(q * (sorted.length - 1));
                result[q] = sorted[idx];
            }
            return result;
        }

        // Return P² estimates
        const result = {};
        for (let i = 0; i < this.quantiles.length; i++) {
            result[this.quantiles[i]] = this.markers[i + 1];
        }
        return result;
    }
}

// ============================================
// Count-Distinct Algorithms
// ============================================

/**
 * HyperLogLog for cardinality estimation
 */
export class HyperLogLog {
    constructor(precision = 14) {
        this.precision = precision;
        this.m = Math.pow(2, precision); // Number of buckets
        this.buckets = new Uint8Array(this.m);
        this.alphaMM = this.getAlpha() * this.m * this.m;
    }

    /**
     * Add item to the stream
     */
    add(item) {
        const hash = this.hash(item);
        const j = hash & ((1 << this.precision) - 1); // First p bits
        const w = hash >>> this.precision; // Remaining bits
        const leadingZeros = this.countLeadingZeros(w) + 1;

        if (leadingZeros > this.buckets[j]) {
            this.buckets[j] = leadingZeros;
        }
    }

    /**
     * Add multiple items
     */
    addAll(items) {
        for (const item of items) {
            this.add(item);
        }
    }

    /**
     * Estimate cardinality
     */
    cardinality() {
        let sum = 0;
        let zeros = 0;

        for (let i = 0; i < this.m; i++) {
            sum += Math.pow(2, -this.buckets[i]);
            if (this.buckets[i] === 0) {
                zeros++;
            }
        }

        let estimate = this.alphaMM / sum;

        // Apply bias correction
        if (estimate <= 2.5 * this.m) {
            // Small range correction
            if (zeros !== 0) {
                estimate = this.m * Math.log(this.m / zeros);
            }
        } else if (estimate > (1 / 30) * Math.pow(2, 32)) {
            // Large range correction
            estimate = -Math.pow(2, 32) * Math.log(1 - estimate / Math.pow(2, 32));
        }

        return Math.round(estimate);
    }

    /**
     * Merge with another HyperLogLog
     */
    merge(other) {
        if (other.precision !== this.precision) {
            throw new Error('Cannot merge HyperLogLogs with different precisions');
        }

        for (let i = 0; i < this.m; i++) {
            if (other.buckets[i] > this.buckets[i]) {
                this.buckets[i] = other.buckets[i];
            }
        }
    }

    /**
     * Reset the counter
     */
    reset() {
        this.buckets.fill(0);
    }

    /**
     * Get alpha constant
     */
    getAlpha() {
        if (this.m >= 128) return 0.7213 / (1 + 1.079 / this.m);
        if (this.m >= 64) return 0.709;
        if (this.m >= 32) return 0.697;
        if (this.m >= 16) return 0.673;
        return 0.5;
    }

    /**
     * Simple hash function (MurmurHash3-like)
     */
    hash(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            hash = ((hash << 5) - hash) + str.charCodeAt(i);
            hash = hash & 0xFFFFFFFF;
        }
        return hash >>> 0;
    }

    /**
     * Count leading zeros
     */
    countLeadingZeros(x) {
        if (x === 0) return 32 - this.precision;
        let n = 0;
        if ((x & 0xFFFF0000) === 0) { n += 16; x <<= 16; }
        if ((x & 0xFF000000) === 0) { n += 8; x <<= 8; }
        if ((x & 0xF0000000) === 0) { n += 4; x <<= 4; }
        if ((x & 0xC0000000) === 0) { n += 2; x <<= 2; }
        if ((x & 0x80000000) === 0) { n += 1; }
        return n;
    }
}

/**
 * Count-Min Sketch for frequency estimation
 */
export class CountMinSketch {
    constructor(width = 1000, depth = 5) {
        this.width = width;
        this.depth = depth;
        this.table = Array(depth).fill().map(() => new Uint32Array(width));
        this.hashSeeds = Array(depth).fill().map((_, i) => i + 1);
    }

    /**
     * Add item to the sketch
     */
    add(item, count = 1) {
        for (let i = 0; i < this.depth; i++) {
            const j = this.hash(item, this.hashSeeds[i]) % this.width;
            this.table[i][j] += count;
        }
    }

    /**
     * Estimate frequency of an item
     */
    estimate(item) {
        let minCount = Infinity;
        for (let i = 0; i < this.depth; i++) {
            const j = this.hash(item, this.hashSeeds[i]) % this.width;
            minCount = Math.min(minCount, this.table[i][j]);
        }
        return minCount;
    }

    /**
     * Merge with another sketch
     */
    merge(other) {
        if (other.width !== this.width || other.depth !== this.depth) {
            throw new Error('Cannot merge sketches with different dimensions');
        }

        for (let i = 0; i < this.depth; i++) {
            for (let j = 0; j < this.width; j++) {
                this.table[i][j] += other.table[i][j];
            }
        }
    }

    /**
     * Reset the sketch
     */
    reset() {
        for (let i = 0; i < this.depth; i++) {
            this.table[i].fill(0);
        }
    }

    /**
     * Hash function with seed
     */
    hash(str, seed) {
        let hash = seed;
        for (let i = 0; i < str.length; i++) {
            hash = ((hash << 5) - hash) + str.charCodeAt(i);
            hash = hash & 0xFFFFFFFF;
        }
        return Math.abs(hash);
    }
}

// ============================================
// Frequent Elements
// ============================================

/**
 * Misra-Gries algorithm for finding frequent items
 */
export class MisraGries {
    constructor(k) {
        this.k = k; // Find elements with frequency > n/k
        this.counters = new Map();
        this.totalCount = 0;
    }

    /**
     * Process an item
     */
    add(item) {
        this.totalCount++;

        if (this.counters.has(item)) {
            this.counters.set(item, this.counters.get(item) + 1);
        } else if (this.counters.size < this.k - 1) {
            this.counters.set(item, 1);
        } else {
            // Decrement all counters
            const toDelete = [];
            for (const [key, count] of this.counters) {
                if (count === 1) {
                    toDelete.push(key);
                } else {
                    this.counters.set(key, count - 1);
                }
            }
            for (const key of toDelete) {
                this.counters.delete(key);
            }
        }
    }

    /**
     * Get frequent items (candidates)
     */
    getFrequentItems(threshold = null) {
        if (threshold === null) {
            threshold = this.totalCount / this.k;
        }

        const frequent = [];
        for (const [item, count] of this.counters) {
            if (count >= threshold) {
                frequent.push({ item, estimatedCount: count });
            }
        }
        return frequent;
    }

    /**
     * Get all tracked items
     */
    getAll() {
        return Array.from(this.counters.entries()).map(([item, count]) => ({
            item,
            estimatedCount: count,
            minFrequency: count / this.totalCount
        }));
    }

    reset() {
        this.counters.clear();
        this.totalCount = 0;
    }
}

/**
 * Space-Saving algorithm for top-k elements
 */
export class SpaceSaving {
    constructor(k) {
        this.k = k;
        this.counters = new Map();
        this.totalCount = 0;
    }

    /**
     * Process an item
     */
    add(item) {
        this.totalCount++;

        if (this.counters.has(item)) {
            const counter = this.counters.get(item);
            counter.count++;
            counter.error = counter.error || 0;
        } else if (this.counters.size < this.k) {
            this.counters.set(item, { count: 1, error: 0 });
        } else {
            // Replace item with minimum count
            let minItem = null;
            let minCount = Infinity;

            for (const [key, counter] of this.counters) {
                if (counter.count < minCount) {
                    minCount = counter.count;
                    minItem = key;
                }
            }

            this.counters.delete(minItem);
            this.counters.set(item, {
                count: minCount + 1,
                error: minCount
            });
        }
    }

    /**
     * Get top-k items
     */
    getTopK() {
        const items = Array.from(this.counters.entries())
            .map(([item, counter]) => ({
                item,
                count: counter.count,
                error: counter.error
            }))
            .sort((a, b) => b.count - a.count);

        return items.slice(0, this.k);
    }

    reset() {
        this.counters.clear();
        this.totalCount = 0;
    }
}

// ============================================
// Sliding Window Algorithms
// ============================================

/**
 * Sliding Window Statistics
 */
export class SlidingWindowStats {
    constructor(windowSize) {
        this.windowSize = windowSize;
        this.window = [];
        this.sum = 0;
        this.sumSquares = 0;
    }

    /**
     * Add value to window
     */
    add(value) {
        this.window.push(value);
        this.sum += value;
        this.sumSquares += value * value;

        if (this.window.length > this.windowSize) {
            const removed = this.window.shift();
            this.sum -= removed;
            this.sumSquares -= removed * removed;
        }

        return this.getStats();
    }

    /**
     * Get current statistics
     */
    getStats() {
        const n = this.window.length;
        if (n === 0) {
            return { mean: 0, variance: 0, stdDev: 0, min: null, max: null };
        }

        const mean = this.sum / n;
        const variance = n > 1 ?
            (this.sumSquares - n * mean * mean) / (n - 1) : 0;

        return {
            mean,
            variance,
            stdDev: Math.sqrt(variance),
            min: Math.min(...this.window),
            max: Math.max(...this.window),
            sum: this.sum,
            count: n
        };
    }

    reset() {
        this.window = [];
        this.sum = 0;
        this.sumSquares = 0;
    }
}

/**
 * Sliding Window Maximum/Minimum
 */
export class SlidingWindowExtreme {
    constructor(windowSize, isMax = true) {
        this.windowSize = windowSize;
        this.isMax = isMax;
        this.window = [];
        this.deque = []; // Monotonic deque for O(1) extreme finding
    }

    /**
     * Add value to window
     */
    add(value, timestamp = Date.now()) {
        const entry = { value, timestamp };
        this.window.push(entry);

        // Remove old entries
        while (this.window.length > 0 &&
               this.window[0].timestamp <= timestamp - this.windowSize) {
            this.window.shift();
        }

        // Update monotonic deque
        if (this.isMax) {
            while (this.deque.length > 0 &&
                   this.deque[this.deque.length - 1].value <= value) {
                this.deque.pop();
            }
        } else {
            while (this.deque.length > 0 &&
                   this.deque[this.deque.length - 1].value >= value) {
                this.deque.pop();
            }
        }

        this.deque.push(entry);

        // Remove outdated deque entries
        while (this.deque.length > 0 &&
               this.deque[0].timestamp <= timestamp - this.windowSize) {
            this.deque.shift();
        }

        return this.getExtreme();
    }

    /**
     * Get current extreme value
     */
    getExtreme() {
        return this.deque.length > 0 ? this.deque[0].value : null;
    }

    /**
     * Get all values in window
     */
    getWindow() {
        return this.window.map(e => e.value);
    }

    reset() {
        this.window = [];
        this.deque = [];
    }
}

/**
 * Sliding Window Counter
 */
export class SlidingWindowCounter {
    constructor(windowSize, granularity = 1000) {
        this.windowSize = windowSize;
        this.granularity = granularity; // Time bucket size in ms
        this.buckets = new Map();
        this.total = 0;
    }

    /**
     * Increment counter
     */
    increment(count = 1, timestamp = Date.now()) {
        const bucket = Math.floor(timestamp / this.granularity);

        if (!this.buckets.has(bucket)) {
            this.buckets.set(bucket, 0);
        }
        this.buckets.set(bucket, this.buckets.get(bucket) + count);
        this.total += count;

        this.cleanup(timestamp);
    }

    /**
     * Get current count
     */
    getCount(timestamp = Date.now()) {
        this.cleanup(timestamp);

        let count = 0;
        const minBucket = Math.floor((timestamp - this.windowSize) / this.granularity);

        for (const [bucket, value] of this.buckets) {
            if (bucket >= minBucket) {
                count += value;
            }
        }

        return count;
    }

    /**
     * Get rate (events per second)
     */
    getRate(timestamp = Date.now()) {
        const count = this.getCount(timestamp);
        return count / (this.windowSize / 1000);
    }

    /**
     * Clean up old buckets
     */
    cleanup(timestamp = Date.now()) {
        const minBucket = Math.floor((timestamp - this.windowSize) / this.granularity);

        for (const bucket of this.buckets.keys()) {
            if (bucket < minBucket) {
                this.total -= this.buckets.get(bucket);
                this.buckets.delete(bucket);
            }
        }
    }

    reset() {
        this.buckets.clear();
        this.total = 0;
    }
}

// ============================================
// Bloom Filter (Probabilistic Membership)
// ============================================

/**
 * Bloom Filter for membership testing
 */
export class BloomFilter {
    constructor(expectedItems = 1000, falsePositiveRate = 0.01) {
        // Calculate optimal parameters
        this.m = Math.ceil(-expectedItems * Math.log(falsePositiveRate) / Math.pow(Math.log(2), 2));
        this.k = Math.ceil(this.m / expectedItems * Math.log(2));
        this.bits = new Uint8Array(Math.ceil(this.m / 8));
        this.count = 0;
    }

    /**
     * Add item to filter
     */
    add(item) {
        const hashes = this.getHashes(item);
        for (const hash of hashes) {
            const byte = Math.floor(hash / 8);
            const bit = hash % 8;
            this.bits[byte] |= (1 << bit);
        }
        this.count++;
    }

    /**
     * Test membership
     */
    contains(item) {
        const hashes = this.getHashes(item);
        for (const hash of hashes) {
            const byte = Math.floor(hash / 8);
            const bit = hash % 8;
            if (!(this.bits[byte] & (1 << bit))) {
                return false;
            }
        }
        return true;
    }

    /**
     * Get k hash values for an item
     */
    getHashes(item) {
        const hashes = [];
        let h1 = this.hash1(item);
        let h2 = this.hash2(item);

        for (let i = 0; i < this.k; i++) {
            hashes.push((h1 + i * h2) % this.m);
        }

        return hashes;
    }

    /**
     * First hash function
     */
    hash1(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            hash = ((hash << 5) - hash) + str.charCodeAt(i);
            hash = hash & 0xFFFFFFFF;
        }
        return Math.abs(hash);
    }

    /**
     * Second hash function
     */
    hash2(str) {
        let hash = 5381;
        for (let i = 0; i < str.length; i++) {
            hash = ((hash << 5) + hash) + str.charCodeAt(i);
        }
        return Math.abs(hash);
    }

    /**
     * Estimate false positive rate
     */
    getFalsePositiveRate() {
        const filledBits = this.countSetBits();
        const ratio = filledBits / this.m;
        return Math.pow(ratio, this.k);
    }

    /**
     * Count set bits
     */
    countSetBits() {
        let count = 0;
        for (let i = 0; i < this.bits.length; i++) {
            let byte = this.bits[i];
            while (byte) {
                count += byte & 1;
                byte >>= 1;
            }
        }
        return count;
    }

    /**
     * Reset filter
     */
    reset() {
        this.bits.fill(0);
        this.count = 0;
    }
}

// ============================================
// Online Learning Algorithms
// ============================================

/**
 * Online Linear Regression (Stochastic Gradient Descent)
 */
export class OnlineLinearRegression {
    constructor(featureCount, learningRate = 0.01) {
        this.weights = new Array(featureCount).fill(0);
        this.bias = 0;
        this.learningRate = learningRate;
        this.count = 0;
        this.totalError = 0;
    }

    /**
     * Update model with new sample
     */
    update(features, target) {
        this.count++;

        // Make prediction
        const prediction = this.predict(features);
        const error = target - prediction;
        this.totalError += error * error;

        // Update weights (SGD)
        for (let i = 0; i < this.weights.length; i++) {
            this.weights[i] += this.learningRate * error * features[i];
        }
        this.bias += this.learningRate * error;

        // Decay learning rate
        this.learningRate *= 0.999;

        return prediction;
    }

    /**
     * Make prediction
     */
    predict(features) {
        let sum = this.bias;
        for (let i = 0; i < features.length; i++) {
            sum += this.weights[i] * features[i];
        }
        return sum;
    }

    /**
     * Get mean squared error
     */
    getMSE() {
        return this.count > 0 ? this.totalError / this.count : 0;
    }

    reset() {
        this.weights.fill(0);
        this.bias = 0;
        this.count = 0;
        this.totalError = 0;
    }
}

/**
 * Online K-Means clustering
 */
export class OnlineKMeans {
    constructor(k, dimension) {
        this.k = k;
        this.dimension = dimension;
        this.centroids = Array(k).fill().map(() =>
            Array(dimension).fill().map(() => Math.random())
        );
        this.counts = new Array(k).fill(0);
        this.totalPoints = 0;
    }

    /**
     * Update centroids with new point
     */
    update(point) {
        this.totalPoints++;

        // Find nearest centroid
        const clusterIdx = this.findNearestCentroid(point);
        this.counts[clusterIdx]++;

        // Update centroid (incremental mean)
        const centroid = this.centroids[clusterIdx];
        const weight = 1 / this.counts[clusterIdx];

        for (let i = 0; i < this.dimension; i++) {
            centroid[i] = centroid[i] * (1 - weight) + point[i] * weight;
        }

        return clusterIdx;
    }

    /**
     * Find nearest centroid
     */
    findNearestCentroid(point) {
        let minDist = Infinity;
        let minIdx = 0;

        for (let i = 0; i < this.k; i++) {
            const dist = this.distance(point, this.centroids[i]);
            if (dist < minDist) {
                minDist = dist;
                minIdx = i;
            }
        }

        return minIdx;
    }

    /**
     * Predict cluster for a point
     */
    predict(point) {
        return this.findNearestCentroid(point);
    }

    /**
     * Calculate distance
     */
    distance(a, b) {
        let sum = 0;
        for (let i = 0; i < this.dimension; i++) {
            sum += Math.pow(a[i] - b[i], 2);
        }
        return Math.sqrt(sum);
    }

    /**
     * Get centroids
     */
    getCentroids() {
        return this.centroids.map(c => [...c]);
    }

    reset() {
        this.centroids = Array(this.k).fill().map(() =>
            Array(this.dimension).fill().map(() => Math.random())
        );
        this.counts.fill(0);
        this.totalPoints = 0;
    }
}

// ============================================
// Stream Sampling Utilities
// ============================================

/**
 * Bernoulli sampling
 */
export class BernoulliSampler {
    constructor(probability) {
        this.probability = probability;
        this.sample = [];
        this.totalCount = 0;
    }

    add(item) {
        this.totalCount++;
        if (Math.random() < this.probability) {
            this.sample.push(item);
        }
    }

    getSample() {
        return [...this.sample];
    }

    getStats() {
        return {
            sampleSize: this.sample.length,
            totalCount: this.totalCount,
            actualRate: this.sample.length / this.totalCount
        };
    }

    reset() {
        this.sample = [];
        this.totalCount = 0;
    }
}

/**
 * Systematic sampling
 */
export class SystematicSampler {
    constructor(k) {
        this.k = k; // Sample every kth element
        this.sample = [];
        this.count = 0;
        this.start = Math.floor(Math.random() * k);
    }

    add(item) {
        if (this.count % this.k === this.start) {
            this.sample.push(item);
        }
        this.count++;
    }

    getSample() {
        return [...this.sample];
    }

    reset() {
        this.sample = [];
        this.count = 0;
        this.start = Math.floor(Math.random() * this.k);
    }
}

// Export all classes
export default {
    // Reservoir Sampling
    ReservoirSampler,
    WeightedReservoirSampler,
    StratifiedReservoirSampler,

    // Streaming Statistics
    StreamingStats,
    EWMA,
    StreamingQuantiles,

    // Count-Distinct
    HyperLogLog,
    CountMinSketch,

    // Frequent Elements
    MisraGries,
    SpaceSaving,

    // Sliding Window
    SlidingWindowStats,
    SlidingWindowExtreme,
    SlidingWindowCounter,

    // Probabilistic
    BloomFilter,

    // Online Learning
    OnlineLinearRegression,
    OnlineKMeans,

    // Sampling
    BernoulliSampler,
    SystematicSampler
};