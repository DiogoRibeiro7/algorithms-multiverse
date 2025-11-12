/**
 * Search Visualizer
 * Handles search algorithm visualizations (Linear, Binary, Jump, Interpolation)
 */

export class SearchVisualizer {
    constructor(canvas, core) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.core = core;

        this.array = [];
        this.arraySize = 30;
        this.targetValue = 50;
        this.found = false;
        this.foundIndex = -1;

        this.colors = {
            default: '#3b82f6',
            checking: '#f59e0b',
            found: '#10b981',
            notFound: '#94a3b8',
            target: '#ef4444',
            range: '#8b5cf6'
        };

        this.resize();
        this.generateData();
    }

    /**
     * Resize canvas to fit container
     */
    resize() {
        const container = this.canvas.parentElement;
        const rect = container.getBoundingClientRect();

        this.canvas.width = Math.min(800, rect.width - 32);
        this.canvas.height = 400;

        this.draw();
    }

    /**
     * Generate sorted array data
     */
    generateData() {
        this.core.reset();

        // Generate sorted array for search algorithms
        this.array = Array.from({ length: this.arraySize }, (_, i) => (i + 1) * 3);

        // Set random target that exists in array
        const randomIndex = Math.floor(Math.random() * this.array.length);
        this.targetValue = this.array[randomIndex];

        this.found = false;
        this.foundIndex = -1;
        this.draw();
    }

    /**
     * Set target value
     */
    setTarget(value) {
        this.targetValue = value;
        this.found = false;
        this.foundIndex = -1;
        this.draw();
    }

    /**
     * Draw array with highlights
     */
    draw(highlightIndices = {}) {
        const ctx = this.ctx;
        const width = this.canvas.width;
        const height = this.canvas.height;

        // Clear canvas
        ctx.clearRect(0, 0, width, height);

        // Draw target value display
        ctx.fillStyle = this.colors.target;
        ctx.font = 'bold 20px Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(`Target: ${this.targetValue}`, width / 2, 30);

        // Calculate bar dimensions
        const barWidth = width / this.array.length;
        const maxValue = Math.max(...this.array);
        const padding = 80;

        // Draw range highlight (for binary/jump search)
        if (highlightIndices.range) {
            const [start, end] = highlightIndices.range;
            ctx.fillStyle = 'rgba(139, 92, 246, 0.1)';
            ctx.fillRect(
                start * barWidth,
                padding,
                (end - start + 1) * barWidth,
                height - padding - 20
            );
        }

        // Draw bars
        this.array.forEach((value, index) => {
            const barHeight = ((value / maxValue) * (height - padding - 20));
            const x = index * barWidth;
            const y = height - barHeight - 20;

            // Determine color
            let color = this.colors.default;
            if (highlightIndices.found === index) {
                color = this.colors.found;
            } else if (highlightIndices.checking === index) {
                color = this.colors.checking;
            } else if (highlightIndices.visited && highlightIndices.visited.includes(index)) {
                color = this.colors.notFound;
            }

            // Draw bar
            ctx.fillStyle = color;
            ctx.fillRect(x + 1, y, barWidth - 2, barHeight);

            // Draw value (if bars are wide enough)
            if (barWidth > 20) {
                ctx.fillStyle = '#ffffff';
                ctx.font = '11px monospace';
                ctx.textAlign = 'center';
                ctx.fillText(value, x + barWidth / 2, y + 15);
            }

            // Draw index
            ctx.fillStyle = '#6b7280';
            ctx.font = '10px monospace';
            ctx.fillText(index, x + barWidth / 2, height - 5);
        });

        // Draw result message
        if (highlightIndices.message) {
            ctx.fillStyle = highlightIndices.found !== undefined ? this.colors.found : this.colors.target;
            ctx.font = 'bold 16px Inter, sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText(highlightIndices.message, width / 2, 55);
        }
    }

    /**
     * Start search visualization
     */
    async start(algorithm, target) {
        this.targetValue = target;
        this.core.reset();

        switch (algorithm) {
            case 'linear':
                await this.linearSearch();
                break;
            case 'binary':
                await this.binarySearch();
                break;
            case 'jump':
                await this.jumpSearch();
                break;
            case 'interpolation':
                await this.interpolationSearch();
                break;
            default:
                console.error('Unknown search algorithm:', algorithm);
                return;
        }

        this.core.start();
    }

    /**
     * Linear Search
     */
    async linearSearch() {
        const visited = [];

        for (let i = 0; i < this.array.length; i++) {
            // Check current element
            this.core.addStep(() => {
                this.core.recordComparison();
                this.core.recordAccess();
                this.draw({
                    checking: i,
                    visited: [...visited]
                });
            });

            if (this.array[i] === this.targetValue) {
                // Found!
                this.core.addStep(() => {
                    this.foundIndex = i;
                    this.found = true;
                    this.draw({
                        found: i,
                        visited: [...visited],
                        message: `Found at index ${i}!`
                    });
                });
                return;
            }

            visited.push(i);
        }

        // Not found
        this.core.addStep(() => {
            this.draw({
                visited: [...visited],
                message: 'Target not found in array'
            });
        });
    }

    /**
     * Binary Search
     */
    async binarySearch() {
        let left = 0;
        let right = this.array.length - 1;
        const visited = [];

        while (left <= right) {
            const mid = Math.floor((left + right) / 2);

            // Show current range and mid
            this.core.addStep(() => {
                this.core.recordComparison();
                this.core.recordAccess();
                this.draw({
                    checking: mid,
                    range: [left, right],
                    visited: [...visited]
                });
            });

            if (this.array[mid] === this.targetValue) {
                // Found!
                this.core.addStep(() => {
                    this.foundIndex = mid;
                    this.found = true;
                    this.draw({
                        found: mid,
                        visited: [...visited],
                        message: `Found at index ${mid}!`
                    });
                });
                return;
            }

            visited.push(mid);

            if (this.array[mid] < this.targetValue) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }

        // Not found
        this.core.addStep(() => {
            this.draw({
                visited: [...visited],
                message: 'Target not found in array'
            });
        });
    }

    /**
     * Jump Search
     */
    async jumpSearch() {
        const n = this.array.length;
        const jump = Math.floor(Math.sqrt(n));
        let prev = 0;
        const visited = [];

        // Jump to find the block
        while (this.array[Math.min(jump, n) - 1] < this.targetValue) {
            // Show jump
            this.core.addStep(() => {
                this.core.recordComparison();
                this.core.recordAccess();
                const checkIndex = Math.min(jump, n) - 1;
                this.draw({
                    checking: checkIndex,
                    range: [prev, Math.min(jump, n) - 1],
                    visited: [...visited]
                });
            });

            visited.push(Math.min(jump, n) - 1);
            prev = jump;

            if (prev >= n) {
                // Not found
                this.core.addStep(() => {
                    this.draw({
                        visited: [...visited],
                        message: 'Target not found in array'
                    });
                });
                return;
            }
        }

        // Linear search in the block
        for (let i = prev; i < Math.min(jump, n); i++) {
            this.core.addStep(() => {
                this.core.recordComparison();
                this.core.recordAccess();
                this.draw({
                    checking: i,
                    range: [prev, Math.min(jump, n) - 1],
                    visited: [...visited]
                });
            });

            if (this.array[i] === this.targetValue) {
                // Found!
                this.core.addStep(() => {
                    this.foundIndex = i;
                    this.found = true;
                    this.draw({
                        found: i,
                        visited: [...visited],
                        message: `Found at index ${i}!`
                    });
                });
                return;
            }

            visited.push(i);
        }

        // Not found
        this.core.addStep(() => {
            this.draw({
                visited: [...visited],
                message: 'Target not found in array'
            });
        });
    }

    /**
     * Interpolation Search
     */
    async interpolationSearch() {
        let left = 0;
        let right = this.array.length - 1;
        const visited = [];

        while (left <= right &&
               this.targetValue >= this.array[left] &&
               this.targetValue <= this.array[right]) {

            // Calculate interpolated position
            const pos = left + Math.floor(
                ((this.targetValue - this.array[left]) / (this.array[right] - this.array[left])) *
                (right - left)
            );

            // Show current position and range
            this.core.addStep(() => {
                this.core.recordComparison();
                this.core.recordAccess();
                this.draw({
                    checking: pos,
                    range: [left, right],
                    visited: [...visited]
                });
            });

            if (this.array[pos] === this.targetValue) {
                // Found!
                this.core.addStep(() => {
                    this.foundIndex = pos;
                    this.found = true;
                    this.draw({
                        found: pos,
                        visited: [...visited],
                        message: `Found at index ${pos}!`
                    });
                });
                return;
            }

            visited.push(pos);

            if (this.array[pos] < this.targetValue) {
                left = pos + 1;
            } else {
                right = pos - 1;
            }
        }

        // Not found
        this.core.addStep(() => {
            this.draw({
                visited: [...visited],
                message: 'Target not found in array'
            });
        });
    }

    /**
     * Reset visualization
     */
    reset() {
        this.core.reset();
        this.generateData();
    }

    /**
     * Pause search
     */
    pause() {
        this.core.pause();
    }
}
