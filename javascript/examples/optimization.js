/**
 * Optimization Examples
 * Demonstrates various optimization algorithms for different problems
 */

import * as opt from '../src/optimization.js';

console.log('=== OPTIMIZATION ALGORITHMS EXAMPLES ===\n');

// ============================================
// Example 1: Function Optimization Benchmark
// ============================================

console.log('--- BENCHMARK: STANDARD TEST FUNCTIONS ---\n');

// Test on Rosenbrock function (2D)
console.log('Optimizing Rosenbrock Function (2D):');
console.log('Global minimum: f(1, 1) = 0\n');

const rosenbrockBounds = opt.createBounds(2, -5, 10);

// Test different optimizers
const optimizers = [
    ['Genetic Algorithm', opt.GeneticAlgorithm, { populationSize: 50, generations: 100 }],
    ['Simulated Annealing', opt.SimulatedAnnealing, { maxIterations: 1000, initialTemp: 100 }],
    ['Particle Swarm', opt.ParticleSwarm, { swarmSize: 30, maxIterations: 100 }],
    ['Differential Evolution', opt.DifferentialEvolution, { populationSize: 30, generations: 100 }],
    ['Gradient Descent (Adam)', opt.GradientDescent, { method: 'adam', learningRate: 0.1, maxIterations: 500 }],
];

for (const [name, OptimizerClass, options] of optimizers) {
    const optimizer = new OptimizerClass(
        opt.testFunctions.rosenbrock.fn,
        rosenbrockBounds,
        { ...options, verbose: false }
    );

    const result = optimizer.optimize();
    console.log(`${name}:`);
    console.log(`  Solution: [${result.solution.map(x => x.toFixed(4)).join(', ')}]`);
    console.log(`  Value: ${result.value.toFixed(6)}`);
    console.log(`  Error: ${Math.sqrt(result.solution.reduce((sum, x, i) => sum + Math.pow(x - (i === 0 ? 1 : 1), 2), 0)).toFixed(6)}`);
}

// Test on Rastrigin function (multimodal, 5D)
console.log('\n\nOptimizing Rastrigin Function (5D - Highly Multimodal):');
console.log('Global minimum: f(0, 0, 0, 0, 0) = 0\n');

const rastriginBounds = opt.createBounds(5, -5.12, 5.12);

const rastriginOptimizers = [
    ['Genetic Algorithm', opt.GeneticAlgorithm, { populationSize: 100, generations: 200 }],
    ['Particle Swarm', opt.ParticleSwarm, { swarmSize: 50, maxIterations: 150 }],
    ['Differential Evolution', opt.DifferentialEvolution, { populationSize: 50, generations: 150 }],
];

for (const [name, OptimizerClass, options] of rastriginOptimizers) {
    const optimizer = new OptimizerClass(
        opt.testFunctions.rastrigin.fn,
        rastriginBounds,
        { ...options, verbose: false }
    );

    const result = optimizer.optimize();
    console.log(`${name}:`);
    console.log(`  Solution: [${result.solution.map(x => x.toFixed(4)).join(', ')}]`);
    console.log(`  Value: ${result.value.toFixed(6)}`);
    console.log(`  Distance from optimum: ${Math.sqrt(result.solution.reduce((sum, x) => sum + x * x, 0)).toFixed(6)}`);
}

// ============================================
// Example 2: Engineering Design Optimization
// ============================================

console.log('\n\n--- ENGINEERING: PRESSURE VESSEL DESIGN ---\n');

console.log('Minimize cost of cylindrical pressure vessel');
console.log('Variables: [thickness_shell, thickness_head, radius, length]');
console.log('Subject to stress and volume constraints\n');

// Pressure vessel design problem
function pressureVesselCost(x) {
    const [Ts, Th, R, L] = x;

    // Cost function
    const cost = 0.6224 * Ts * R * L + 1.7781 * Th * R * R +
                3.1661 * Ts * Ts * L + 19.84 * Ts * Ts * R;

    // Penalty for constraint violations
    let penalty = 0;

    // Constraints
    const g1 = -Ts + 0.0193 * R; // <= 0
    const g2 = -Th + 0.00954 * R; // <= 0
    const g3 = -Math.PI * R * R * L - (4/3) * Math.PI * R * R * R + 1296000; // <= 0
    const g4 = L - 240; // <= 0

    // Apply penalties
    if (g1 > 0) penalty += 1000000 * g1 * g1;
    if (g2 > 0) penalty += 1000000 * g2 * g2;
    if (g3 > 0) penalty += 1000000 * g3 * g3;
    if (g4 > 0) penalty += 1000000 * g4 * g4;

    return cost + penalty;
}

const vesselBounds = [
    [0.0625, 6.1875],  // Thickness of shell (inches * 0.0625)
    [0.0625, 6.1875],  // Thickness of head (inches * 0.0625)
    [10, 200],         // Inner radius
    [10, 200]          // Length
];

console.log('Optimizing with Differential Evolution...');
const vesselOptimizer = new opt.DifferentialEvolution(
    pressureVesselCost,
    vesselBounds,
    { populationSize: 50, generations: 200, verbose: false }
);

const vesselResult = vesselOptimizer.optimize();
console.log(`Optimal design found:`);
console.log(`  Shell thickness: ${vesselResult.solution[0].toFixed(4)} inches`);
console.log(`  Head thickness: ${vesselResult.solution[1].toFixed(4)} inches`);
console.log(`  Radius: ${vesselResult.solution[2].toFixed(2)} inches`);
console.log(`  Length: ${vesselResult.solution[3].toFixed(2)} inches`);
console.log(`  Minimum cost: $${vesselResult.value.toFixed(2)}`);

// ============================================
// Example 3: Portfolio Optimization
// ============================================

console.log('\n\n--- FINANCE: PORTFOLIO OPTIMIZATION ---\n');

console.log('Optimize portfolio allocation for maximum Sharpe ratio');
console.log('Assets: Tech Stock, Healthcare Stock, Bonds, Real Estate, Commodities\n');

// Historical returns and risks (mock data)
const assetReturns = [0.15, 0.12, 0.05, 0.08, 0.10]; // Expected annual returns
const assetRisks = [0.25, 0.20, 0.08, 0.15, 0.22]; // Standard deviations
const riskFreeRate = 0.02;

// Correlation matrix (simplified)
const correlations = [
    [1.0, 0.6, -0.2, 0.3, 0.4],
    [0.6, 1.0, -0.1, 0.4, 0.3],
    [-0.2, -0.1, 1.0, 0.1, -0.2],
    [0.3, 0.4, 0.1, 1.0, 0.5],
    [0.4, 0.3, -0.2, 0.5, 1.0]
];

// Portfolio optimization (maximize Sharpe ratio)
function portfolioSharpe(weights) {
    // Ensure weights sum to 1
    const sum = weights.reduce((s, w) => s + Math.abs(w), 0);
    const normalizedWeights = weights.map(w => Math.abs(w) / sum);

    // Calculate expected return
    let expectedReturn = 0;
    for (let i = 0; i < normalizedWeights.length; i++) {
        expectedReturn += normalizedWeights[i] * assetReturns[i];
    }

    // Calculate portfolio variance
    let variance = 0;
    for (let i = 0; i < normalizedWeights.length; i++) {
        for (let j = 0; j < normalizedWeights.length; j++) {
            variance += normalizedWeights[i] * normalizedWeights[j] *
                       assetRisks[i] * assetRisks[j] * correlations[i][j];
        }
    }

    const stdDev = Math.sqrt(variance);

    // Sharpe ratio (negative because we minimize)
    const sharpe = -(expectedReturn - riskFreeRate) / stdDev;

    // Add penalty for extreme allocations
    let penalty = 0;
    for (const w of normalizedWeights) {
        if (w > 0.4) penalty += 10 * (w - 0.4) * (w - 0.4); // Penalize > 40% in single asset
        if (w < 0.05) penalty += 5 * (0.05 - w) * (0.05 - w); // Penalize < 5% allocations
    }

    return sharpe + penalty;
}

const portfolioBounds = opt.createBounds(5, 0, 1);

console.log('Optimizing portfolio with Particle Swarm...');
const portfolioOptimizer = new opt.ParticleSwarm(
    portfolioSharpe,
    portfolioBounds,
    { swarmSize: 50, maxIterations: 200, verbose: false }
);

const portfolioResult = portfolioOptimizer.optimize();

// Normalize weights
const finalWeights = portfolioResult.solution.map(w => Math.abs(w));
const totalWeight = finalWeights.reduce((sum, w) => sum + w, 0);
const normalizedWeights = finalWeights.map(w => w / totalWeight);

console.log('Optimal portfolio allocation:');
const assetNames = ['Tech Stock', 'Healthcare', 'Bonds', 'Real Estate', 'Commodities'];
normalizedWeights.forEach((w, i) => {
    console.log(`  ${assetNames[i]}: ${(w * 100).toFixed(1)}%`);
});

// Calculate final metrics
let finalReturn = 0;
let finalVariance = 0;
for (let i = 0; i < 5; i++) {
    finalReturn += normalizedWeights[i] * assetReturns[i];
    for (let j = 0; j < 5; j++) {
        finalVariance += normalizedWeights[i] * normalizedWeights[j] *
                        assetRisks[i] * assetRisks[j] * correlations[i][j];
    }
}

console.log(`\nPortfolio metrics:`);
console.log(`  Expected return: ${(finalReturn * 100).toFixed(2)}%`);
console.log(`  Risk (std dev): ${(Math.sqrt(finalVariance) * 100).toFixed(2)}%`);
console.log(`  Sharpe ratio: ${((finalReturn - riskFreeRate) / Math.sqrt(finalVariance)).toFixed(3)}`);

// ============================================
// Example 4: Neural Network Weight Optimization
// ============================================

console.log('\n\n--- MACHINE LEARNING: NEURAL NETWORK TRAINING ---\n');

console.log('Train a simple neural network for XOR problem');
console.log('Using optimization instead of backpropagation\n');

// XOR dataset
const xorInputs = [[0, 0], [0, 1], [1, 0], [1, 1]];
const xorOutputs = [0, 1, 1, 0];

// Simple 2-2-1 neural network
function sigmoid(x) {
    return 1 / (1 + Math.exp(-x));
}

function neuralNetworkLoss(weights) {
    // Unpack weights: 2*2 (input->hidden) + 2 (hidden bias) + 2*1 (hidden->output) + 1 (output bias)
    const w1 = [[weights[0], weights[1]], [weights[2], weights[3]]]; // 2x2
    const b1 = [weights[4], weights[5]]; // 2
    const w2 = [[weights[6]], [weights[7]]]; // 2x1
    const b2 = weights[8]; // 1

    let totalLoss = 0;

    for (let i = 0; i < xorInputs.length; i++) {
        const input = xorInputs[i];
        const target = xorOutputs[i];

        // Forward pass
        // Hidden layer
        const hidden = [];
        for (let j = 0; j < 2; j++) {
            let sum = b1[j];
            for (let k = 0; k < 2; k++) {
                sum += input[k] * w1[k][j];
            }
            hidden.push(sigmoid(sum));
        }

        // Output layer
        let output = b2;
        for (let j = 0; j < 2; j++) {
            output += hidden[j] * w2[j][0];
        }
        output = sigmoid(output);

        // Loss (MSE)
        totalLoss += Math.pow(output - target, 2);
    }

    return totalLoss / xorInputs.length;
}

const nnBounds = opt.createBounds(9, -5, 5);

console.log('Training neural network with Genetic Algorithm...');
const nnOptimizer = new opt.GeneticAlgorithm(
    neuralNetworkLoss,
    nnBounds,
    {
        populationSize: 100,
        generations: 200,
        mutationRate: 0.1,
        verbose: false
    }
);

const nnResult = nnOptimizer.optimize();
console.log(`Training loss: ${nnResult.value.toFixed(6)}`);

// Test the trained network
console.log('\nTesting trained network:');
const trainedWeights = nnResult.solution;
const w1 = [[trainedWeights[0], trainedWeights[1]], [trainedWeights[2], trainedWeights[3]]];
const b1 = [trainedWeights[4], trainedWeights[5]];
const w2 = [[trainedWeights[6]], [trainedWeights[7]]];
const b2 = trainedWeights[8];

for (let i = 0; i < xorInputs.length; i++) {
    const input = xorInputs[i];

    // Forward pass
    const hidden = [];
    for (let j = 0; j < 2; j++) {
        let sum = b1[j];
        for (let k = 0; k < 2; k++) {
            sum += input[k] * w1[k][j];
        }
        hidden.push(sigmoid(sum));
    }

    let output = b2;
    for (let j = 0; j < 2; j++) {
        output += hidden[j] * w2[j][0];
    }
    output = sigmoid(output);

    console.log(`  Input: [${input}] → Output: ${output.toFixed(4)} (Target: ${xorOutputs[i]})`);
}

// ============================================
// Example 5: Traveling Salesman Problem (TSP)
// ============================================

console.log('\n\n--- COMBINATORIAL: TRAVELING SALESMAN PROBLEM ---\n');

console.log('Find shortest tour visiting all cities exactly once\n');

// Generate random cities
const nCities = 10;
const cities = [];
for (let i = 0; i < nCities; i++) {
    cities.push({
        x: Math.random() * 100,
        y: Math.random() * 100
    });
}

// Calculate distance matrix
const distances = [];
for (let i = 0; i < nCities; i++) {
    distances[i] = [];
    for (let j = 0; j < nCities; j++) {
        const dx = cities[i].x - cities[j].x;
        const dy = cities[i].y - cities[j].y;
        distances[i][j] = Math.sqrt(dx * dx + dy * dy);
    }
}

// TSP objective function (continuous relaxation)
function tspDistance(solution) {
    // Convert continuous values to tour order using sorting
    const indexed = solution.map((val, idx) => ({ val, idx }));
    indexed.sort((a, b) => a.val - b.val);
    const tour = indexed.map(item => item.idx);

    // Calculate tour distance
    let totalDistance = 0;
    for (let i = 0; i < tour.length; i++) {
        const from = tour[i];
        const to = tour[(i + 1) % tour.length];
        totalDistance += distances[from][to];
    }

    return totalDistance;
}

const tspBounds = opt.createBounds(nCities, 0, 1);

console.log(`Solving TSP for ${nCities} cities...`);
const tspOptimizer = new opt.GeneticAlgorithm(
    tspDistance,
    tspBounds,
    {
        populationSize: 100,
        generations: 300,
        crossoverRate: 0.9,
        mutationRate: 0.2,
        verbose: false
    }
);

const tspResult = tspOptimizer.optimize();

// Convert solution to tour
const indexed = tspResult.solution.map((val, idx) => ({ val, idx }));
indexed.sort((a, b) => a.val - b.val);
const tour = indexed.map(item => item.idx);

console.log(`Best tour found: [${tour.join(' → ')}]`);
console.log(`Total distance: ${tspResult.value.toFixed(2)}`);

// ============================================
// Example 6: Hyperparameter Tuning
// ============================================

console.log('\n\n--- HYPERPARAMETER OPTIMIZATION ---\n');

console.log('Optimize SVM hyperparameters for classification\n');

// Mock SVM cross-validation score function
function svmCrossValidation(params) {
    const [C, gamma, kernelParam] = params;

    // Simulate cross-validation score based on hyperparameters
    // In practice, this would train and evaluate an actual SVM
    const baseScore = 0.85;

    // C penalty (regularization)
    const cEffect = 0.1 * Math.exp(-Math.pow(Math.log10(C), 2));

    // Gamma effect (RBF kernel width)
    const gammaEffect = 0.1 * Math.exp(-Math.pow(Math.log10(gamma) + 3, 2));

    // Kernel parameter effect
    const kernelEffect = 0.05 * Math.sin(kernelParam * Math.PI);

    // Add some noise to simulate variance in CV scores
    const noise = (Math.random() - 0.5) * 0.02;

    // Return negative score (we minimize)
    return -(baseScore + cEffect + gammaEffect + kernelEffect + noise);
}

const svmBounds = [
    [0.001, 1000],  // C: regularization parameter
    [0.0001, 10],   // gamma: RBF kernel coefficient
    [0, 1]          // kernel mixing parameter
];

console.log('Optimizing SVM hyperparameters with Simulated Annealing...');
const svmOptimizer = new opt.SimulatedAnnealing(
    svmCrossValidation,
    svmBounds,
    {
        maxIterations: 500,
        initialTemp: 10,
        coolingRate: 0.95,
        verbose: false
    }
);

const svmResult = svmOptimizer.optimize();
console.log('Best hyperparameters found:');
console.log(`  C (regularization): ${svmResult.solution[0].toFixed(4)}`);
console.log(`  gamma (RBF width): ${svmResult.solution[1].toFixed(6)}`);
console.log(`  kernel parameter: ${svmResult.solution[2].toFixed(4)}`);
console.log(`  Cross-validation score: ${(-svmResult.value * 100).toFixed(2)}%`);

// ============================================
// Example 7: Algorithm Comparison
// ============================================

console.log('\n\n--- ALGORITHM COMPARISON ---\n');

console.log('Comparing optimizer performance on Ackley function (5D)\n');

const ackleyBounds = opt.createBounds(5, -32.768, 32.768);

const algorithms = [
    ['Genetic Algorithm', opt.GeneticAlgorithm, { populationSize: 50, generations: 100 }],
    ['Simulated Annealing', opt.SimulatedAnnealing, { maxIterations: 2000 }],
    ['Particle Swarm', opt.ParticleSwarm, { swarmSize: 30, maxIterations: 100 }],
    ['Differential Evolution', opt.DifferentialEvolution, { populationSize: 30, generations: 100 }],
    ['Hill Climbing (5 restarts)', opt.HillClimbing, { nRestarts: 5, maxIterations: 200 }],
    ['Tabu Search', opt.TabuSearch, { maxIterations: 500, tabuTenure: 20 }],
    ['Ant Colony', opt.AntColonyOptimization, { nAnts: 20, nIterations: 100 }]
];

console.log('Running 5 trials for each algorithm...\n');
const results = opt.compareOptimizers(algorithms, opt.testFunctions.ackley.fn, ackleyBounds, 5);

console.log('Results (global minimum = 0):');
console.log('Algorithm                    | Best    | Worst   | Mean    | Std Dev');
console.log('----------------------------|---------|---------|---------|--------');

for (const [name] of algorithms) {
    const r = results[name];
    const namePadded = name.padEnd(27);
    console.log(`${namePadded} | ${r.best.toFixed(4).padStart(7)} | ${r.worst.toFixed(4).padStart(7)} | ${r.mean.toFixed(4).padStart(7)} | ${r.std.toFixed(4).padStart(6)}`);
}

// Find best performer
let bestAlgorithm = '';
let bestMean = Infinity;
for (const [name] of algorithms) {
    if (results[name].mean < bestMean) {
        bestMean = results[name].mean;
        bestAlgorithm = name;
    }
}

console.log(`\nBest average performance: ${bestAlgorithm}`);

console.log('\n=== Optimization Examples Completed ===');