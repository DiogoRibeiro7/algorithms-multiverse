/**
 * Sorting Algorithm Visualizer
 * Handles visualization of all sorting algorithms
 */

export class SortingVisualizer {
    constructor(canvas, core) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.core = core;

        this.array = [];
        this.arraySize = 20;
        this.colors = {
            default: '#3b82f6',
            comparing: '#f59e0b',
            swapping: '#ef4444',
            sorted: '#10b981',
            pivot: '#8b5cf6'
        };

        this.resize();
        this.generateData('random');
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
     * Set array size
     */
    setArraySize(size) {
        this.arraySize = size;
        this.generateData('random');
    }

    /**
     * Set animation speed
     */
    setSpeed(speed) {
        this.core.setSpeed(speed);
    }

    /**
     * Generate data
     */
    generateData(type) {
        this.core.reset();

        switch (type) {
            case 'random':
                this.array = this.core.generateRandomArray(this.arraySize);
                break;
            case 'nearly-sorted':
                this.array = this.core.generateNearlySortedArray(this.arraySize);
                break;
            case 'reversed':
                this.array = this.core.generateReversedArray(this.arraySize);
                break;
            default:
                this.array = this.core.generateRandomArray(this.arraySize);
        }

        this.draw();
    }

    /**
     * Start sorting with selected algorithm
     */
    async start(algorithm) {
        this.core.reset();

        // Generate animation steps
        switch (algorithm) {
            case 'bubble':
                await this.bubbleSort();
                break;
            case 'selection':
                await this.selectionSort();
                break;
            case 'insertion':
                await this.insertionSort();
                break;
            case 'merge':
                await this.mergeSort();
                break;
            case 'quick':
                await this.quickSort();
                break;
            case 'heap':
                await this.heapSort();
                break;
            default:
                console.error('Unknown algorithm:', algorithm);
                return;
        }

        this.core.start();
    }

    /**
     * Pause sorting
     */
    pause() {
        this.core.pause();
    }

    /**
     * Reset visualization
     */
    reset() {
        this.core.reset();
        this.generateData('random');
    }

    /**
     * Draw array
     */
    draw(highlightIndices = {}) {
        const ctx = this.ctx;
        const width = this.canvas.width;
        const height = this.canvas.height;

        // Clear canvas
        ctx.clearRect(0, 0, width, height);

        // Calculate bar dimensions
        const barWidth = width / this.array.length;
        const maxValue = Math.max(...this.array);
        const padding = 40;

        // Draw bars
        this.array.forEach((value, index) => {
            const barHeight = ((value / maxValue) * (height - padding));
            const x = index * barWidth;
            const y = height - barHeight;

            // Determine color
            let color = this.colors.default;
            if (highlightIndices.comparing && highlightIndices.comparing.includes(index)) {
                color = this.colors.comparing;
            } else if (highlightIndices.swapping && highlightIndices.swapping.includes(index)) {
                color = this.colors.swapping;
            } else if (highlightIndices.sorted && highlightIndices.sorted.includes(index)) {
                color = this.colors.sorted;
            } else if (highlightIndices.pivot && highlightIndices.pivot === index) {
                color = this.colors.pivot;
            } else {
                // Gradient color based on value
                color = this.core.getColorForValue(value, 1, maxValue);
            }

            // Draw bar
            ctx.fillStyle = color;
            ctx.fillRect(x + 1, y, barWidth - 2, barHeight);

            // Draw value (if bars are wide enough)
            if (barWidth > 20) {
                ctx.fillStyle = '#ffffff';
                ctx.font = '12px monospace';
                ctx.textAlign = 'center';
                ctx.fillText(value, x + barWidth / 2, y + 20);
            }
        });
    }

    /**
     * Bubble Sort
     */
    async bubbleSort() {
        const arr = [...this.array];
        const n = arr.length;

        for (let i = 0; i < n - 1; i++) {
            for (let j = 0; j < n - i - 1; j++) {
                // Compare
                this.core.addStep(() => {
                    this.core.recordComparison();
                    this.core.recordAccess(2);
                    this.draw({ comparing: [j, j + 1] });
                });

                if (arr[j] > arr[j + 1]) {
                    // Swap
                    [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];

                    this.core.addStep(() => {
                        this.core.recordSwap();
                        this.array = [...arr];
                        this.draw({ swapping: [j, j + 1] });
                    });
                }
            }

            // Mark as sorted
            this.core.addStep(() => {
                const sorted = Array.from({ length: i + 1 }, (_, idx) => n - 1 - idx);
                this.draw({ sorted });
            });
        }

        // Final state - all sorted
        this.core.addStep(() => {
            const sorted = Array.from({ length: n }, (_, idx) => idx);
            this.draw({ sorted });
        });
    }

    /**
     * Selection Sort
     */
    async selectionSort() {
        const arr = [...this.array];
        const n = arr.length;

        for (let i = 0; i < n - 1; i++) {
            let minIdx = i;

            for (let j = i + 1; j < n; j++) {
                // Compare
                this.core.addStep(() => {
                    this.core.recordComparison();
                    this.core.recordAccess(2);
                    const sorted = Array.from({ length: i }, (_, idx) => idx);
                    this.draw({ comparing: [minIdx, j], sorted });
                });

                if (arr[j] < arr[minIdx]) {
                    minIdx = j;
                }
            }

            // Swap if needed
            if (minIdx !== i) {
                [arr[i], arr[minIdx]] = [arr[minIdx], arr[i]];

                this.core.addStep(() => {
                    this.core.recordSwap();
                    this.array = [...arr];
                    const sorted = Array.from({ length: i }, (_, idx) => idx);
                    this.draw({ swapping: [i, minIdx], sorted });
                });
            }

            // Mark as sorted
            this.core.addStep(() => {
                const sorted = Array.from({ length: i + 1 }, (_, idx) => idx);
                this.draw({ sorted });
            });
        }

        // Final state
        this.core.addStep(() => {
            const sorted = Array.from({ length: n }, (_, idx) => idx);
            this.draw({ sorted });
        });
    }

    /**
     * Insertion Sort
     */
    async insertionSort() {
        const arr = [...this.array];
        const n = arr.length;

        for (let i = 1; i < n; i++) {
            const key = arr[i];
            let j = i - 1;

            // Show key being inserted
            this.core.addStep(() => {
                this.core.recordAccess();
                const sorted = Array.from({ length: i }, (_, idx) => idx);
                this.draw({ comparing: [i], sorted });
            });

            while (j >= 0 && arr[j] > key) {
                // Compare and shift
                this.core.addStep(() => {
                    this.core.recordComparison();
                    this.core.recordAccess(2);
                    const sorted = Array.from({ length: i }, (_, idx) => idx);
                    this.draw({ comparing: [j, j + 1], sorted });
                });

                arr[j + 1] = arr[j];
                j--;

                this.core.addStep(() => {
                    this.array = [...arr];
                    const sorted = Array.from({ length: i }, (_, idx) => idx);
                    this.draw({ sorted });
                });
            }

            arr[j + 1] = key;

            // Mark as sorted
            this.core.addStep(() => {
                this.array = [...arr];
                const sorted = Array.from({ length: i + 1 }, (_, idx) => idx);
                this.draw({ sorted });
            });
        }

        // Final state
        this.core.addStep(() => {
            const sorted = Array.from({ length: n }, (_, idx) => idx);
            this.draw({ sorted });
        });
    }

    /**
     * Merge Sort
     */
    async mergeSort() {
        const arr = [...this.array];
        await this.mergeSortHelper(arr, 0, arr.length - 1);

        // Final state
        this.core.addStep(() => {
            this.array = [...arr];
            const sorted = Array.from({ length: arr.length }, (_, idx) => idx);
            this.draw({ sorted });
        });
    }

    async mergeSortHelper(arr, left, right) {
        if (left >= right) return;

        const mid = Math.floor((left + right) / 2);

        await this.mergeSortHelper(arr, left, mid);
        await this.mergeSortHelper(arr, mid + 1, right);
        await this.merge(arr, left, mid, right);
    }

    async merge(arr, left, mid, right) {
        const leftArr = arr.slice(left, mid + 1);
        const rightArr = arr.slice(mid + 1, right + 1);

        let i = 0, j = 0, k = left;

        while (i < leftArr.length && j < rightArr.length) {
            this.core.addStep(() => {
                this.core.recordComparison();
                this.core.recordAccess(2);
                this.draw({ comparing: [left + i, mid + 1 + j] });
            });

            if (leftArr[i] <= rightArr[j]) {
                arr[k] = leftArr[i];
                i++;
            } else {
                arr[k] = rightArr[j];
                j++;
            }

            this.core.addStep(() => {
                this.array = [...arr];
                this.draw({ swapping: [k] });
            });

            k++;
        }

        while (i < leftArr.length) {
            arr[k] = leftArr[i];
            this.core.addStep(() => {
                this.array = [...arr];
                this.draw({ swapping: [k] });
            });
            i++;
            k++;
        }

        while (j < rightArr.length) {
            arr[k] = rightArr[j];
            this.core.addStep(() => {
                this.array = [...arr];
                this.draw({ swapping: [k] });
            });
            j++;
            k++;
        }
    }

    /**
     * Quick Sort
     */
    async quickSort() {
        const arr = [...this.array];
        await this.quickSortHelper(arr, 0, arr.length - 1);

        // Final state
        this.core.addStep(() => {
            this.array = [...arr];
            const sorted = Array.from({ length: arr.length }, (_, idx) => idx);
            this.draw({ sorted });
        });
    }

    async quickSortHelper(arr, low, high) {
        if (low < high) {
            const pi = await this.partition(arr, low, high);
            await this.quickSortHelper(arr, low, pi - 1);
            await this.quickSortHelper(arr, pi + 1, high);
        }
    }

    async partition(arr, low, high) {
        const pivot = arr[high];
        let i = low - 1;

        // Show pivot
        this.core.addStep(() => {
            this.draw({ pivot: high });
        });

        for (let j = low; j < high; j++) {
            this.core.addStep(() => {
                this.core.recordComparison();
                this.core.recordAccess(2);
                this.draw({ comparing: [j, high], pivot: high });
            });

            if (arr[j] < pivot) {
                i++;
                [arr[i], arr[j]] = [arr[j], arr[i]];

                this.core.addStep(() => {
                    this.core.recordSwap();
                    this.array = [...arr];
                    this.draw({ swapping: [i, j], pivot: high });
                });
            }
        }

        [arr[i + 1], arr[high]] = [arr[high], arr[i + 1]];

        this.core.addStep(() => {
            this.core.recordSwap();
            this.array = [...arr];
            this.draw({ swapping: [i + 1, high] });
        });

        return i + 1;
    }

    /**
     * Heap Sort
     */
    async heapSort() {
        const arr = [...this.array];
        const n = arr.length;

        // Build max heap
        for (let i = Math.floor(n / 2) - 1; i >= 0; i--) {
            await this.heapify(arr, n, i);
        }

        // Extract elements from heap one by one
        for (let i = n - 1; i > 0; i--) {
            [arr[0], arr[i]] = [arr[i], arr[0]];

            this.core.addStep(() => {
                this.core.recordSwap();
                this.array = [...arr];
                const sorted = Array.from({ length: n - i }, (_, idx) => n - 1 - idx);
                this.draw({ swapping: [0, i], sorted });
            });

            await this.heapify(arr, i, 0);
        }

        // Final state
        this.core.addStep(() => {
            this.array = [...arr];
            const sorted = Array.from({ length: n }, (_, idx) => idx);
            this.draw({ sorted });
        });
    }

    async heapify(arr, n, i) {
        let largest = i;
        const left = 2 * i + 1;
        const right = 2 * i + 2;

        if (left < n) {
            this.core.addStep(() => {
                this.core.recordComparison();
                this.core.recordAccess(2);
                this.draw({ comparing: [largest, left] });
            });

            if (arr[left] > arr[largest]) {
                largest = left;
            }
        }

        if (right < n) {
            this.core.addStep(() => {
                this.core.recordComparison();
                this.core.recordAccess(2);
                this.draw({ comparing: [largest, right] });
            });

            if (arr[right] > arr[largest]) {
                largest = right;
            }
        }

        if (largest !== i) {
            [arr[i], arr[largest]] = [arr[largest], arr[i]];

            this.core.addStep(() => {
                this.core.recordSwap();
                this.array = [...arr];
                this.draw({ swapping: [i, largest] });
            });

            await this.heapify(arr, n, largest);
        }
    }
}
