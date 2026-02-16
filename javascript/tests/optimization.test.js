/**
 * Test suite for Optimization algorithms
 */

import * as opt from '../src/optimization.js';

console.log('=== OPTIMIZATION ALGORITHMS TESTS ===\n');

// Test tolerance for optimization results
const TOLERANCE = 0.1;

// Simple test function for quick validation
function simpleQuadratic(x) {
    // f(x) = sum((xi - 2)^2), minimum at x = [2, 2, ...]
    return x.reduce((sum, xi) => sum + Math.pow(xi - 2, 2), 0);
}

// Test 1D function
function parabola(x) {
    return Math.pow(x[0] - 3, 2) + 1;
}

// ============================================
// Test Test Functions
// ============================================

console.log('Testing benchmark functions...');

// Test sphere function
const sphereResult = opt.testFunctions.sphere.fn([0, 0, 0]);
console.assert(Math.abs(sphereResult) < 1e-10, 'Sphere function at origin failed');
console.assert(opt.testFunctions.sphere.fn([1, 1, 1]) === 3, 'Sphere function failed');
console.log('✓ Sphere function passed');

// Test Rosenbrock function
const rosenResult = opt.testFunctions.rosenbrock.fn([1, 1]);
console.assert(Math.abs(rosenResult) < 1e-10, 'Rosenbrock at optimum failed');
console.log('✓ Rosenbrock function passed');

// Test Rastrigin function
const rastResult = opt.testFunctions.rastrigin.fn([0, 0]);
console.assert(Math.abs(rastResult) < 1e-10, 'Rastrigin at origin failed');
console.log('✓ Rastrigin function passed');

// ============================================
// Test Base Optimizer Class
// ============================================

console.log('\nTesting base optimizer functionality...');

const testOptimizer = new opt.Optimizer(
    simpleQuadratic,
    [[0, 5], [0, 5]],
    { minimize: true }
);

// Test bounds checking
console.assert(testOptimizer.isWithinBounds([2, 3]) === true, 'Within bounds check failed');
console.assert(testOptimizer.isWithinBounds([-1, 3]) === false, 'Out of bounds check failed');
console.assert(testOptimizer.isWithinBounds([3, 6]) === false, 'Out of bounds check failed');

// Test bounds clipping
const clipped = testOptimizer.clipToBounds([-1, 6]);
console.assert(clipped[0] === 0 && clipped[1] === 5, 'Bounds clipping failed');

// Test random solution generation
const randomSol = testOptimizer.randomSolution();
console.assert(testOptimizer.isWithinBounds(randomSol), 'Random solution out of bounds');

console.log('✓ Base optimizer passed');

// ============================================
// Test Genetic Algorithm
// ============================================

console.log('\nTesting Genetic Algorithm...');

const ga = new opt.GeneticAlgorithm(
    simpleQuadratic,
    [[0, 5], [0, 5]],
    {
        populationSize: 20,
        generations: 50,
        verbose: false
    }
);

const gaResult = ga.optimize();
console.assert(gaResult.solution !== null, 'GA returned null solution');
console.assert(gaResult.value !== null, 'GA returned null value');
console.assert(Math.abs(gaResult.solution[0] - 2) < TOLERANCE, 'GA solution x[0] incorrect');
console.assert(Math.abs(gaResult.solution[1] - 2) < TOLERANCE, 'GA solution x[1] incorrect');
console.assert(gaResult.value < TOLERANCE, 'GA objective value too high');
console.assert(gaResult.history.length > 0, 'GA history not recorded');

console.log(`✓ Genetic Algorithm passed (found minimum: ${gaResult.value.toFixed(6)})`);

// ============================================
// Test Simulated Annealing
// ============================================

console.log('\nTesting Simulated Annealing...');

const sa = new opt.SimulatedAnnealing(
    simpleQuadratic,
    [[0, 5], [0, 5]],
    {
        maxIterations: 500,
        initialTemp: 10,
        verbose: false
    }
);

const saResult = sa.optimize();
console.assert(saResult.solution !== null, 'SA returned null solution');
console.assert(Math.abs(saResult.solution[0] - 2) < TOLERANCE * 2, 'SA solution x[0] incorrect');
console.assert(Math.abs(saResult.solution[1] - 2) < TOLERANCE * 2, 'SA solution x[1] incorrect');
console.assert(saResult.value < TOLERANCE * 2, 'SA objective value too high');

console.log(`✓ Simulated Annealing passed (found minimum: ${saResult.value.toFixed(6)})`);

// ============================================
// Test Particle Swarm Optimization
// ============================================

console.log('\nTesting Particle Swarm Optimization...');

const pso = new opt.ParticleSwarm(
    simpleQuadratic,
    [[0, 5], [0, 5]],
    {
        swarmSize: 20,
        maxIterations: 50,
        verbose: false
    }
);

const psoResult = pso.optimize();
console.assert(psoResult.solution !== null, 'PSO returned null solution');
console.assert(Math.abs(psoResult.solution[0] - 2) < TOLERANCE, 'PSO solution x[0] incorrect');
console.assert(Math.abs(psoResult.solution[1] - 2) < TOLERANCE, 'PSO solution x[1] incorrect');
console.assert(psoResult.value < TOLERANCE, 'PSO objective value too high');

console.log(`✓ Particle Swarm passed (found minimum: ${psoResult.value.toFixed(6)})`);

// ============================================
// Test Gradient Descent
// ============================================

console.log('\nTesting Gradient Descent variants...');

// Test vanilla gradient descent
const gdVanilla = new opt.GradientDescent(
    simpleQuadratic,
    [[0, 5], [0, 5]],
    {
        method: 'vanilla',
        learningRate: 0.1,
        maxIterations: 100,
        verbose: false
    }
);

const gdVanillaResult = gdVanilla.optimize();
console.assert(gdVanillaResult.solution !== null, 'GD vanilla returned null solution');
console.assert(Math.abs(gdVanillaResult.solution[0] - 2) < TOLERANCE, 'GD vanilla x[0] incorrect');
console.assert(Math.abs(gdVanillaResult.solution[1] - 2) < TOLERANCE, 'GD vanilla x[1] incorrect');

console.log(`✓ Gradient Descent (vanilla) passed`);

// Test momentum
const gdMomentum = new opt.GradientDescent(
    simpleQuadratic,
    [[0, 5], [0, 5]],
    {
        method: 'momentum',
        learningRate: 0.05,
        momentum: 0.9,
        maxIterations: 100,
        verbose: false
    }
);

const gdMomentumResult = gdMomentum.optimize();
console.assert(Math.abs(gdMomentumResult.solution[0] - 2) < TOLERANCE, 'GD momentum x[0] incorrect');
console.assert(Math.abs(gdMomentumResult.solution[1] - 2) < TOLERANCE, 'GD momentum x[1] incorrect');

console.log(`✓ Gradient Descent (momentum) passed`);

// Test Adam
const gdAdam = new opt.GradientDescent(
    simpleQuadratic,
    [[0, 5], [0, 5]],
    {
        method: 'adam',
        learningRate: 0.1,
        maxIterations: 100,
        verbose: false
    }
);

const gdAdamResult = gdAdam.optimize();
console.assert(Math.abs(gdAdamResult.solution[0] - 2) < TOLERANCE, 'GD Adam x[0] incorrect');
console.assert(Math.abs(gdAdamResult.solution[1] - 2) < TOLERANCE, 'GD Adam x[1] incorrect');

console.log(`✓ Gradient Descent (Adam) passed`);

// ============================================
// Test Differential Evolution
// ============================================

console.log('\nTesting Differential Evolution...');

const de = new opt.DifferentialEvolution(
    simpleQuadratic,
    [[0, 5], [0, 5]],
    {
        populationSize: 20,
        generations: 50,
        verbose: false
    }
);

const deResult = de.optimize();
console.assert(deResult.solution !== null, 'DE returned null solution');
console.assert(Math.abs(deResult.solution[0] - 2) < TOLERANCE, 'DE solution x[0] incorrect');
console.assert(Math.abs(deResult.solution[1] - 2) < TOLERANCE, 'DE solution x[1] incorrect');
console.assert(deResult.value < TOLERANCE, 'DE objective value too high');

console.log(`✓ Differential Evolution passed (found minimum: ${deResult.value.toFixed(6)})`);

// ============================================
// Test Hill Climbing
// ============================================

console.log('\nTesting Hill Climbing...');

const hc = new opt.HillClimbing(
    simpleQuadratic,
    [[0, 5], [0, 5]],
    {
        maxIterations: 100,
        nRestarts: 3,
        verbose: false
    }
);

const hcResult = hc.optimize();
console.assert(hcResult.solution !== null, 'HC returned null solution');
console.assert(Math.abs(hcResult.solution[0] - 2) < TOLERANCE * 2, 'HC solution x[0] incorrect');
console.assert(Math.abs(hcResult.solution[1] - 2) < TOLERANCE * 2, 'HC solution x[1] incorrect');

console.log(`✓ Hill Climbing passed (found minimum: ${hcResult.value.toFixed(6)})`);

// ============================================
// Test Tabu Search
// ============================================

console.log('\nTesting Tabu Search...');

const ts = new opt.TabuSearch(
    simpleQuadratic,
    [[0, 5], [0, 5]],
    {
        maxIterations: 100,
        tabuTenure: 10,
        neighborhoodSize: 10,
        verbose: false
    }
);

const tsResult = ts.optimize();
console.assert(tsResult.solution !== null, 'TS returned null solution');
console.assert(Math.abs(tsResult.solution[0] - 2) < TOLERANCE * 3, 'TS solution x[0] incorrect');
console.assert(Math.abs(tsResult.solution[1] - 2) < TOLERANCE * 3, 'TS solution x[1] incorrect');

console.log(`✓ Tabu Search passed (found minimum: ${tsResult.value.toFixed(6)})`);

// ============================================
// Test Ant Colony Optimization
// ============================================

console.log('\nTesting Ant Colony Optimization...');

const aco = new opt.AntColonyOptimization(
    simpleQuadratic,
    [[0, 5], [0, 5]],
    {
        nAnts: 10,
        nIterations: 50,
        archiveSize: 5,
        verbose: false
    }
);

const acoResult = aco.optimize();
console.assert(acoResult.solution !== null, 'ACO returned null solution');
console.assert(Math.abs(acoResult.solution[0] - 2) < TOLERANCE * 2, 'ACO solution x[0] incorrect');
console.assert(Math.abs(acoResult.solution[1] - 2) < TOLERANCE * 2, 'ACO solution x[1] incorrect');

console.log(`✓ Ant Colony Optimization passed (found minimum: ${acoResult.value.toFixed(6)})`);

// ============================================
// Test on 1D function
// ============================================

console.log('\nTesting on 1D function...');

const de1D = new opt.DifferentialEvolution(
    parabola,
    [[0, 6]],
    {
        populationSize: 10,
        generations: 30,
        verbose: false
    }
);

const result1D = de1D.optimize();
console.assert(Math.abs(result1D.solution[0] - 3) < TOLERANCE, '1D optimization failed');
console.assert(Math.abs(result1D.value - 1) < TOLERANCE, '1D objective value incorrect');

console.log('✓ 1D optimization passed');

// ============================================
// Test maximization
// ============================================

console.log('\nTesting maximization...');

function negParabola(x) {
    return -(Math.pow(x[0] - 3, 2) + 1); // Maximum at x=3, value=-1
}

const maxOpt = new opt.ParticleSwarm(
    negParabola,
    [[0, 6]],
    {
        swarmSize: 15,
        maxIterations: 50,
        minimize: false,
        verbose: false
    }
);

const maxResult = maxOpt.optimize();
console.assert(Math.abs(maxResult.solution[0] - 3) < TOLERANCE, 'Maximization solution incorrect');
console.assert(Math.abs(maxResult.value - (-1)) < TOLERANCE, 'Maximization value incorrect');

console.log('✓ Maximization passed');

// ============================================
// Test utility functions
// ============================================

console.log('\nTesting utility functions...');

// Test createBounds
const bounds = opt.createBounds(3, -10, 10);
console.assert(bounds.length === 3, 'createBounds dimension incorrect');
console.assert(bounds[0][0] === -10 && bounds[0][1] === 10, 'createBounds values incorrect');

console.log('✓ Utility functions passed');

// ============================================
// Test on multimodal function
// ============================================

console.log('\nTesting on multimodal function (Rastrigin 2D)...');

const multimodalOpt = new opt.DifferentialEvolution(
    opt.testFunctions.rastrigin.fn,
    opt.createBounds(2, -5.12, 5.12),
    {
        populationSize: 50,
        generations: 100,
        verbose: false
    }
);

const multiResult = multimodalOpt.optimize();
console.assert(multiResult.solution !== null, 'Multimodal optimization failed');
console.assert(multiResult.value < 5, 'Multimodal optimization poor result');

console.log(`✓ Multimodal optimization passed (found minimum: ${multiResult.value.toFixed(6)})`);

// ============================================
// Test algorithm comparison
// ============================================

console.log('\nTesting algorithm comparison...');

const testAlgorithms = [
    ['GA', opt.GeneticAlgorithm, { populationSize: 20, generations: 30 }],
    ['PSO', opt.ParticleSwarm, { swarmSize: 20, maxIterations: 30 }]
];

const compResults = opt.compareOptimizers(
    testAlgorithms,
    simpleQuadratic,
    [[0, 5], [0, 5]],
    3
);

console.assert(compResults['GA'] !== undefined, 'Comparison missing GA results');
console.assert(compResults['PSO'] !== undefined, 'Comparison missing PSO results');
console.assert(compResults['GA'].mean !== undefined, 'Comparison missing mean');
console.assert(compResults['GA'].std !== undefined, 'Comparison missing std');

console.log('✓ Algorithm comparison passed');

// ============================================
// Performance test on higher dimensions
// ============================================

console.log('\nTesting on higher dimensions (5D)...');

const highDimOpt = new opt.ParticleSwarm(
    simpleQuadratic,
    opt.createBounds(5, 0, 5),
    {
        swarmSize: 30,
        maxIterations: 100,
        verbose: false
    }
);

const highDimResult = highDimOpt.optimize();
console.assert(highDimResult.solution.length === 5, 'High-dim solution wrong dimension');

let allNear2 = true;
for (let i = 0; i < 5; i++) {
    if (Math.abs(highDimResult.solution[i] - 2) > TOLERANCE * 2) {
        allNear2 = false;
        break;
    }
}
console.assert(allNear2, 'High-dim solution not near optimum');

console.log(`✓ High-dimensional optimization passed (5D, value: ${highDimResult.value.toFixed(6)})`);

console.log('\n=== All Optimization tests completed successfully ===');