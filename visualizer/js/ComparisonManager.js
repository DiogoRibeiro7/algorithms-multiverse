/**
 * Comparison Manager - Handles side-by-side algorithm comparison
 */

export class ComparisonManager {
    constructor(core) {
        this.core = core;
        this.results = [];
    }

    /**
     * Compare multiple algorithms
     */
    async compare(algorithms) {
        console.log('🔬 Comparing algorithms:', algorithms);

        const grid = document.getElementById('comparison-grid');
        if (!grid) return;

        // Clear previous results
        grid.innerHTML = '';
        this.results = [];

        // Generate test data
        const testData = this.core.generateRandomArray(50);

        // Create comparison items for each algorithm
        algorithms.forEach(algo => {
            const item = this.createComparisonItem(algo);
            grid.appendChild(item);
        });

        // Run algorithms and collect results
        for (const algo of algorithms) {
            await this.runAlgorithm(algo, [...testData]);
        }

        // Display comparison chart
        this.displayComparisonChart();
    }

    /**
     * Create comparison item HTML
     */
    createComparisonItem(algorithmName) {
        const item = document.createElement('div');
        item.className = 'comparison-item';
        item.id = `comparison-${algorithmName}`;

        item.innerHTML = `
            <div class="comparison-item-header">
                <h3>${this.getAlgorithmTitle(algorithmName)}</h3>
                <span class="comparison-status pending">Pending</span>
            </div>
            <canvas class="comparison-canvas" width="350" height="200"></canvas>
            <div class="comparison-stats">
                <div class="comparison-stat">
                    <div class="comparison-stat-label">Time</div>
                    <div class="comparison-stat-value" id="${algorithmName}-time">-</div>
                </div>
                <div class="comparison-stat">
                    <div class="comparison-stat-label">Comparisons</div>
                    <div class="comparison-stat-value" id="${algorithmName}-comparisons">-</div>
                </div>
            </div>
        `;

        return item;
    }

    /**
     * Run algorithm and collect metrics
     */
    async runAlgorithm(algorithmName, data) {
        const status = document.querySelector(`#comparison-${algorithmName} .comparison-status`);
        if (status) status.textContent = 'Running';
        if (status) status.className = 'comparison-status running';

        const startTime = performance.now();
        let comparisons = 0;

        // Simple sorting simulation (replace with actual visualizer logic)
        const sorted = data.sort((a, b) => {
            comparisons++;
            return a - b;
        });

        const elapsed = performance.now() - startTime;

        // Update display
        document.getElementById(`${algorithmName}-time`).textContent = `${elapsed.toFixed(2)}ms`;
        document.getElementById(`${algorithmName}-comparisons`).textContent = comparisons;

        if (status) status.textContent = 'Completed';
        if (status) status.className = 'comparison-status completed';

        // Store results
        this.results.push({
            algorithm: algorithmName,
            time: elapsed,
            comparisons: comparisons
        });
    }

    /**
     * Display comparison chart
     */
    displayComparisonChart() {
        console.log('📊 Displaying comparison chart', this.results);
        // This would use a charting library like Chart.js in a full implementation
    }

    /**
     * Get algorithm title
     */
    getAlgorithmTitle(name) {
        const titles = {
            bubble: 'Bubble Sort',
            insertion: 'Insertion Sort',
            selection: 'Selection Sort',
            merge: 'Merge Sort',
            quick: 'Quick Sort',
            heap: 'Heap Sort'
        };
        return titles[name] || name;
    }
}
