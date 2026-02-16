/**
 * Test suite for Streaming Algorithms
 */

import * as stream from '../src/streaming.js';

console.log('=== STREAMING ALGORITHMS TESTS ===\n');

// ============================================
// Test Reservoir Sampling
// ============================================

console.log('Testing Reservoir Sampling...');

// Test basic reservoir sampling
const reservoir = new stream.ReservoirSampler(5);
for (let i = 0; i < 100; i++) {
    reservoir.add(i);
}
const sample = reservoir.getSample();
console.assert(sample.length === 5, 'Reservoir sample size incorrect');
console.assert(sample.every(x => x >= 0 && x < 100), 'Reservoir sample values out of range');

const stats = reservoir.getStats();
console.assert(stats.totalSeen === 100, 'Reservoir total count incorrect');
console.assert(stats.isFull === true, 'Reservoir should be full');

// Test weighted reservoir sampling
const weighted = new stream.WeightedReservoirSampler(3);
weighted.add('a', 1);
weighted.add('b', 10);
weighted.add('c', 1);
weighted.add('d', 10);
const weightedSample = weighted.getSample();
console.assert(weightedSample.length === 3, 'Weighted reservoir sample size incorrect');

// Test stratified reservoir sampling
const stratified = new stream.StratifiedReservoirSampler(10, x => x.type);
for (let i = 0; i < 50; i++) {
    stratified.add({ value: i, type: i % 3 === 0 ? 'A' : 'B' });
}
const stratSample = stratified.getSample();
console.assert(stratSample.length <= 10, 'Stratified sample size exceeds limit');

console.log('✓ Reservoir Sampling passed');

// ============================================
// Test Streaming Statistics
// ============================================

console.log('\nTesting Streaming Statistics...');

// Test online mean and variance
const stats2 = new stream.StreamingStats();
const values = [1, 2, 3, 4, 5];
values.forEach(v => stats2.add(v));

console.assert(Math.abs(stats2.getMean() - 3) < 0.001, 'Streaming mean incorrect');
console.assert(Math.abs(stats2.getVariance() - 2.5) < 0.001, 'Streaming variance incorrect');
console.assert(stats2.min === 1, 'Streaming min incorrect');
console.assert(stats2.max === 5, 'Streaming max incorrect');
console.assert(stats2.sum === 15, 'Streaming sum incorrect');

// Test EWMA
const ewma = new stream.EWMA(0.5);
console.assert(ewma.update(10) === 10, 'EWMA first value incorrect');
console.assert(ewma.update(20) === 15, 'EWMA second value incorrect');
console.assert(ewma.getValue() === 15, 'EWMA getValue incorrect');

// Test streaming quantiles
const quantiles = new stream.StreamingQuantiles([0.5]);
for (let i = 1; i <= 100; i++) {
    quantiles.add(i);
}
const q = quantiles.getQuantiles();
console.assert(q[0.5] !== undefined, 'Streaming quantile not computed');

console.log('✓ Streaming Statistics passed');

// ============================================
// Test Count-Distinct Algorithms
// ============================================

console.log('\nTesting Count-Distinct Algorithms...');

// Test HyperLogLog
const hll = new stream.HyperLogLog(14);
const uniqueItems = new Set();
for (let i = 0; i < 1000; i++) {
    const item = `item_${Math.floor(Math.random() * 500)}`;
    hll.add(item);
    uniqueItems.add(item);
}

const estimate = hll.cardinality();
const actual = uniqueItems.size;
const error = Math.abs(estimate - actual) / actual;
console.assert(error < 0.1, `HyperLogLog error too high: ${error}`);

// Test HyperLogLog merge
const hll2 = new stream.HyperLogLog(14);
for (let i = 0; i < 100; i++) {
    hll2.add(`other_${i}`);
}
hll.merge(hll2);
console.assert(hll.cardinality() > estimate, 'HyperLogLog merge failed');

// Test Count-Min Sketch
const cms = new stream.CountMinSketch(100, 5);
cms.add('apple', 5);
cms.add('banana', 3);
cms.add('apple', 2);

console.assert(cms.estimate('apple') >= 7, 'Count-Min Sketch estimate too low');
console.assert(cms.estimate('banana') >= 3, 'Count-Min Sketch estimate too low');
console.assert(cms.estimate('unknown') >= 0, 'Count-Min Sketch estimate negative');

console.log('✓ Count-Distinct Algorithms passed');

// ============================================
// Test Frequent Elements
// ============================================

console.log('\nTesting Frequent Elements...');

// Test Misra-Gries
const mg = new stream.MisraGries(3);
for (let i = 0; i < 100; i++) {
    if (i % 2 === 0) mg.add('even');
    if (i % 3 === 0) mg.add('div3');
    if (i % 5 === 0) mg.add('div5');
}

const frequent = mg.getFrequentItems(20);
console.assert(frequent.length > 0, 'Misra-Gries found no frequent items');
console.assert(frequent.some(x => x.item === 'even'), 'Misra-Gries missed frequent item');

// Test Space-Saving
const ss = new stream.SpaceSaving(3);
for (let i = 0; i < 100; i++) {
    ss.add(`item_${i % 10}`);
}

const topK = ss.getTopK();
console.assert(topK.length === 3, 'Space-Saving topK size incorrect');
console.assert(topK[0].count >= topK[1].count, 'Space-Saving topK not sorted');
console.assert(topK[1].count >= topK[2].count, 'Space-Saving topK not sorted');

console.log('✓ Frequent Elements passed');

// ============================================
// Test Sliding Window Algorithms
// ============================================

console.log('\nTesting Sliding Window Algorithms...');

// Test sliding window statistics
const windowStats = new stream.SlidingWindowStats(3);
windowStats.add(1);
windowStats.add(2);
windowStats.add(3);
let wStats = windowStats.getStats();
console.assert(wStats.mean === 2, 'Window stats mean incorrect');

windowStats.add(4);
wStats = windowStats.getStats();
console.assert(wStats.mean === 3, 'Window stats mean after slide incorrect');
console.assert(wStats.count === 3, 'Window size incorrect after slide');

// Test sliding window extreme
const maxWindow = new stream.SlidingWindowExtreme(3, true);
maxWindow.add(1, 1);
maxWindow.add(3, 2);
maxWindow.add(2, 3);
console.assert(maxWindow.getExtreme() === 3, 'Window max incorrect');

maxWindow.add(4, 4);
console.assert(maxWindow.getExtreme() === 4, 'Window max after slide incorrect');

// Test sliding window counter
const counter = new stream.SlidingWindowCounter(1000, 100);
const now = Date.now();
counter.increment(5, now);
counter.increment(3, now + 100);

console.assert(counter.getCount(now + 200) === 8, 'Window counter sum incorrect');
console.assert(counter.getCount(now + 1100) === 3, 'Window counter after slide incorrect');

console.log('✓ Sliding Window Algorithms passed');

// ============================================
// Test Bloom Filter
// ============================================

console.log('\nTesting Bloom Filter...');

const bloom = new stream.BloomFilter(100, 0.01);
bloom.add('apple');
bloom.add('banana');
bloom.add('cherry');

console.assert(bloom.contains('apple') === true, 'Bloom filter false negative');
console.assert(bloom.contains('banana') === true, 'Bloom filter false negative');
console.assert(bloom.contains('cherry') === true, 'Bloom filter false negative');

// Test false positive rate
let falsePositives = 0;
for (let i = 0; i < 1000; i++) {
    if (bloom.contains(`nonexistent_${i}`)) {
        falsePositives++;
    }
}
const fpRate = falsePositives / 1000;
console.assert(fpRate < 0.05, `Bloom filter FP rate too high: ${fpRate}`);

console.log('✓ Bloom Filter passed');

// ============================================
// Test Online Learning
// ============================================

console.log('\nTesting Online Learning...');

// Test online linear regression
const olr = new stream.OnlineLinearRegression(2, 0.1);
for (let i = 0; i < 100; i++) {
    const x1 = Math.random();
    const x2 = Math.random();
    const y = 2 * x1 + 3 * x2 + 1; // True function
    olr.update([x1, x2], y);
}

const prediction = olr.predict([1, 1]);
console.assert(Math.abs(prediction - 6) < 1, 'Online regression prediction inaccurate');

// Test online K-Means
const okm = new stream.OnlineKMeans(2, 2);
// Add points from two clusters
for (let i = 0; i < 50; i++) {
    okm.update([Math.random(), Math.random()]); // Cluster 1 near (0.5, 0.5)
    okm.update([5 + Math.random(), 5 + Math.random()]); // Cluster 2 near (5.5, 5.5)
}

const centroids = okm.getCentroids();
console.assert(centroids.length === 2, 'Online K-Means wrong number of centroids');

// One centroid should be near origin, other near (5, 5)
const distances = centroids.map(c => Math.sqrt(c[0] * c[0] + c[1] * c[1]));
console.assert(Math.min(...distances) < 2, 'Online K-Means centroid misplaced');
console.assert(Math.max(...distances) > 5, 'Online K-Means centroid misplaced');

console.log('✓ Online Learning passed');

// ============================================
// Test Sampling Utilities
// ============================================

console.log('\nTesting Sampling Utilities...');

// Test Bernoulli sampling
const bernoulli = new stream.BernoulliSampler(0.1);
for (let i = 0; i < 1000; i++) {
    bernoulli.add(i);
}
const bStats = bernoulli.getStats();
console.assert(bStats.totalCount === 1000, 'Bernoulli total count incorrect');
console.assert(Math.abs(bStats.actualRate - 0.1) < 0.05, 'Bernoulli sampling rate off');

// Test systematic sampling
const systematic = new stream.SystematicSampler(10);
for (let i = 0; i < 100; i++) {
    systematic.add(i);
}
const sysSample = systematic.getSample();
console.assert(sysSample.length === 10, 'Systematic sampling count incorrect');

console.log('✓ Sampling Utilities passed');

// ============================================
// Test Edge Cases
// ============================================

console.log('\nTesting Edge Cases...');

// Empty reservoir
const emptyReservoir = new stream.ReservoirSampler(5);
console.assert(emptyReservoir.getSample().length === 0, 'Empty reservoir should return empty array');

// Reset functionality
const resetTest = new stream.StreamingStats();
resetTest.add(5);
resetTest.reset();
console.assert(resetTest.count === 0, 'Reset failed');
console.assert(resetTest.getMean() === 0, 'Reset failed to clear mean');

// Single element
const singleElem = new stream.EWMA(0.5);
singleElem.update(42);
console.assert(singleElem.getValue() === 42, 'Single element EWMA failed');

// Overflow protection
const overflow = new stream.HyperLogLog(14);
for (let i = 0; i < 100000; i++) {
    overflow.add(`item_${i}`);
}
const bigEstimate = overflow.cardinality();
console.assert(bigEstimate > 50000, 'HyperLogLog failed on large cardinality');

console.log('✓ Edge cases passed');

// ============================================
// Test Memory Efficiency
// ============================================

console.log('\nTesting Memory Efficiency...');

// Ensure bounded memory usage
const memTest = new stream.ReservoirSampler(100);
for (let i = 0; i < 1000000; i++) {
    memTest.add(i);
}
console.assert(memTest.getSample().length === 100, 'Reservoir exceeded size limit');

const slidingMemTest = new stream.SlidingWindowStats(100);
for (let i = 0; i < 1000; i++) {
    slidingMemTest.add(i);
}
console.assert(slidingMemTest.window.length === 100, 'Sliding window exceeded size limit');

console.log('✓ Memory efficiency passed');

// ============================================
// Test Accuracy
// ============================================

console.log('\nTesting Algorithm Accuracy...');

// Test Welford's algorithm accuracy
const welford = new stream.StreamingStats();
const testData = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0];
testData.forEach(v => welford.add(v));

const expectedMean = 5.0;
const expectedVar = 4.57142857;
console.assert(Math.abs(welford.getMean() - expectedMean) < 0.001, 'Welford mean inaccurate');
console.assert(Math.abs(welford.getVariance() - expectedVar) < 0.01, 'Welford variance inaccurate');

// Test reservoir sampling uniformity (statistical test)
const uniformTest = new stream.ReservoirSampler(10);
const counts = new Array(100).fill(0);

// Run multiple trials
for (let trial = 0; trial < 1000; trial++) {
    uniformTest.reset();
    for (let i = 0; i < 100; i++) {
        uniformTest.add(i);
    }
    const sample = uniformTest.getSample();
    sample.forEach(x => counts[x]++);
}

// Each element should appear roughly 100 times (10% of trials)
const avgCount = counts.reduce((a, b) => a + b, 0) / counts.length;
const variance = counts.reduce((sum, c) => sum + Math.pow(c - avgCount, 2), 0) / counts.length;
console.assert(Math.abs(avgCount - 100) < 10, 'Reservoir sampling not uniform');
console.assert(variance < 500, 'Reservoir sampling variance too high');

console.log('✓ Algorithm accuracy passed');

console.log('\n=== All Streaming tests completed successfully ===');