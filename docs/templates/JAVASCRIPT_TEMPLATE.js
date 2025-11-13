/**
 * @fileoverview JavaScript Documentation Template for Algorithms Multiverse
 *
 * This template provides the standard documentation format for JavaScript files
 * in the Algorithms Multiverse project.
 *
 * @module algorithm-module
 * @author Algorithms Multiverse
 * @version 1.0.0
 *
 * @description
 * Brief description of what this module does.
 *
 * Features:
 * - Feature 1
 * - Feature 2
 * - Feature 3
 *
 * @requires module:dependency1
 * @requires module:dependency2
 *
 * @example
 * // Basic usage
 * const { algorithmFunction } = require('./module');
 * const result = algorithmFunction([1, 2, 3], { param1: 10 });
 * console.log(result);
 *
 * @see {@link https://example.com/docs|Documentation}
 */

'use strict';

// ============================================================================
// CONSTANTS
// ============================================================================

/**
 * Maximum allowed array size for processing.
 * @constant {number}
 * @default
 */
const MAX_ARRAY_SIZE = 1000000;

/**
 * Default timeout in milliseconds.
 * @constant {number}
 * @default
 */
const DEFAULT_TIMEOUT = 5000;

// ============================================================================
// CUSTOM ERROR CLASSES
// ============================================================================

/**
 * Base error class for algorithm-related errors.
 *
 * @class AlgorithmError
 * @extends Error
 *
 * @example
 * throw new AlgorithmError('Algorithm failed');
 */
class AlgorithmError extends Error {
    /**
     * Creates an AlgorithmError.
     *
     * @param {string} message - Error message
     * @param {Object} [details={}] - Additional error details
     * @param {string} [details.code] - Error code
     * @param {*} [details.context] - Error context
     */
    constructor(message, details = {}) {
        super(message);
        this.name = 'AlgorithmError';
        this.details = details;

        // Maintains proper stack trace for where error was thrown (V8 only)
        if (Error.captureStackTrace) {
            Error.captureStackTrace(this, AlgorithmError);
        }
    }
}

/**
 * Error thrown when input validation fails.
 *
 * @class InvalidInputError
 * @extends AlgorithmError
 */
class InvalidInputError extends AlgorithmError {
    /**
     * Creates an InvalidInputError.
     *
     * @param {string} message - Error message
     * @param {string} paramName - Name of invalid parameter
     * @param {*} paramValue - The invalid value
     */
    constructor(message, paramName, paramValue) {
        super(message, { paramName, paramValue });
        this.name = 'InvalidInputError';
        this.paramName = paramName;
        this.paramValue = paramValue;
    }
}

// ============================================================================
// TYPE DEFINITIONS (JSDoc)
// ============================================================================

/**
 * Options for algorithm configuration.
 *
 * @typedef {Object} AlgorithmOptions
 * @property {number} [param1=10] - First parameter (range: 0-1000)
 * @property {string} [param2=null] - Optional second parameter
 * @property {boolean} [validate=true] - Whether to validate inputs
 * @property {number} [timeout=5000] - Timeout in milliseconds
 * @property {Function} [onProgress] - Progress callback function
 */

/**
 * Result object returned by algorithm functions.
 *
 * @typedef {Object} AlgorithmResult
 * @property {boolean} success - Whether operation succeeded
 * @property {*} result - The actual result data
 * @property {Object} metrics - Performance metrics
 * @property {number} metrics.time - Execution time in ms
 * @property {number} metrics.comparisons - Number of comparisons
 * @property {number} metrics.iterations - Number of iterations
 * @property {?string} error - Error message if failed
 */

/**
 * Callback for progress updates.
 *
 * @callback ProgressCallback
 * @param {number} progress - Progress percentage (0-100)
 * @param {string} stage - Current stage description
 */

// ============================================================================
// INPUT VALIDATION
// ============================================================================

/**
 * Validates input data and parameters.
 *
 * @private
 * @function validateInput
 *
 * @param {Array} data - Input data array
 * @param {AlgorithmOptions} options - Algorithm options
 *
 * @throws {InvalidInputError} If validation fails
 * @throws {TypeError} If types are incorrect
 *
 * @returns {void}
 *
 * @example
 * try {
 *     validateInput([1, 2, 3], { param1: 10 });
 * } catch (error) {
 *     console.error('Validation failed:', error);
 * }
 */
function validateInput(data, options) {
    // Check data exists
    if (data === null || data === undefined) {
        throw new InvalidInputError(
            'Data cannot be null or undefined',
            'data',
            data
        );
    }

    // Check data is an array
    if (!Array.isArray(data)) {
        throw new TypeError(
            `Expected array, got ${typeof data}`
        );
    }

    // Check array is not empty
    if (data.length === 0) {
        throw new InvalidInputError(
            'Input array cannot be empty',
            'data',
            data
        );
    }

    // Check array size
    if (data.length > MAX_ARRAY_SIZE) {
        throw new InvalidInputError(
            `Array size ${data.length} exceeds maximum ${MAX_ARRAY_SIZE}`,
            'data',
            data
        );
    }

    // Validate options
    if (options.param1 !== undefined) {
        if (typeof options.param1 !== 'number') {
            throw new TypeError(
                `param1 must be number, got ${typeof options.param1}`
            );
        }
        if (options.param1 < 0 || options.param1 > 1000) {
            throw new InvalidInputError(
                `param1 must be in range [0, 1000], got ${options.param1}`,
                'param1',
                options.param1
            );
        }
    }

    // Validate param2 if provided
    if (options.param2 !== null && options.param2 !== undefined) {
        if (typeof options.param2 !== 'string') {
            throw new TypeError(
                `param2 must be string, got ${typeof options.param2}`
            );
        }
    }
}

// ============================================================================
// MAIN ALGORITHM FUNCTION
// ============================================================================

/**
 * Main algorithm function with comprehensive documentation.
 *
 * Detailed description of what this algorithm does, how it works,
 * and when to use it. Explain the approach and any important
 * implementation details.
 *
 * Algorithm Steps:
 * 1. Validate input parameters
 * 2. Initialize data structures
 * 3. Process data according to algorithm
 * 4. Return results with metrics
 *
 * @function algorithmFunction
 * @public
 *
 * @template T
 * @param {T[]} data - Input array to process (must be non-empty)
 * @param {AlgorithmOptions} [options={}] - Configuration options
 * @param {number} [options.param1=10] - First parameter
 * @param {string} [options.param2=null] - Second parameter
 * @param {boolean} [options.validate=true] - Enable input validation
 * @param {ProgressCallback} [options.onProgress] - Progress callback
 *
 * @returns {AlgorithmResult} Result object with success status and data
 *
 * @throws {InvalidInputError} If input validation fails
 * @throws {AlgorithmError} If algorithm encounters an error
 * @throws {TypeError} If types are incorrect
 *
 * @complexity
 * Time Complexity:
 * - Best Case: O(n)
 * - Average Case: O(n log n)
 * - Worst Case: O(n²)
 *
 * Space Complexity: O(n)
 *
 * @example <caption>Basic usage</caption>
 * const result = algorithmFunction([3, 1, 4, 1, 5]);
 * console.log(result.success); // true
 * console.log(result.result);  // [1, 1, 3, 4, 5]
 *
 * @example <caption>With options</caption>
 * const result = algorithmFunction(
 *     [5, 2, 8, 1, 9],
 *     {
 *         param1: 20,
 *         param2: 'custom',
 *         validate: true,
 *         onProgress: (progress, stage) => {
 *             console.log(`${stage}: ${progress}%`);
 *         }
 *     }
 * );
 *
 * @example <caption>Error handling</caption>
 * try {
 *     const result = algorithmFunction([]);
 * } catch (error) {
 *     if (error instanceof InvalidInputError) {
 *         console.error('Invalid input:', error.message);
 *         console.error('Parameter:', error.paramName);
 *     }
 * }
 *
 * @see {@link helperFunction}
 * @see {@link https://example.com/algorithm|Algorithm Documentation}
 *
 * @since 1.0.0
 */
function algorithmFunction(data, options = {}) {
    // Start timing
    const startTime = performance.now();

    // Default options
    const config = {
        param1: 10,
        param2: null,
        validate: true,
        timeout: DEFAULT_TIMEOUT,
        onProgress: null,
        ...options
    };

    // Initialize metrics
    const metrics = {
        comparisons: 0,
        swaps: 0,
        iterations: 0,
        time: 0
    };

    try {
        // Input validation
        if (config.validate) {
            validateInput(data, config);
        }

        // Report progress
        if (typeof config.onProgress === 'function') {
            config.onProgress(0, 'Starting algorithm');
        }

        // Main algorithm implementation
        const result = coreAlgorithm(
            data,
            config.param1,
            config.param2,
            metrics,
            config.onProgress
        );

        // Calculate execution time
        metrics.time = performance.now() - startTime;

        // Report completion
        if (typeof config.onProgress === 'function') {
            config.onProgress(100, 'Complete');
        }

        return {
            success: true,
            result: result,
            metrics: metrics,
            error: null
        };

    } catch (error) {
        metrics.time = performance.now() - startTime;

        // Handle specific error types
        if (error instanceof InvalidInputError) {
            console.error('Input validation failed:', error.message);
        } else if (error instanceof AlgorithmError) {
            console.error('Algorithm error:', error.message);
        } else {
            console.error('Unexpected error:', error);
        }

        return {
            success: false,
            result: null,
            metrics: metrics,
            error: error.message
        };
    }
}

// ============================================================================
// CORE ALGORITHM (PRIVATE)
// ============================================================================

/**
 * Core algorithm implementation.
 *
 * @private
 * @function coreAlgorithm
 *
 * @template T
 * @param {T[]} data - Validated input data
 * @param {number} param1 - Validated parameter 1
 * @param {?string} param2 - Validated parameter 2
 * @param {Object} metrics - Metrics object to update
 * @param {?ProgressCallback} onProgress - Progress callback
 *
 * @returns {T[]} Processed data
 *
 * @throws {AlgorithmError} If processing fails
 */
function coreAlgorithm(data, param1, param2, metrics, onProgress) {
    // Create a copy to avoid mutating input
    const result = [...data];

    // Algorithm implementation goes here
    for (let i = 0; i < result.length; i++) {
        metrics.iterations++;

        // Report progress periodically
        if (onProgress && i % 100 === 0) {
            const progress = Math.floor((i / result.length) * 100);
            onProgress(progress, `Processing element ${i}`);
        }
    }

    return result;
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Check if input is valid without throwing exceptions.
 *
 * @function isValidInput
 * @public
 *
 * @param {*} data - Data to validate
 * @returns {boolean} True if valid, false otherwise
 *
 * @example
 * if (isValidInput([1, 2, 3])) {
 *     const result = algorithmFunction([1, 2, 3]);
 * }
 */
function isValidInput(data) {
    try {
        validateInput(data, { param1: 10 });
        return true;
    } catch (error) {
        return false;
    }
}

/**
 * Get algorithm information and metadata.
 *
 * @function getAlgorithmInfo
 * @public
 *
 * @returns {Object} Algorithm metadata
 * @returns {string} return.name - Algorithm name
 * @returns {string} return.version - Version number
 * @returns {Object} return.complexity - Complexity information
 *
 * @example
 * const info = getAlgorithmInfo();
 * console.log(`${info.name} v${info.version}`);
 * console.log(`Complexity: ${info.complexity.average}`);
 */
function getAlgorithmInfo() {
    return {
        name: 'Algorithm Name',
        version: '1.0.0',
        author: 'Algorithms Multiverse',
        complexity: {
            best: 'O(n)',
            average: 'O(n log n)',
            worst: 'O(n²)',
            space: 'O(n)'
        },
        features: [
            'Feature 1',
            'Feature 2',
            'Feature 3'
        ]
    };
}

// ============================================================================
// CLASS-BASED IMPLEMENTATION
// ============================================================================

/**
 * Class-based algorithm implementation with state management.
 *
 * @class Algorithm
 *
 * @description
 * Provides a stateful interface to the algorithm with configuration
 * and statistics tracking.
 *
 * @property {number} param1 - Configuration parameter 1
 * @property {?string} param2 - Configuration parameter 2
 * @property {Object} statistics - Performance statistics
 *
 * @example <caption>Basic usage</caption>
 * const algo = new Algorithm({ param1: 15 });
 * const result1 = algo.process([3, 1, 4]);
 * const result2 = algo.process([2, 7, 1]);
 * console.log(algo.getStatistics());
 *
 * @example <caption>With event listeners</caption>
 * const algo = new Algorithm();
 * algo.on('progress', (progress) => {
 *     console.log(`Progress: ${progress}%`);
 * });
 * algo.on('complete', (result) => {
 *     console.log('Done:', result);
 * });
 * algo.process([1, 2, 3, 4, 5]);
 */
class Algorithm {
    /**
     * Create an Algorithm instance.
     *
     * @param {AlgorithmOptions} [options={}] - Configuration options
     * @throws {InvalidInputError} If configuration is invalid
     */
    constructor(options = {}) {
        this.param1 = options.param1 || 10;
        this.param2 = options.param2 || null;
        this.validate = options.validate !== false;

        this.statistics = {
            totalRuns: 0,
            totalTime: 0,
            averageTime: 0,
            lastResult: null
        };

        this.eventListeners = new Map();

        // Validate configuration
        if (this.param1 < 0 || this.param1 > 1000) {
            throw new InvalidInputError(
                `param1 must be in [0, 1000], got ${this.param1}`,
                'param1',
                this.param1
            );
        }
    }

    /**
     * Process data using configured parameters.
     *
     * @param {Array} data - Input data to process
     * @returns {AlgorithmResult} Processing result
     *
     * @fires Algorithm#progress
     * @fires Algorithm#complete
     * @fires Algorithm#error
     */
    process(data) {
        const result = algorithmFunction(data, {
            param1: this.param1,
            param2: this.param2,
            validate: this.validate,
            onProgress: (progress, stage) => {
                this.emit('progress', { progress, stage });
            }
        });

        // Update statistics
        this.statistics.totalRuns++;
        this.statistics.totalTime += result.metrics.time;
        this.statistics.averageTime =
            this.statistics.totalTime / this.statistics.totalRuns;
        this.statistics.lastResult = result.result;

        // Emit events
        if (result.success) {
            this.emit('complete', result);
        } else {
            this.emit('error', new AlgorithmError(result.error));
        }

        return result;
    }

    /**
     * Register event listener.
     *
     * @param {string} event - Event name ('progress', 'complete', 'error')
     * @param {Function} callback - Callback function
     * @returns {Algorithm} This instance for chaining
     */
    on(event, callback) {
        if (!this.eventListeners.has(event)) {
            this.eventListeners.set(event, []);
        }
        this.eventListeners.get(event).push(callback);
        return this;
    }

    /**
     * Emit event to listeners.
     *
     * @private
     * @param {string} event - Event name
     * @param {*} data - Event data
     */
    emit(event, data) {
        const listeners = this.eventListeners.get(event) || [];
        listeners.forEach(callback => callback(data));
    }

    /**
     * Get current statistics.
     *
     * @returns {Object} Statistics object
     */
    getStatistics() {
        return { ...this.statistics };
    }

    /**
     * Reset statistics.
     *
     * @returns {void}
     */
    resetStatistics() {
        this.statistics = {
            totalRuns: 0,
            totalTime: 0,
            averageTime: 0,
            lastResult: null
        };
    }
}

// ============================================================================
// EXPORTS
// ============================================================================

// CommonJS (Node.js)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        algorithmFunction,
        Algorithm,
        isValidInput,
        getAlgorithmInfo,
        AlgorithmError,
        InvalidInputError,
        MAX_ARRAY_SIZE,
        DEFAULT_TIMEOUT
    };
}

// ES6 modules
export {
    algorithmFunction,
    Algorithm,
    isValidInput,
    getAlgorithmInfo,
    AlgorithmError,
    InvalidInputError,
    MAX_ARRAY_SIZE,
    DEFAULT_TIMEOUT
};

// ============================================================================
// MAIN EXECUTION (for direct running)
// ============================================================================

if (typeof require !== 'undefined' && require.main === module) {
    console.log('='.repeat(70));
    console.log('Algorithm Function Demonstration');
    console.log('='.repeat(70));

    // Example 1: Basic usage
    console.log('\nExample 1: Basic Usage');
    console.log('-'.repeat(70));
    const data1 = [5, 2, 8, 1, 9, 3, 7];
    const result1 = algorithmFunction(data1);
    console.log('Input:', data1);
    console.log('Success:', result1.success);
    console.log('Result:', result1.result);
    console.log('Metrics:', result1.metrics);

    // Example 2: Error handling
    console.log('\nExample 2: Error Handling');
    console.log('-'.repeat(70));
    const result2 = algorithmFunction([]);
    console.log('Success:', result2.success);
    console.log('Error:', result2.error);

    // Example 3: Class-based approach
    console.log('\nExample 3: Class-Based Approach');
    console.log('-'.repeat(70));
    const algo = new Algorithm({ param1: 5 });
    algo.on('progress', ({ progress, stage }) => {
        console.log(`${stage}: ${progress}%`);
    });
    algo.process([3, 1, 4]);
    algo.process([2, 7, 1]);
    console.log('Statistics:', algo.getStatistics());

    console.log('\n' + '='.repeat(70));
    console.log('Demonstration Complete!');
    console.log('='.repeat(70));
}
