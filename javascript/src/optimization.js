/**
 * Optimization Algorithms Module
 * Metaheuristic and gradient-based optimization techniques
 */

// ============================================
// Test Functions for Optimization
// ============================================

/**
 * Collection of benchmark functions for testing optimization algorithms
 */
export const testFunctions = {
    /**
     * Sphere function - simple convex function
     * Global minimum: f(0, 0, ..., 0) = 0
     */
    sphere: {
        fn: (x) => x.reduce((sum, xi) => sum + xi * xi, 0),
        bounds: [-5.12, 5.12],
        optimum: 0,
        dimension: 'n'
    },

    /**
     * Rosenbrock function - non-convex with narrow valley
     * Global minimum: f(1, 1, ..., 1) = 0
     */
    rosenbrock: {
        fn: (x) => {
            let sum = 0;
            for (let i = 0; i < x.length - 1; i++) {
                sum += 100 * Math.pow(x[i + 1] - x[i] * x[i], 2) + Math.pow(1 - x[i], 2);
            }
            return sum;
        },
        bounds: [-5, 10],
        optimum: 0,
        dimension: 'n'
    },

    /**
     * Rastrigin function - highly multimodal
     * Global minimum: f(0, 0, ..., 0) = 0
     */
    rastrigin: {
        fn: (x) => {
            const A = 10;
            const n = x.length;
            return A * n + x.reduce((sum, xi) => sum + xi * xi - A * Math.cos(2 * Math.PI * xi), 0);
        },
        bounds: [-5.12, 5.12],
        optimum: 0,
        dimension: 'n'
    },

    /**
     * Ackley function - multimodal with many local minima
     * Global minimum: f(0, 0, ..., 0) = 0
     */
    ackley: {
        fn: (x) => {
            const n = x.length;
            const sum1 = x.reduce((sum, xi) => sum + xi * xi, 0) / n;
            const sum2 = x.reduce((sum, xi) => sum + Math.cos(2 * Math.PI * xi), 0) / n;
            return -20 * Math.exp(-0.2 * Math.sqrt(sum1)) - Math.exp(sum2) + 20 + Math.E;
        },
        bounds: [-32.768, 32.768],
        optimum: 0,
        dimension: 'n'
    },

    /**
     * Griewank function - many local minima
     * Global minimum: f(0, 0, ..., 0) = 0
     */
    griewank: {
        fn: (x) => {
            const sum = x.reduce((s, xi) => s + xi * xi / 4000, 0);
            const prod = x.reduce((p, xi, i) => p * Math.cos(xi / Math.sqrt(i + 1)), 1);
            return sum - prod + 1;
        },
        bounds: [-600, 600],
        optimum: 0,
        dimension: 'n'
    },

    /**
     * Schwefel function - deceptive multimodal
     * Global minimum: f(420.9687, ..., 420.9687) ≈ 0
     */
    schwefel: {
        fn: (x) => {
            const n = x.length;
            const sum = x.reduce((s, xi) => s - xi * Math.sin(Math.sqrt(Math.abs(xi))), 0);
            return 418.9829 * n + sum;
        },
        bounds: [-500, 500],
        optimum: 0,
        dimension: 'n'
    },

    /**
     * Beale function (2D only)
     * Global minimum: f(3, 0.5) = 0
     */
    beale: {
        fn: (x) => {
            if (x.length !== 2) throw new Error('Beale function requires exactly 2 dimensions');
            const [x1, x2] = x;
            return Math.pow(1.5 - x1 + x1 * x2, 2) +
                   Math.pow(2.25 - x1 + x1 * x2 * x2, 2) +
                   Math.pow(2.625 - x1 + x1 * x2 * x2 * x2, 2);
        },
        bounds: [-4.5, 4.5],
        optimum: 0,
        dimension: 2
    },

    /**
     * Booth function (2D only)
     * Global minimum: f(1, 3) = 0
     */
    booth: {
        fn: (x) => {
            if (x.length !== 2) throw new Error('Booth function requires exactly 2 dimensions');
            const [x1, x2] = x;
            return Math.pow(x1 + 2 * x2 - 7, 2) + Math.pow(2 * x1 + x2 - 5, 2);
        },
        bounds: [-10, 10],
        optimum: 0,
        dimension: 2
    },

    /**
     * Himmelblau function (2D only) - four global minima
     * Global minima: f(3, 2) = f(-2.805, 3.131) = f(-3.779, -3.283) = f(3.584, -1.848) = 0
     */
    himmelblau: {
        fn: (x) => {
            if (x.length !== 2) throw new Error('Himmelblau function requires exactly 2 dimensions');
            const [x1, x2] = x;
            return Math.pow(x1 * x1 + x2 - 11, 2) + Math.pow(x1 + x2 * x2 - 7, 2);
        },
        bounds: [-5, 5],
        optimum: 0,
        dimension: 2
    }
};

// ============================================
// Base Optimizer Class
// ============================================

/**
 * Base class for optimization algorithms
 */
export class Optimizer {
    constructor(objectiveFunction, bounds, options = {}) {
        this.objectiveFunction = objectiveFunction;
        this.bounds = bounds; // Array of [min, max] for each dimension
        this.dimension = bounds.length;
        this.minimize = options.minimize !== undefined ? options.minimize : true;
        this.verbose = options.verbose || false;
        this.history = [];
    }

    /**
     * Evaluate objective function (handle minimization/maximization)
     */
    evaluate(x) {
        const value = this.objectiveFunction(x);
        return this.minimize ? value : -value;
    }

    /**
     * Check if solution is within bounds
     */
    isWithinBounds(x) {
        for (let i = 0; i < x.length; i++) {
            if (x[i] < this.bounds[i][0] || x[i] > this.bounds[i][1]) {
                return false;
            }
        }
        return true;
    }

    /**
     * Clip solution to bounds
     */
    clipToBounds(x) {
        return x.map((xi, i) => {
            return Math.max(this.bounds[i][0], Math.min(this.bounds[i][1], xi));
        });
    }

    /**
     * Random initialization within bounds
     */
    randomSolution() {
        return this.bounds.map(([min, max]) => min + Math.random() * (max - min));
    }

    /**
     * Abstract optimize method - must be implemented by subclasses
     */
    optimize() {
        throw new Error('optimize() must be implemented by subclass');
    }
}

// ============================================
// Genetic Algorithm
// ============================================

/**
 * Genetic Algorithm optimizer
 */
export class GeneticAlgorithm extends Optimizer {
    constructor(objectiveFunction, bounds, options = {}) {
        super(objectiveFunction, bounds, options);

        // GA parameters
        this.populationSize = options.populationSize || 50;
        this.generations = options.generations || 100;
        this.crossoverRate = options.crossoverRate || 0.8;
        this.mutationRate = options.mutationRate || 0.1;
        this.eliteSize = options.eliteSize || 2;
        this.selectionMethod = options.selectionMethod || 'tournament';
        this.tournamentSize = options.tournamentSize || 3;

        this.population = [];
        this.fitness = [];
    }

    /**
     * Initialize population
     */
    initializePopulation() {
        this.population = [];
        for (let i = 0; i < this.populationSize; i++) {
            this.population.push(this.randomSolution());
        }
    }

    /**
     * Evaluate fitness for entire population
     */
    evaluatePopulation() {
        this.fitness = this.population.map(individual => this.evaluate(individual));
    }

    /**
     * Tournament selection
     */
    tournamentSelection() {
        const tournamentIndices = [];
        for (let i = 0; i < this.tournamentSize; i++) {
            tournamentIndices.push(Math.floor(Math.random() * this.populationSize));
        }

        let bestIdx = tournamentIndices[0];
        let bestFitness = this.fitness[bestIdx];

        for (let i = 1; i < tournamentIndices.length; i++) {
            const idx = tournamentIndices[i];
            if (this.fitness[idx] < bestFitness) {
                bestFitness = this.fitness[idx];
                bestIdx = idx;
            }
        }

        return this.population[bestIdx];
    }

    /**
     * Roulette wheel selection
     */
    rouletteSelection() {
        // Convert fitness to positive values for selection
        const minFitness = Math.min(...this.fitness);
        const adjustedFitness = this.fitness.map(f => 1 / (1 + f - minFitness));
        const totalFitness = adjustedFitness.reduce((sum, f) => sum + f, 0);

        const random = Math.random() * totalFitness;
        let cumSum = 0;

        for (let i = 0; i < this.populationSize; i++) {
            cumSum += adjustedFitness[i];
            if (cumSum >= random) {
                return this.population[i];
            }
        }

        return this.population[this.populationSize - 1];
    }

    /**
     * Select parent for reproduction
     */
    selectParent() {
        if (this.selectionMethod === 'tournament') {
            return this.tournamentSelection();
        } else if (this.selectionMethod === 'roulette') {
            return this.rouletteSelection();
        } else {
            throw new Error(`Unknown selection method: ${this.selectionMethod}`);
        }
    }

    /**
     * Uniform crossover
     */
    crossover(parent1, parent2) {
        const child1 = [];
        const child2 = [];

        for (let i = 0; i < this.dimension; i++) {
            if (Math.random() < 0.5) {
                child1.push(parent1[i]);
                child2.push(parent2[i]);
            } else {
                child1.push(parent2[i]);
                child2.push(parent1[i]);
            }
        }

        return [child1, child2];
    }

    /**
     * Arithmetic crossover
     */
    arithmeticCrossover(parent1, parent2) {
        const alpha = Math.random();
        const child1 = [];
        const child2 = [];

        for (let i = 0; i < this.dimension; i++) {
            child1.push(alpha * parent1[i] + (1 - alpha) * parent2[i]);
            child2.push((1 - alpha) * parent1[i] + alpha * parent2[i]);
        }

        return [child1, child2];
    }

    /**
     * Gaussian mutation
     */
    mutate(individual) {
        const mutated = [...individual];

        for (let i = 0; i < this.dimension; i++) {
            if (Math.random() < this.mutationRate) {
                // Gaussian mutation with adaptive step size
                const range = this.bounds[i][1] - this.bounds[i][0];
                const sigma = range * 0.1; // 10% of range
                mutated[i] += this.gaussianRandom() * sigma;
            }
        }

        return this.clipToBounds(mutated);
    }

    /**
     * Generate Gaussian random number (Box-Muller transform)
     */
    gaussianRandom() {
        let u1 = Math.random();
        let u2 = Math.random();
        return Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
    }

    /**
     * Create new generation
     */
    createNextGeneration() {
        const newPopulation = [];

        // Elitism - keep best individuals
        const sortedIndices = this.fitness
            .map((f, i) => ({ fitness: f, index: i }))
            .sort((a, b) => a.fitness - b.fitness)
            .map(item => item.index);

        for (let i = 0; i < this.eliteSize; i++) {
            newPopulation.push([...this.population[sortedIndices[i]]]);
        }

        // Generate offspring
        while (newPopulation.length < this.populationSize) {
            const parent1 = this.selectParent();

            if (Math.random() < this.crossoverRate) {
                const parent2 = this.selectParent();
                const [child1, child2] = this.arithmeticCrossover(parent1, parent2);
                newPopulation.push(this.mutate(child1));
                if (newPopulation.length < this.populationSize) {
                    newPopulation.push(this.mutate(child2));
                }
            } else {
                newPopulation.push(this.mutate(parent1));
            }
        }

        // Ensure correct population size
        this.population = newPopulation.slice(0, this.populationSize);
    }

    /**
     * Run genetic algorithm optimization
     */
    optimize() {
        this.initializePopulation();
        this.evaluatePopulation();

        let bestSolution = null;
        let bestFitness = Infinity;

        for (let gen = 0; gen < this.generations; gen++) {
            // Find best in current generation
            const genBestIdx = this.fitness.indexOf(Math.min(...this.fitness));
            const genBestFitness = this.fitness[genBestIdx];

            if (genBestFitness < bestFitness) {
                bestFitness = genBestFitness;
                bestSolution = [...this.population[genBestIdx]];
            }

            // Store history
            this.history.push({
                generation: gen,
                bestFitness: bestFitness,
                avgFitness: this.fitness.reduce((sum, f) => sum + f, 0) / this.populationSize
            });

            if (this.verbose && gen % 10 === 0) {
                console.log(`Generation ${gen}: Best fitness = ${bestFitness.toFixed(6)}`);
            }

            // Create next generation
            this.createNextGeneration();
            this.evaluatePopulation();
        }

        return {
            solution: bestSolution,
            value: this.minimize ? bestFitness : -bestFitness,
            iterations: this.generations,
            history: this.history
        };
    }
}

// ============================================
// Simulated Annealing
// ============================================

/**
 * Simulated Annealing optimizer
 */
export class SimulatedAnnealing extends Optimizer {
    constructor(objectiveFunction, bounds, options = {}) {
        super(objectiveFunction, bounds, options);

        // SA parameters
        this.maxIterations = options.maxIterations || 1000;
        this.initialTemp = options.initialTemp || 100;
        this.coolingRate = options.coolingRate || 0.95;
        this.minTemp = options.minTemp || 0.001;
        this.neighborhoodSize = options.neighborhoodSize || 0.1;
    }

    /**
     * Generate neighbor solution
     */
    generateNeighbor(current) {
        const neighbor = [...current];

        // Perturb random dimensions
        const nPerturb = Math.max(1, Math.floor(Math.random() * this.dimension));
        const indices = [];

        while (indices.length < nPerturb) {
            const idx = Math.floor(Math.random() * this.dimension);
            if (!indices.includes(idx)) {
                indices.push(idx);
            }
        }

        for (const idx of indices) {
            const range = this.bounds[idx][1] - this.bounds[idx][0];
            const delta = (Math.random() - 0.5) * 2 * range * this.neighborhoodSize;
            neighbor[idx] += delta;
        }

        return this.clipToBounds(neighbor);
    }

    /**
     * Acceptance probability
     */
    acceptanceProbability(currentCost, newCost, temperature) {
        if (newCost < currentCost) {
            return 1.0;
        }
        return Math.exp(-(newCost - currentCost) / temperature);
    }

    /**
     * Run simulated annealing optimization
     */
    optimize() {
        // Initialize
        let current = this.randomSolution();
        let currentCost = this.evaluate(current);

        let best = [...current];
        let bestCost = currentCost;

        let temperature = this.initialTemp;
        let iteration = 0;

        while (iteration < this.maxIterations && temperature > this.minTemp) {
            // Generate neighbor
            const neighbor = this.generateNeighbor(current);
            const neighborCost = this.evaluate(neighbor);

            // Accept or reject
            if (Math.random() < this.acceptanceProbability(currentCost, neighborCost, temperature)) {
                current = neighbor;
                currentCost = neighborCost;

                // Update best
                if (currentCost < bestCost) {
                    best = [...current];
                    bestCost = currentCost;
                }
            }

            // Store history
            this.history.push({
                iteration,
                temperature,
                currentCost,
                bestCost
            });

            if (this.verbose && iteration % 100 === 0) {
                console.log(`Iteration ${iteration}: T=${temperature.toFixed(4)}, Best=${bestCost.toFixed(6)}`);
            }

            // Cool down
            temperature *= this.coolingRate;
            iteration++;
        }

        return {
            solution: best,
            value: this.minimize ? bestCost : -bestCost,
            iterations: iteration,
            history: this.history
        };
    }
}

// ============================================
// Particle Swarm Optimization
// ============================================

/**
 * Particle Swarm Optimization
 */
export class ParticleSwarm extends Optimizer {
    constructor(objectiveFunction, bounds, options = {}) {
        super(objectiveFunction, bounds, options);

        // PSO parameters
        this.swarmSize = options.swarmSize || 30;
        this.maxIterations = options.maxIterations || 100;
        this.inertia = options.inertia || 0.7;
        this.cognitiveWeight = options.cognitiveWeight || 1.5;
        this.socialWeight = options.socialWeight || 1.5;
        this.maxVelocity = options.maxVelocity || 0.2; // Fraction of range

        this.particles = [];
        this.velocities = [];
        this.personalBest = [];
        this.personalBestCost = [];
        this.globalBest = null;
        this.globalBestCost = Infinity;
    }

    /**
     * Initialize swarm
     */
    initializeSwarm() {
        for (let i = 0; i < this.swarmSize; i++) {
            // Initialize position
            const position = this.randomSolution();
            this.particles.push(position);

            // Initialize velocity
            const velocity = this.bounds.map(([min, max]) => {
                const range = max - min;
                return (Math.random() - 0.5) * range * this.maxVelocity;
            });
            this.velocities.push(velocity);

            // Initialize personal best
            this.personalBest.push([...position]);
            const cost = this.evaluate(position);
            this.personalBestCost.push(cost);

            // Update global best
            if (cost < this.globalBestCost) {
                this.globalBest = [...position];
                this.globalBestCost = cost;
            }
        }
    }

    /**
     * Update particle velocity and position
     */
    updateParticle(idx) {
        const particle = this.particles[idx];
        const velocity = this.velocities[idx];
        const pBest = this.personalBest[idx];

        // Update velocity
        for (let d = 0; d < this.dimension; d++) {
            const r1 = Math.random();
            const r2 = Math.random();

            velocity[d] = this.inertia * velocity[d] +
                         this.cognitiveWeight * r1 * (pBest[d] - particle[d]) +
                         this.socialWeight * r2 * (this.globalBest[d] - particle[d]);

            // Limit velocity
            const maxV = (this.bounds[d][1] - this.bounds[d][0]) * this.maxVelocity;
            velocity[d] = Math.max(-maxV, Math.min(maxV, velocity[d]));

            // Update position
            particle[d] += velocity[d];
        }

        // Ensure within bounds
        this.particles[idx] = this.clipToBounds(particle);
    }

    /**
     * Run PSO optimization
     */
    optimize() {
        this.initializeSwarm();

        for (let iter = 0; iter < this.maxIterations; iter++) {
            // Update each particle
            for (let i = 0; i < this.swarmSize; i++) {
                this.updateParticle(i);

                // Evaluate new position
                const cost = this.evaluate(this.particles[i]);

                // Update personal best
                if (cost < this.personalBestCost[i]) {
                    this.personalBest[i] = [...this.particles[i]];
                    this.personalBestCost[i] = cost;

                    // Update global best
                    if (cost < this.globalBestCost) {
                        this.globalBest = [...this.particles[i]];
                        this.globalBestCost = cost;
                    }
                }
            }

            // Adaptive inertia (optional)
            this.inertia *= 0.99;

            // Store history
            this.history.push({
                iteration: iter,
                globalBestCost: this.globalBestCost,
                avgCost: this.personalBestCost.reduce((sum, c) => sum + c, 0) / this.swarmSize
            });

            if (this.verbose && iter % 10 === 0) {
                console.log(`Iteration ${iter}: Best = ${this.globalBestCost.toFixed(6)}`);
            }
        }

        return {
            solution: this.globalBest,
            value: this.minimize ? this.globalBestCost : -this.globalBestCost,
            iterations: this.maxIterations,
            history: this.history
        };
    }
}

// ============================================
// Gradient-Based Methods
// ============================================

/**
 * Gradient Descent and variants
 */
export class GradientDescent extends Optimizer {
    constructor(objectiveFunction, bounds, options = {}) {
        super(objectiveFunction, bounds, options);

        // GD parameters
        this.learningRate = options.learningRate || 0.01;
        this.maxIterations = options.maxIterations || 1000;
        this.tolerance = options.tolerance || 1e-6;
        this.method = options.method || 'vanilla'; // vanilla, momentum, adam

        // Method-specific parameters
        this.momentum = options.momentum || 0.9;
        this.beta1 = options.beta1 || 0.9; // Adam
        this.beta2 = options.beta2 || 0.999; // Adam
        this.epsilon = options.epsilon || 1e-8; // Adam

        // Gradient function (if provided)
        this.gradientFunction = options.gradientFunction || null;
    }

    /**
     * Numerical gradient computation (if analytical gradient not provided)
     */
    computeGradient(x) {
        if (this.gradientFunction) {
            return this.gradientFunction(x);
        }

        const grad = [];
        const h = 1e-5;
        const fx = this.evaluate(x);

        for (let i = 0; i < this.dimension; i++) {
            const xPlus = [...x];
            xPlus[i] += h;
            const fxPlus = this.evaluate(xPlus);
            grad.push((fxPlus - fx) / h);
        }

        return grad;
    }

    /**
     * Vanilla gradient descent update
     */
    vanillaUpdate(x, gradient) {
        const updated = [];
        for (let i = 0; i < this.dimension; i++) {
            updated.push(x[i] - this.learningRate * gradient[i]);
        }
        return this.clipToBounds(updated);
    }

    /**
     * Momentum gradient descent update
     */
    momentumUpdate(x, gradient, velocity) {
        const updated = [];
        const newVelocity = [];

        for (let i = 0; i < this.dimension; i++) {
            newVelocity[i] = this.momentum * velocity[i] - this.learningRate * gradient[i];
            updated.push(x[i] + newVelocity[i]);
        }

        return {
            x: this.clipToBounds(updated),
            velocity: newVelocity
        };
    }

    /**
     * Adam optimizer update
     */
    adamUpdate(x, gradient, m, v, t) {
        const updated = [];
        const newM = [];
        const newV = [];

        for (let i = 0; i < this.dimension; i++) {
            // Update biased first moment estimate
            newM[i] = this.beta1 * m[i] + (1 - this.beta1) * gradient[i];

            // Update biased second moment estimate
            newV[i] = this.beta2 * v[i] + (1 - this.beta2) * gradient[i] * gradient[i];

            // Compute bias-corrected moments
            const mHat = newM[i] / (1 - Math.pow(this.beta1, t));
            const vHat = newV[i] / (1 - Math.pow(this.beta2, t));

            // Update parameters
            updated.push(x[i] - this.learningRate * mHat / (Math.sqrt(vHat) + this.epsilon));
        }

        return {
            x: this.clipToBounds(updated),
            m: newM,
            v: newV
        };
    }

    /**
     * Run gradient descent optimization
     */
    optimize() {
        // Initialize
        let x = this.randomSolution();
        let bestX = [...x];
        let bestCost = this.evaluate(x);

        // Method-specific initialization
        let velocity = Array(this.dimension).fill(0); // For momentum
        let m = Array(this.dimension).fill(0); // For Adam
        let v = Array(this.dimension).fill(0); // For Adam

        for (let iter = 0; iter < this.maxIterations; iter++) {
            // Compute gradient
            const gradient = this.computeGradient(x);

            // Update based on method
            if (this.method === 'vanilla') {
                x = this.vanillaUpdate(x, gradient);
            } else if (this.method === 'momentum') {
                const result = this.momentumUpdate(x, gradient, velocity);
                x = result.x;
                velocity = result.velocity;
            } else if (this.method === 'adam') {
                const result = this.adamUpdate(x, gradient, m, v, iter + 1);
                x = result.x;
                m = result.m;
                v = result.v;
            }

            // Evaluate new position
            const cost = this.evaluate(x);

            // Update best
            if (cost < bestCost) {
                bestX = [...x];
                bestCost = cost;
            }

            // Check convergence
            const gradNorm = Math.sqrt(gradient.reduce((sum, g) => sum + g * g, 0));

            this.history.push({
                iteration: iter,
                cost: cost,
                gradientNorm: gradNorm
            });

            if (this.verbose && iter % 100 === 0) {
                console.log(`Iteration ${iter}: Cost = ${cost.toFixed(6)}, |∇| = ${gradNorm.toFixed(6)}`);
            }

            if (gradNorm < this.tolerance) {
                if (this.verbose) {
                    console.log(`Converged at iteration ${iter}`);
                }
                break;
            }
        }

        return {
            solution: bestX,
            value: this.minimize ? bestCost : -bestCost,
            iterations: this.history.length,
            history: this.history
        };
    }
}

// ============================================
// Differential Evolution
// ============================================

/**
 * Differential Evolution optimizer
 */
export class DifferentialEvolution extends Optimizer {
    constructor(objectiveFunction, bounds, options = {}) {
        super(objectiveFunction, bounds, options);

        // DE parameters
        this.populationSize = options.populationSize || 50;
        this.generations = options.generations || 100;
        this.F = options.F || 0.8; // Differential weight
        this.CR = options.CR || 0.9; // Crossover probability
        this.strategy = options.strategy || 'best1bin'; // DE/best/1/bin

        this.population = [];
        this.fitness = [];
    }

    /**
     * Initialize population
     */
    initializePopulation() {
        this.population = [];
        this.fitness = [];

        for (let i = 0; i < this.populationSize; i++) {
            const individual = this.randomSolution();
            this.population.push(individual);
            this.fitness.push(this.evaluate(individual));
        }
    }

    /**
     * Select random individuals (excluding current)
     */
    selectIndividuals(currentIdx, count) {
        const selected = [];
        const available = Array.from({length: this.populationSize}, (_, i) => i)
            .filter(i => i !== currentIdx);

        for (let i = 0; i < count; i++) {
            const idx = Math.floor(Math.random() * available.length);
            selected.push(available[idx]);
            available.splice(idx, 1);
        }

        return selected;
    }

    /**
     * Create mutant vector
     */
    createMutant(targetIdx) {
        const mutant = [];

        if (this.strategy === 'rand1bin') {
            // DE/rand/1/bin
            const [r1, r2, r3] = this.selectIndividuals(targetIdx, 3);
            for (let i = 0; i < this.dimension; i++) {
                mutant[i] = this.population[r1][i] +
                           this.F * (this.population[r2][i] - this.population[r3][i]);
            }
        } else if (this.strategy === 'best1bin') {
            // DE/best/1/bin
            const bestIdx = this.fitness.indexOf(Math.min(...this.fitness));
            const [r1, r2] = this.selectIndividuals(targetIdx, 2);
            for (let i = 0; i < this.dimension; i++) {
                mutant[i] = this.population[bestIdx][i] +
                           this.F * (this.population[r1][i] - this.population[r2][i]);
            }
        } else if (this.strategy === 'current-to-best1') {
            // DE/current-to-best/1
            const bestIdx = this.fitness.indexOf(Math.min(...this.fitness));
            const [r1, r2] = this.selectIndividuals(targetIdx, 2);
            for (let i = 0; i < this.dimension; i++) {
                mutant[i] = this.population[targetIdx][i] +
                           this.F * (this.population[bestIdx][i] - this.population[targetIdx][i]) +
                           this.F * (this.population[r1][i] - this.population[r2][i]);
            }
        }

        return this.clipToBounds(mutant);
    }

    /**
     * Binomial crossover
     */
    crossover(target, mutant) {
        const trial = [];
        const jRand = Math.floor(Math.random() * this.dimension);

        for (let j = 0; j < this.dimension; j++) {
            if (Math.random() < this.CR || j === jRand) {
                trial[j] = mutant[j];
            } else {
                trial[j] = target[j];
            }
        }

        return trial;
    }

    /**
     * Run differential evolution optimization
     */
    optimize() {
        this.initializePopulation();

        let bestIdx = this.fitness.indexOf(Math.min(...this.fitness));
        let bestSolution = [...this.population[bestIdx]];
        let bestFitness = this.fitness[bestIdx];

        for (let gen = 0; gen < this.generations; gen++) {
            const newPopulation = [];
            const newFitness = [];

            for (let i = 0; i < this.populationSize; i++) {
                // Create mutant
                const mutant = this.createMutant(i);

                // Crossover
                const trial = this.crossover(this.population[i], mutant);

                // Selection
                const trialFitness = this.evaluate(trial);

                if (trialFitness <= this.fitness[i]) {
                    newPopulation.push(trial);
                    newFitness.push(trialFitness);

                    // Update best
                    if (trialFitness < bestFitness) {
                        bestSolution = [...trial];
                        bestFitness = trialFitness;
                    }
                } else {
                    newPopulation.push([...this.population[i]]);
                    newFitness.push(this.fitness[i]);
                }
            }

            this.population = newPopulation;
            this.fitness = newFitness;

            // Store history
            this.history.push({
                generation: gen,
                bestFitness: bestFitness,
                avgFitness: this.fitness.reduce((sum, f) => sum + f, 0) / this.populationSize
            });

            if (this.verbose && gen % 10 === 0) {
                console.log(`Generation ${gen}: Best = ${bestFitness.toFixed(6)}`);
            }
        }

        return {
            solution: bestSolution,
            value: this.minimize ? bestFitness : -bestFitness,
            iterations: this.generations,
            history: this.history
        };
    }
}

// ============================================
// Hill Climbing
// ============================================

/**
 * Hill Climbing optimizer (with random restarts)
 */
export class HillClimbing extends Optimizer {
    constructor(objectiveFunction, bounds, options = {}) {
        super(objectiveFunction, bounds, options);

        this.maxIterations = options.maxIterations || 1000;
        this.stepSize = options.stepSize || 0.1;
        this.nRestarts = options.nRestarts || 1;
        this.adaptiveStep = options.adaptiveStep !== undefined ? options.adaptiveStep : true;
    }

    /**
     * Generate neighbors
     */
    generateNeighbors(current, stepSize) {
        const neighbors = [];

        // Generate neighbors in each dimension (positive and negative)
        for (let i = 0; i < this.dimension; i++) {
            // Positive direction
            const neighborPos = [...current];
            neighborPos[i] += stepSize * (this.bounds[i][1] - this.bounds[i][0]);
            neighbors.push(this.clipToBounds(neighborPos));

            // Negative direction
            const neighborNeg = [...current];
            neighborNeg[i] -= stepSize * (this.bounds[i][1] - this.bounds[i][0]);
            neighbors.push(this.clipToBounds(neighborNeg));
        }

        return neighbors;
    }

    /**
     * Climb from a starting point
     */
    climb(start) {
        let current = start;
        let currentCost = this.evaluate(current);
        let stepSize = this.stepSize;
        let noImprovement = 0;

        for (let iter = 0; iter < this.maxIterations; iter++) {
            // Generate neighbors
            const neighbors = this.generateNeighbors(current, stepSize);

            // Find best neighbor
            let bestNeighbor = null;
            let bestNeighborCost = currentCost;

            for (const neighbor of neighbors) {
                const cost = this.evaluate(neighbor);
                if (cost < bestNeighborCost) {
                    bestNeighbor = neighbor;
                    bestNeighborCost = cost;
                }
            }

            // Move to better neighbor or stop
            if (bestNeighbor !== null) {
                current = bestNeighbor;
                currentCost = bestNeighborCost;
                noImprovement = 0;

                // Increase step size if improving
                if (this.adaptiveStep) {
                    stepSize = Math.min(stepSize * 1.1, 0.5);
                }
            } else {
                noImprovement++;

                // Decrease step size if not improving
                if (this.adaptiveStep) {
                    stepSize *= 0.9;

                    if (stepSize < 1e-6) {
                        break; // Converged
                    }
                }

                if (noImprovement > 10 && !this.adaptiveStep) {
                    break; // Stuck at local optimum
                }
            }
        }

        return { solution: current, cost: currentCost };
    }

    /**
     * Run hill climbing with random restarts
     */
    optimize() {
        let bestSolution = null;
        let bestCost = Infinity;

        for (let restart = 0; restart < this.nRestarts; restart++) {
            // Random starting point
            const start = this.randomSolution();

            // Climb
            const result = this.climb(start);

            // Update best
            if (result.cost < bestCost) {
                bestSolution = result.solution;
                bestCost = result.cost;
            }

            this.history.push({
                restart,
                cost: result.cost,
                bestCost
            });

            if (this.verbose) {
                console.log(`Restart ${restart + 1}: Cost = ${result.cost.toFixed(6)}`);
            }
        }

        return {
            solution: bestSolution,
            value: this.minimize ? bestCost : -bestCost,
            iterations: this.nRestarts * this.maxIterations,
            history: this.history
        };
    }
}

// ============================================
// Tabu Search
// ============================================

/**
 * Tabu Search optimizer
 */
export class TabuSearch extends Optimizer {
    constructor(objectiveFunction, bounds, options = {}) {
        super(objectiveFunction, bounds, options);

        this.maxIterations = options.maxIterations || 1000;
        this.tabuTenure = options.tabuTenure || 10;
        this.neighborhoodSize = options.neighborhoodSize || 20;
        this.aspirationCriteria = options.aspirationCriteria !== undefined ? options.aspirationCriteria : true;

        this.tabuList = [];
    }

    /**
     * Generate neighborhood
     */
    generateNeighborhood(current) {
        const neighborhood = [];

        for (let i = 0; i < this.neighborhoodSize; i++) {
            const neighbor = [...current];

            // Random perturbation
            const nDims = Math.min(this.dimension, Math.max(1, Math.floor(Math.random() * 3) + 1));
            const dims = [];

            while (dims.length < nDims) {
                const dim = Math.floor(Math.random() * this.dimension);
                if (!dims.includes(dim)) {
                    dims.push(dim);
                }
            }

            for (const dim of dims) {
                const range = this.bounds[dim][1] - this.bounds[dim][0];
                neighbor[dim] += (Math.random() - 0.5) * range * 0.2;
            }

            neighborhood.push(this.clipToBounds(neighbor));
        }

        return neighborhood;
    }

    /**
     * Check if move is tabu
     */
    isTabu(solution) {
        for (const tabuSolution of this.tabuList) {
            let isSame = true;
            for (let i = 0; i < this.dimension; i++) {
                if (Math.abs(solution[i] - tabuSolution[i]) > 1e-6) {
                    isSame = false;
                    break;
                }
            }
            if (isSame) return true;
        }
        return false;
    }

    /**
     * Update tabu list
     */
    updateTabuList(solution) {
        this.tabuList.push([...solution]);

        // Remove oldest if list too long
        if (this.tabuList.length > this.tabuTenure) {
            this.tabuList.shift();
        }
    }

    /**
     * Run tabu search optimization
     */
    optimize() {
        let current = this.randomSolution();
        let currentCost = this.evaluate(current);

        let best = [...current];
        let bestCost = currentCost;

        this.updateTabuList(current);

        for (let iter = 0; iter < this.maxIterations; iter++) {
            // Generate neighborhood
            const neighborhood = this.generateNeighborhood(current);

            // Find best non-tabu neighbor (or best if aspiration criteria met)
            let bestNeighbor = null;
            let bestNeighborCost = Infinity;

            for (const neighbor of neighborhood) {
                const cost = this.evaluate(neighbor);

                // Check tabu status
                const isTabuMove = this.isTabu(neighbor);

                // Accept if not tabu or if aspiration criteria met
                if (!isTabuMove || (this.aspirationCriteria && cost < bestCost)) {
                    if (cost < bestNeighborCost) {
                        bestNeighbor = neighbor;
                        bestNeighborCost = cost;
                    }
                }
            }

            // Move to best neighbor
            if (bestNeighbor !== null) {
                current = bestNeighbor;
                currentCost = bestNeighborCost;
                this.updateTabuList(current);

                // Update global best
                if (currentCost < bestCost) {
                    best = [...current];
                    bestCost = currentCost;
                }
            }

            this.history.push({
                iteration: iter,
                currentCost,
                bestCost,
                tabuSize: this.tabuList.length
            });

            if (this.verbose && iter % 100 === 0) {
                console.log(`Iteration ${iter}: Best = ${bestCost.toFixed(6)}, Tabu size = ${this.tabuList.length}`);
            }
        }

        return {
            solution: best,
            value: this.minimize ? bestCost : -bestCost,
            iterations: this.maxIterations,
            history: this.history
        };
    }
}

// ============================================
// Ant Colony Optimization (for continuous domains)
// ============================================

/**
 * Ant Colony Optimization for continuous optimization
 */
export class AntColonyOptimization extends Optimizer {
    constructor(objectiveFunction, bounds, options = {}) {
        super(objectiveFunction, bounds, options);

        this.nAnts = options.nAnts || 20;
        this.nIterations = options.nIterations || 100;
        this.archiveSize = options.archiveSize || 10;
        this.q = options.q || 0.1; // Locality of search
        this.xi = options.xi || 0.85; // Convergence speed

        this.archive = [];
        this.weights = [];
    }

    /**
     * Initialize solution archive
     */
    initializeArchive() {
        this.archive = [];

        for (let i = 0; i < this.archiveSize; i++) {
            const solution = this.randomSolution();
            const fitness = this.evaluate(solution);
            this.archive.push({ solution, fitness });
        }

        this.archive.sort((a, b) => a.fitness - b.fitness);
        this.calculateWeights();
    }

    /**
     * Calculate selection probabilities
     */
    calculateWeights() {
        this.weights = [];
        const sum = this.archiveSize * (this.archiveSize + 1) / 2;

        for (let i = 0; i < this.archiveSize; i++) {
            const weight = (this.archiveSize - i) / sum;
            this.weights.push(weight);
        }
    }

    /**
     * Select solution from archive
     */
    selectSolution() {
        const r = Math.random();
        let cumSum = 0;

        for (let i = 0; i < this.archiveSize; i++) {
            cumSum += this.weights[i];
            if (r <= cumSum) {
                return this.archive[i].solution;
            }
        }

        return this.archive[this.archiveSize - 1].solution;
    }

    /**
     * Generate new solution
     */
    generateSolution() {
        const selected = this.selectSolution();
        const newSolution = [];

        for (let d = 0; d < this.dimension; d++) {
            // Sample from Gaussian kernel
            const sigma = this.xi * (this.bounds[d][1] - this.bounds[d][0]);
            const value = selected[d] + sigma * this.gaussianRandom() * this.q;
            newSolution.push(value);
        }

        return this.clipToBounds(newSolution);
    }

    /**
     * Gaussian random number generator
     */
    gaussianRandom() {
        let u1 = Math.random();
        let u2 = Math.random();
        return Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
    }

    /**
     * Update solution archive
     */
    updateArchive(newSolutions) {
        // Add new solutions to archive
        for (const sol of newSolutions) {
            this.archive.push(sol);
        }

        // Sort and keep best
        this.archive.sort((a, b) => a.fitness - b.fitness);
        this.archive = this.archive.slice(0, this.archiveSize);

        // Recalculate weights
        this.calculateWeights();
    }

    /**
     * Run ACO optimization
     */
    optimize() {
        this.initializeArchive();

        for (let iter = 0; iter < this.nIterations; iter++) {
            const newSolutions = [];

            // Generate new solutions
            for (let ant = 0; ant < this.nAnts; ant++) {
                const solution = this.generateSolution();
                const fitness = this.evaluate(solution);
                newSolutions.push({ solution, fitness });
            }

            // Update archive
            this.updateArchive(newSolutions);

            // Update convergence speed parameter
            if (this.xi > 0.5) {
                this.xi *= 0.99;
            }

            this.history.push({
                iteration: iter,
                bestFitness: this.archive[0].fitness,
                avgFitness: this.archive.reduce((sum, s) => sum + s.fitness, 0) / this.archiveSize
            });

            if (this.verbose && iter % 10 === 0) {
                console.log(`Iteration ${iter}: Best = ${this.archive[0].fitness.toFixed(6)}`);
            }
        }

        return {
            solution: this.archive[0].solution,
            value: this.minimize ? this.archive[0].fitness : -this.archive[0].fitness,
            iterations: this.nIterations,
            history: this.history
        };
    }
}

// ============================================
// Utility Functions
// ============================================

/**
 * Compare optimization algorithms on a test function
 */
export function compareOptimizers(optimizers, testFunction, bounds, runs = 10) {
    const results = {};

    for (const [name, OptimizerClass, options] of optimizers) {
        console.log(`Testing ${name}...`);
        const runResults = [];

        for (let run = 0; run < runs; run++) {
            const optimizer = new OptimizerClass(testFunction, bounds, { ...options, verbose: false });
            const result = optimizer.optimize();
            runResults.push(result.value);
        }

        results[name] = {
            best: Math.min(...runResults),
            worst: Math.max(...runResults),
            mean: runResults.reduce((sum, v) => sum + v, 0) / runs,
            std: Math.sqrt(runResults.reduce((sum, v) => sum + Math.pow(v - results[name]?.mean || 0, 2), 0) / runs)
        };
    }

    return results;
}

/**
 * Create bounds array for n-dimensional optimization
 */
export function createBounds(dimension, min, max) {
    return Array(dimension).fill([min, max]);
}

// Export all classes and functions
export default {
    // Test functions
    testFunctions,

    // Optimizers
    Optimizer,
    GeneticAlgorithm,
    SimulatedAnnealing,
    ParticleSwarm,
    GradientDescent,
    DifferentialEvolution,
    HillClimbing,
    TabuSearch,
    AntColonyOptimization,

    // Utilities
    compareOptimizers,
    createBounds
};