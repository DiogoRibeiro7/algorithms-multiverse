/**
 * Visualizer Core - Central engine for all visualizations
 * Handles animation, state management, and common utilities
 */

export class VisualizerCore {
    constructor() {
        this.state = {
            isRunning: false,
            isPaused: false,
            speed: 5, // 1-10 scale
            currentStep: 0,
            totalSteps: 0
        };

        this.animationQueue = [];
        this.animationFrame = null;
        this.stats = {
            comparisons: 0,
            swaps: 0,
            accesses: 0,
            startTime: 0
        };

        this.onStatsUpdate = null;
        this.onComplete = null;
    }

    /**
     * Reset the core state
     */
    reset() {
        this.stop();
        this.animationQueue = [];
        this.state.currentStep = 0;
        this.state.totalSteps = 0;
        this.resetStats();
    }

    /**
     * Reset statistics
     */
    resetStats() {
        this.stats = {
            comparisons: 0,
            swaps: 0,
            accesses: 0,
            startTime: 0
        };
        this.updateStatsDisplay();
    }

    /**
     * Start execution
     */
    start() {
        this.state.isRunning = true;
        this.state.isPaused = false;
        this.stats.startTime = Date.now();
        this.processAnimationQueue();
    }

    /**
     * Pause execution
     */
    pause() {
        this.state.isPaused = !this.state.isPaused;
        if (!this.state.isPaused) {
            this.processAnimationQueue();
        }
    }

    /**
     * Stop execution
     */
    stop() {
        this.state.isRunning = false;
        this.state.isPaused = false;
        if (this.animationFrame) {
            cancelAnimationFrame(this.animationFrame);
            this.animationFrame = null;
        }
    }

    /**
     * Set animation speed (1-10)
     */
    setSpeed(speed) {
        this.state.speed = Math.max(1, Math.min(10, speed));
    }

    /**
     * Get delay in milliseconds based on speed
     */
    getDelay() {
        // Map speed 1-10 to delays 500ms-50ms
        return 550 - (this.state.speed * 50);
    }

    /**
     * Add animation step to queue
     */
    addStep(renderFunction, data = {}) {
        this.animationQueue.push({
            render: renderFunction,
            data: data
        });
        this.state.totalSteps = this.animationQueue.length;
    }

    /**
     * Process animation queue
     */
    async processAnimationQueue() {
        if (this.state.currentStep >= this.animationQueue.length) {
            this.complete();
            return;
        }

        if (!this.state.isRunning || this.state.isPaused) {
            return;
        }

        const step = this.animationQueue[this.state.currentStep];

        // Execute render function
        if (step && step.render) {
            try {
                await step.render(step.data);
            } catch (error) {
                console.error('Error executing animation step:', error);
            }
        }

        this.state.currentStep++;

        // Schedule next step
        setTimeout(() => {
            this.animationFrame = requestAnimationFrame(() => {
                this.processAnimationQueue();
            });
        }, this.getDelay());
    }

    /**
     * Mark algorithm as complete
     */
    complete() {
        this.state.isRunning = false;
        this.state.isPaused = false;

        if (this.onComplete) {
            this.onComplete({
                stats: this.stats,
                elapsed: Date.now() - this.stats.startTime
            });
        }

        console.log('✅ Algorithm completed', this.stats);
    }

    /**
     * Record a comparison
     */
    recordComparison() {
        this.stats.comparisons++;
        this.updateStatsDisplay();
    }

    /**
     * Record a swap
     */
    recordSwap() {
        this.stats.swaps++;
        this.updateStatsDisplay();
    }

    /**
     * Record an array access
     */
    recordAccess(count = 1) {
        this.stats.accesses += count;
        this.updateStatsDisplay();
    }

    /**
     * Update statistics display
     */
    updateStatsDisplay() {
        const comparisonsEl = document.getElementById('comparisons');
        const accessesEl = document.getElementById('accesses');
        const timeEl = document.getElementById('time-elapsed');

        if (comparisonsEl) {
            comparisonsEl.textContent = this.stats.comparisons.toLocaleString();
        }

        if (accessesEl) {
            accessesEl.textContent = this.stats.accesses.toLocaleString();
        }

        if (timeEl && this.stats.startTime > 0) {
            const elapsed = Date.now() - this.stats.startTime;
            timeEl.textContent = `${elapsed}ms`;
        }

        if (this.onStatsUpdate) {
            this.onStatsUpdate(this.stats);
        }
    }

    /**
     * Generate random array
     */
    generateRandomArray(size, min = 10, max = 100) {
        return Array.from({ length: size }, () =>
            Math.floor(Math.random() * (max - min + 1)) + min
        );
    }

    /**
     * Generate nearly sorted array
     */
    generateNearlySortedArray(size, shufflePercent = 0.2) {
        const arr = Array.from({ length: size }, (_, i) => i + 1);
        const shuffleCount = Math.floor(size * shufflePercent);

        for (let i = 0; i < shuffleCount; i++) {
            const idx1 = Math.floor(Math.random() * size);
            const idx2 = Math.floor(Math.random() * size);
            [arr[idx1], arr[idx2]] = [arr[idx2], arr[idx1]];
        }

        return arr;
    }

    /**
     * Generate reversed array
     */
    generateReversedArray(size) {
        return Array.from({ length: size }, (_, i) => size - i);
    }

    /**
     * Interpolate color between two colors
     */
    interpolateColor(color1, color2, factor) {
        const c1 = this.hexToRgb(color1);
        const c2 = this.hexToRgb(color2);

        const r = Math.round(c1.r + factor * (c2.r - c1.r));
        const g = Math.round(c1.g + factor * (c2.g - c1.g));
        const b = Math.round(c1.b + factor * (c2.b - c1.b));

        return `rgb(${r}, ${g}, ${b})`;
    }

    /**
     * Convert hex to RGB
     */
    hexToRgb(hex) {
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16)
        } : null;
    }

    /**
     * Get color for array value
     */
    getColorForValue(value, min, max) {
        const factor = (value - min) / (max - min);
        return this.interpolateColor('#3b82f6', '#8b5cf6', factor);
    }

    /**
     * Sleep for specified milliseconds
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Format complexity notation
     */
    formatComplexity(notation) {
        const complexityMap = {
            '1': 'O(1)',
            'logn': 'O(log n)',
            'n': 'O(n)',
            'nlogn': 'O(n log n)',
            'n2': 'O(n²)',
            'n3': 'O(n³)',
            '2n': 'O(2ⁿ)'
        };

        return complexityMap[notation] || notation;
    }

    /**
     * Calculate complexity value for given n
     */
    calculateComplexity(notation, n) {
        switch (notation) {
            case '1':
                return 1;
            case 'logn':
                return Math.log2(n);
            case 'n':
                return n;
            case 'nlogn':
                return n * Math.log2(n);
            case 'n2':
                return n * n;
            case 'n3':
                return n * n * n;
            case '2n':
                return Math.pow(2, n);
            default:
                return n;
        }
    }

    /**
     * Normalize value to 0-1 range
     */
    normalize(value, min, max) {
        return (value - min) / (max - min);
    }

    /**
     * Clamp value between min and max
     */
    clamp(value, min, max) {
        return Math.max(min, Math.min(max, value));
    }

    /**
     * Shuffle array (Fisher-Yates)
     */
    shuffleArray(array) {
        const arr = [...array];
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        return arr;
    }

    /**
     * Check if array is sorted
     */
    isSorted(array) {
        for (let i = 0; i < array.length - 1; i++) {
            if (array[i] > array[i + 1]) {
                return false;
            }
        }
        return true;
    }

    /**
     * Get algorithm complexity information
     */
    getAlgorithmInfo(algorithmName) {
        const algorithmInfo = {
            bubble: {
                name: 'Bubble Sort',
                description: 'Repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order.',
                timeComplexity: {
                    best: 'O(n)',
                    average: 'O(n²)',
                    worst: 'O(n²)'
                },
                spaceComplexity: 'O(1)',
                stable: true
            },
            selection: {
                name: 'Selection Sort',
                description: 'Divides the input into a sorted and unsorted region, repeatedly selecting the smallest element from the unsorted region.',
                timeComplexity: {
                    best: 'O(n²)',
                    average: 'O(n²)',
                    worst: 'O(n²)'
                },
                spaceComplexity: 'O(1)',
                stable: false
            },
            insertion: {
                name: 'Insertion Sort',
                description: 'Builds the final sorted array one item at a time, inserting each element into its correct position.',
                timeComplexity: {
                    best: 'O(n)',
                    average: 'O(n²)',
                    worst: 'O(n²)'
                },
                spaceComplexity: 'O(1)',
                stable: true
            },
            merge: {
                name: 'Merge Sort',
                description: 'Divide and conquer algorithm that divides the array into halves, sorts them, and merges them back together.',
                timeComplexity: {
                    best: 'O(n log n)',
                    average: 'O(n log n)',
                    worst: 'O(n log n)'
                },
                spaceComplexity: 'O(n)',
                stable: true
            },
            quick: {
                name: 'Quick Sort',
                description: 'Divide and conquer algorithm that picks a pivot element and partitions the array around it.',
                timeComplexity: {
                    best: 'O(n log n)',
                    average: 'O(n log n)',
                    worst: 'O(n²)'
                },
                spaceComplexity: 'O(log n)',
                stable: false
            },
            heap: {
                name: 'Heap Sort',
                description: 'Uses a binary heap data structure to sort elements, building a max heap and extracting elements.',
                timeComplexity: {
                    best: 'O(n log n)',
                    average: 'O(n log n)',
                    worst: 'O(n log n)'
                },
                spaceComplexity: 'O(1)',
                stable: false
            }
        };

        return algorithmInfo[algorithmName] || null;
    }
}
