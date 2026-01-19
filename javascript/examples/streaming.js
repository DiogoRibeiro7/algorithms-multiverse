/**
 * Streaming Algorithms Examples
 * Demonstrates real-time data processing and online algorithms
 */

import * as stream from '../src/streaming.js';

console.log('=== STREAMING ALGORITHMS EXAMPLES ===\n');

// ============================================
// Example 1: Web Analytics - Real-time Statistics
// ============================================

console.log('--- WEB ANALYTICS: REAL-TIME PAGE LOAD MONITORING ---\n');

// Simulate page load times (in milliseconds)
const pageLoadSimulator = {
    generate: function() {
        // Normal distribution with occasional slow loads
        const normal = Math.random() < 0.95;
        if (normal) {
            return 200 + Math.random() * 800 + (Math.random() - 0.5) * 200;
        } else {
            return 2000 + Math.random() * 3000; // Slow loads
        }
    }
};

console.log('Monitoring page load times over 1000 requests...\n');

const stats = new stream.StreamingStats();
const ewma = new stream.EWMA(0.1); // 10% weight for new values
const quantiles = new stream.StreamingQuantiles([0.5, 0.75, 0.95, 0.99]);

// Simulate streaming data
for (let i = 0; i < 1000; i++) {
    const loadTime = pageLoadSimulator.generate();
    stats.add(loadTime);
    ewma.update(loadTime);
    quantiles.add(loadTime);

    // Report every 100 requests
    if ((i + 1) % 100 === 0) {
        const currentStats = stats.getStats();
        console.log(`After ${i + 1} requests:`);
        console.log(`  Mean: ${currentStats.mean.toFixed(2)}ms`);
        console.log(`  Std Dev: ${currentStats.stdDev.toFixed(2)}ms`);
        console.log(`  Min: ${currentStats.min.toFixed(2)}ms, Max: ${currentStats.max.toFixed(2)}ms`);
        console.log(`  EWMA: ${ewma.getValue().toFixed(2)}ms`);

        const q = quantiles.getQuantiles();
        console.log(`  Quantiles: 50%=${q[0.5]?.toFixed(2)}ms, 95%=${q[0.95]?.toFixed(2)}ms, 99%=${q[0.99]?.toFixed(2)}ms`);
        console.log('');
    }
}

// ============================================
// Example 2: Social Media - Unique User Counting
// ============================================

console.log('\n--- SOCIAL MEDIA: COUNTING UNIQUE USERS ---\n');

// Simulate user IDs visiting the platform
function generateUserId() {
    // Power law distribution (some users are very active)
    const userId = Math.floor(Math.pow(Math.random(), 2) * 10000);
    return `user_${userId}`;
}

console.log('Tracking unique users with HyperLogLog vs exact counting...\n');

const hyperloglog = new stream.HyperLogLog(14); // 14-bit precision
const exactSet = new Set();

// Simulate stream of user visits
const visits = 100000;
for (let i = 0; i < visits; i++) {
    const userId = generateUserId();
    hyperloglog.add(userId);
    exactSet.add(userId);

    // Report periodically
    if ((i + 1) % 20000 === 0) {
        const estimated = hyperloglog.cardinality();
        const exact = exactSet.size;
        const error = Math.abs(estimated - exact) / exact * 100;

        console.log(`After ${i + 1} visits:`);
        console.log(`  Exact unique users: ${exact}`);
        console.log(`  HyperLogLog estimate: ${estimated}`);
        console.log(`  Error: ${error.toFixed(2)}%`);
        console.log(`  Memory: Set=${(exact * 20 / 1024).toFixed(2)}KB, HLL=${(Math.pow(2, 14) / 1024).toFixed(2)}KB`);
        console.log('');
    }
}

// ============================================
// Example 3: Network Monitoring - Top Traffic Sources
// ============================================

console.log('\n--- NETWORK MONITORING: TOP TRAFFIC SOURCES ---\n');

// Simulate IP addresses with varying traffic patterns
function generateIP() {
    // Some IPs generate more traffic
    const heavyHitters = ['192.168.1.1', '10.0.0.1', '172.16.0.1', '192.168.2.1'];
    if (Math.random() < 0.3) {
        return heavyHitters[Math.floor(Math.random() * heavyHitters.length)];
    }
    return `${Math.floor(Math.random() * 256)}.${Math.floor(Math.random() * 256)}.` +
           `${Math.floor(Math.random() * 256)}.${Math.floor(Math.random() * 256)}`;
}

console.log('Tracking top IP addresses by request count...\n');

const spaceSaving = new stream.SpaceSaving(5); // Track top 5
const countMin = new stream.CountMinSketch(1000, 5);
const ipCounts = new Map(); // For verification

// Simulate traffic
for (let i = 0; i < 10000; i++) {
    const ip = generateIP();
    spaceSaving.add(ip);
    countMin.add(ip);

    // Track exact counts
    ipCounts.set(ip, (ipCounts.get(ip) || 0) + 1);
}

// Report top IPs
console.log('Space-Saving Algorithm Results:');
const topK = spaceSaving.getTopK();
for (const item of topK) {
    const exact = ipCounts.get(item.item) || 0;
    const cmEstimate = countMin.estimate(item.item);
    console.log(`  ${item.item}: SS=${item.count}, CM=${cmEstimate}, Exact=${exact}`);
}

// Show actual top 5
console.log('\nActual Top 5:');
const sortedIPs = Array.from(ipCounts.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5);
for (const [ip, count] of sortedIPs) {
    console.log(`  ${ip}: ${count} requests`);
}

// ============================================
// Example 4: Stock Trading - Sliding Window Analysis
// ============================================

console.log('\n\n--- STOCK TRADING: SLIDING WINDOW ANALYSIS ---\n');

// Simulate stock price ticks
function generateStockPrice(basePrice, volatility) {
    const change = (Math.random() - 0.5) * 2 * volatility;
    return basePrice * (1 + change);
}

console.log('Analyzing stock price movements with 100-tick window...\n');

const windowStats = new stream.SlidingWindowStats(100);
const windowMax = new stream.SlidingWindowExtreme(100, true);
const windowMin = new stream.SlidingWindowExtreme(100, false);

let basePrice = 100;
const prices = [];

// Simulate price stream
for (let i = 0; i < 500; i++) {
    const price = generateStockPrice(basePrice, 0.02);
    basePrice = price; // Random walk

    windowStats.add(price);
    windowMax.add(price, i);
    windowMin.add(price, i);
    prices.push(price);

    // Report periodically
    if ((i + 1) % 100 === 0) {
        const stats = windowStats.getStats();
        const max = windowMax.getExtreme();
        const min = windowMin.getExtreme();

        console.log(`Tick ${i + 1}:`);
        console.log(`  Current Price: $${price.toFixed(2)}`);
        console.log(`  Window Mean: $${stats.mean.toFixed(2)}`);
        console.log(`  Window Std Dev: $${stats.stdDev.toFixed(2)}`);
        console.log(`  Window Range: $${min.toFixed(2)} - $${max.toFixed(2)}`);
        console.log(`  Volatility: ${(stats.stdDev / stats.mean * 100).toFixed(2)}%`);
        console.log('');
    }
}

// ============================================
// Example 5: IoT Sensors - Anomaly Detection
// ============================================

console.log('\n--- IOT SENSORS: TEMPERATURE ANOMALY DETECTION ---\n');

// Simulate temperature readings
function generateTemperature(hour) {
    // Base temperature varies by hour (cooler at night)
    const baseTemp = 20 + 5 * Math.sin((hour - 6) * Math.PI / 12);

    // Normal variation
    const normalVariation = (Math.random() - 0.5) * 2;

    // Occasional anomalies
    const isAnomaly = Math.random() < 0.02;
    const anomaly = isAnomaly ? (Math.random() - 0.5) * 20 : 0;

    return baseTemp + normalVariation + anomaly;
}

console.log('Detecting temperature anomalies using EWMA...\n');

const tempEWMA = new stream.EWMA(0.2);
const tempStats = new stream.StreamingStats();
let anomalyCount = 0;

// Simulate 24 hours of readings (every minute)
for (let minute = 0; minute < 24 * 60; minute++) {
    const hour = minute / 60;
    const temperature = generateTemperature(hour);

    tempStats.add(temperature);
    const smoothed = tempEWMA.update(temperature);

    // Detect anomaly if temperature deviates significantly from EWMA
    const deviation = Math.abs(temperature - smoothed);
    const isAnomaly = deviation > 3; // 3 degrees threshold

    if (isAnomaly) {
        anomalyCount++;
        console.log(`Anomaly detected at ${Math.floor(hour)}:${(minute % 60).toString().padStart(2, '0')}`);
        console.log(`  Temperature: ${temperature.toFixed(2)}°C`);
        console.log(`  Expected (EWMA): ${smoothed.toFixed(2)}°C`);
        console.log(`  Deviation: ${deviation.toFixed(2)}°C`);
        console.log('');
    }

    // Hourly summary
    if (minute > 0 && minute % 60 === 0) {
        const stats = tempStats.getStats();
        console.log(`Hour ${Math.floor(hour)} summary:`);
        console.log(`  Mean temp: ${stats.mean.toFixed(2)}°C`);
        console.log(`  Anomalies this hour: ${anomalyCount}`);
        console.log('');
        anomalyCount = 0;
    }
}

// ============================================
// Example 6: Database Query Optimization
// ============================================

console.log('\n--- DATABASE: QUERY FREQUENCY TRACKING ---\n');

// Simulate SQL queries
const queryTemplates = [
    'SELECT * FROM users WHERE id = ?',
    'SELECT * FROM products WHERE category = ?',
    'UPDATE users SET last_login = NOW() WHERE id = ?',
    'SELECT COUNT(*) FROM orders WHERE user_id = ?',
    'INSERT INTO logs (message) VALUES (?)',
    'SELECT * FROM users JOIN orders ON users.id = orders.user_id',
    'DELETE FROM sessions WHERE expired < NOW()'
];

console.log('Tracking query patterns with Count-Min Sketch...\n');

const querySketch = new stream.CountMinSketch(2000, 7);
const frequentQueries = new stream.MisraGries(10);

// Simulate query stream
for (let i = 0; i < 5000; i++) {
    // Some queries are more frequent
    let query;
    if (Math.random() < 0.7) {
        // Frequent queries
        query = queryTemplates[Math.floor(Math.random() * 3)];
    } else {
        // All queries
        query = queryTemplates[Math.floor(Math.random() * queryTemplates.length)];
    }

    querySketch.add(query);
    frequentQueries.add(query);
}

// Report query statistics
console.log('Query frequency estimates:');
for (const template of queryTemplates) {
    const estimate = querySketch.estimate(template);
    console.log(`  ${template.substring(0, 40)}...`);
    console.log(`    Estimated count: ${estimate}`);
}

console.log('\nFrequent queries (Misra-Gries):');
const frequent = frequentQueries.getFrequentItems(300);
for (const item of frequent) {
    console.log(`  ${item.item.substring(0, 40)}...`);
    console.log(`    Count: ${item.estimatedCount}`);
}

// ============================================
// Example 7: Recommendation System Sampling
// ============================================

console.log('\n\n--- RECOMMENDATION SYSTEM: RESERVOIR SAMPLING ---\n');

// Simulate user interaction stream
function generateInteraction() {
    const actions = ['view', 'click', 'purchase', 'like', 'share'];
    const categories = ['electronics', 'books', 'clothing', 'food', 'sports'];

    return {
        userId: `user_${Math.floor(Math.random() * 1000)}`,
        itemId: `item_${Math.floor(Math.random() * 10000)}`,
        action: actions[Math.floor(Math.random() * actions.length)],
        category: categories[Math.floor(Math.random() * categories.length)],
        score: Math.random() * 5,
        timestamp: Date.now()
    };
}

console.log('Sampling user interactions for recommendation training...\n');

const generalSampler = new stream.ReservoirSampler(100);
const stratifiedSampler = new stream.StratifiedReservoirSampler(
    100,
    (item) => item.category
);
const weightedSampler = new stream.WeightedReservoirSampler(100);

// Simulate interaction stream
for (let i = 0; i < 10000; i++) {
    const interaction = generateInteraction();

    generalSampler.add(interaction);
    stratifiedSampler.add(interaction);

    // Weight by interaction importance (purchases > clicks > views)
    const weight = interaction.action === 'purchase' ? 10 :
                  interaction.action === 'click' ? 3 : 1;
    weightedSampler.add(interaction, weight);
}

// Analyze samples
console.log('General Reservoir Sample:');
const generalSample = generalSampler.getSample();
const generalActions = {};
for (const item of generalSample) {
    generalActions[item.action] = (generalActions[item.action] || 0) + 1;
}
console.log('  Action distribution:', generalActions);

console.log('\nStratified Sample (by category):');
const stratStats = stratifiedSampler.getStrataStats();
for (const [category, stats] of Object.entries(stratStats)) {
    console.log(`  ${category}: ${stats.sampleSize} samples (${(stats.proportion * 100).toFixed(1)}% of stream)`);
}

console.log('\nWeighted Sample (by importance):');
const weightedSample = weightedSampler.getSample();
const weightedActions = {};
for (const item of weightedSample) {
    weightedActions[item.action] = (weightedActions[item.action] || 0) + 1;
}
console.log('  Action distribution:', weightedActions);
console.log('  (Note: Weighted sampling favors purchases and clicks)');

// ============================================
// Example 8: Bloom Filter for Cache Management
// ============================================

console.log('\n\n--- CACHE MANAGEMENT: BLOOM FILTER ---\n');

console.log('Using Bloom filter to avoid unnecessary cache lookups...\n');

const bloomFilter = new stream.BloomFilter(10000, 0.01); // 1% false positive rate
const cache = new Map(); // Actual cache
let cacheHits = 0;
let cacheMisses = 0;
let bloomFalsePositives = 0;

// Add some items to cache
for (let i = 0; i < 1000; i++) {
    const key = `cached_item_${i}`;
    cache.set(key, `value_${i}`);
    bloomFilter.add(key);
}

// Simulate cache queries
for (let i = 0; i < 5000; i++) {
    // Mix of cached and non-cached items
    const key = `cached_item_${Math.floor(Math.random() * 2000)}`;

    if (bloomFilter.contains(key)) {
        // Bloom filter says it might be in cache
        if (cache.has(key)) {
            cacheHits++;
        } else {
            // False positive
            bloomFalsePositives++;
            cacheMisses++;
        }
    } else {
        // Bloom filter says definitely not in cache
        cacheMisses++;
        // We avoid the cache lookup entirely
    }
}

console.log('Cache query results:');
console.log(`  Total queries: ${cacheHits + cacheMisses}`);
console.log(`  Cache hits: ${cacheHits}`);
console.log(`  Cache misses: ${cacheMisses}`);
console.log(`  Bloom filter false positives: ${bloomFalsePositives}`);
console.log(`  False positive rate: ${(bloomFalsePositives / cacheMisses * 100).toFixed(2)}%`);
console.log(`  Estimated FP rate: ${(bloomFilter.getFalsePositiveRate() * 100).toFixed(2)}%`);

// ============================================
// Example 9: Online Machine Learning
// ============================================

console.log('\n\n--- ONLINE MACHINE LEARNING ---\n');

console.log('Training models on streaming data...\n');

// Online Linear Regression for prediction
const onlineRegressor = new stream.OnlineLinearRegression(2, 0.01);

// Online K-Means for clustering
const onlineKMeans = new stream.OnlineKMeans(3, 2);

// Generate streaming training data
console.log('Linear Regression: Predicting y = 2*x1 + 3*x2 + 1');
for (let i = 0; i < 1000; i++) {
    // Generate features
    const x1 = Math.random() * 10;
    const x2 = Math.random() * 10;
    const features = [x1, x2];

    // True target with noise
    const target = 2 * x1 + 3 * x2 + 1 + (Math.random() - 0.5) * 2;

    // Update model
    const prediction = onlineRegressor.update(features, target);

    // Report periodically
    if ((i + 1) % 200 === 0) {
        console.log(`  After ${i + 1} samples: MSE = ${onlineRegressor.getMSE().toFixed(4)}`);
    }
}

// Test the trained model
console.log('\nTesting regression model:');
const testCases = [[1, 1], [2, 3], [5, 2]];
for (const features of testCases) {
    const prediction = onlineRegressor.predict(features);
    const actual = 2 * features[0] + 3 * features[1] + 1;
    console.log(`  Features: [${features}], Predicted: ${prediction.toFixed(2)}, Actual: ${actual}`);
}

console.log('\n\nOnline K-Means: Clustering 2D points');
// Generate clustered data
for (let i = 0; i < 300; i++) {
    let point;
    const cluster = Math.floor(Math.random() * 3);

    if (cluster === 0) {
        point = [Math.random() * 2, Math.random() * 2];
    } else if (cluster === 1) {
        point = [5 + Math.random() * 2, Math.random() * 2];
    } else {
        point = [2.5 + Math.random() * 2, 5 + Math.random() * 2];
    }

    onlineKMeans.update(point);
}

console.log('Final cluster centroids:');
const centroids = onlineKMeans.getCentroids();
centroids.forEach((c, i) => {
    console.log(`  Cluster ${i}: [${c[0].toFixed(2)}, ${c[1].toFixed(2)}]`);
});

// ============================================
// Example 10: Rate Limiting with Sliding Window
// ============================================

console.log('\n\n--- API RATE LIMITING ---\n');

console.log('Monitoring API request rates with sliding window...\n');

const windowCounter = new stream.SlidingWindowCounter(60000, 1000); // 1-minute window, 1-second granularity

// Simulate API requests with varying rates
let currentTime = Date.now();
const startTime = currentTime;

// Burst of requests
for (let i = 0; i < 100; i++) {
    windowCounter.increment(1, currentTime);
}

console.log(`Initial burst: ${windowCounter.getCount(currentTime)} requests in window`);
console.log(`Rate: ${windowCounter.getRate(currentTime).toFixed(2)} req/s`);

// Simulate time passing with varying request rates
for (let second = 0; second < 120; second++) {
    currentTime = startTime + second * 1000;

    // Varying request patterns
    let requests;
    if (second < 30) {
        requests = 10; // High rate
    } else if (second < 60) {
        requests = 5; // Medium rate
    } else if (second < 90) {
        requests = 2; // Low rate
    } else {
        requests = 20; // Another burst
    }

    for (let i = 0; i < requests; i++) {
        windowCounter.increment(1, currentTime);
    }

    // Report every 30 seconds
    if (second > 0 && second % 30 === 0) {
        const count = windowCounter.getCount(currentTime);
        const rate = windowCounter.getRate(currentTime);

        console.log(`\nAt ${second} seconds:`);
        console.log(`  Requests in last minute: ${count}`);
        console.log(`  Current rate: ${rate.toFixed(2)} req/s`);

        // Check rate limit
        const rateLimit = 10; // 10 req/s limit
        if (rate > rateLimit) {
            console.log(`  ⚠️ RATE LIMIT EXCEEDED (limit: ${rateLimit} req/s)`);
        } else {
            console.log(`  ✓ Within rate limit`);
        }
    }
}

console.log('\n=== Streaming Algorithms Examples Completed ===');