/**
 * Dynamic Programming Visualizer
 * Visualizes DP table filling and memoization for classic DP problems
 */

export class DPVisualizer {
    constructor(canvas, core) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.core = core;

        this.table = [];
        this.problem = 'fibonacci';
        this.inputA = '';
        this.inputB = '';

        this.colors = {
            cell: '#f3f4f6',
            cellComputing: '#f59e0b',
            cellComputed: '#10b981',
            cellUsed: '#3b82f6',
            cellResult: '#ef4444',
            text: '#111827',
            grid: '#e5e7eb'
        };

        this.resize();
    }

    /**
     * Resize canvas
     */
    resize() {
        const container = this.canvas.parentElement;
        const rect = container.getBoundingClientRect();

        this.canvas.width = Math.min(800, rect.width - 32);
        this.canvas.height = 500;

        this.draw();
    }

    /**
     * Start DP problem visualization
     */
    async start(problem) {
        this.problem = problem;
        this.core.reset();

        switch (problem) {
            case 'fibonacci':
                await this.fibonacci(10);
                break;
            case 'knapsack':
                await this.knapsack([2, 3, 4, 5], [3, 4, 5, 6], 8);
                break;
            case 'lcs':
                await this.longestCommonSubsequence('ABCDGH', 'AEDFHR');
                break;
            case 'edit-distance':
                await this.editDistance('SUNDAY', 'SATURDAY');
                break;
            case 'coin-change':
                await this.coinChange([1, 2, 5], 11);
                break;
            default:
                console.error('Unknown DP problem:', problem);
                return;
        }

        this.core.start();
    }

    /**
     * Draw DP table
     */
    draw(highlightStates = {}) {
        const ctx = this.ctx;
        const width = this.canvas.width;
        const height = this.canvas.height;

        // Clear canvas
        ctx.clearRect(0, 0, width, height);

        if (!this.table || this.table.length === 0) {
            ctx.fillStyle = this.colors.text;
            ctx.font = '16px Inter, sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('Select a problem and click Start', width / 2, height / 2);
            return;
        }

        const rows = this.table.length;
        const cols = this.table[0].length;

        // Calculate cell dimensions
        const padding = 40;
        const cellWidth = Math.min(60, (width - 2 * padding) / cols);
        const cellHeight = Math.min(40, (height - 2 * padding - 60) / rows);

        const tableWidth = cellWidth * cols;
        const tableHeight = cellHeight * rows;
        const startX = (width - tableWidth) / 2;
        const startY = 80;

        // Draw title
        ctx.fillStyle = this.colors.text;
        ctx.font = 'bold 20px Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(this.getProblemTitle(), width / 2, 30);

        // Draw input labels if available
        if (this.inputA) {
            ctx.font = '14px monospace';
            ctx.textAlign = 'left';
            ctx.fillText(this.inputA, startX, startY - 10);
        }
        if (this.inputB) {
            ctx.font = '14px monospace';
            ctx.textAlign = 'left';
            ctx.save();
            ctx.translate(startX - 20, startY + 20);
            ctx.rotate(-Math.PI / 2);
            ctx.fillText(this.inputB, 0, 0);
            ctx.restore();
        }

        // Draw cells
        for (let i = 0; i < rows; i++) {
            for (let j = 0; j < cols; j++) {
                const x = startX + j * cellWidth;
                const y = startY + i * cellHeight;
                const value = this.table[i][j];

                // Determine cell color
                let fillColor = this.colors.cell;

                if (highlightStates.result && highlightStates.result.row === i && highlightStates.result.col === j) {
                    fillColor = this.colors.cellResult;
                } else if (highlightStates.computing && highlightStates.computing.row === i && highlightStates.computing.col === j) {
                    fillColor = this.colors.cellComputing;
                } else if (highlightStates.computed && highlightStates.computed.some(cell => cell.row === i && cell.col === j)) {
                    fillColor = this.colors.cellComputed;
                } else if (highlightStates.used && highlightStates.used.some(cell => cell.row === i && cell.col === j)) {
                    fillColor = this.colors.cellUsed;
                }

                // Draw cell background
                ctx.fillStyle = fillColor;
                ctx.fillRect(x, y, cellWidth, cellHeight);

                // Draw cell border
                ctx.strokeStyle = this.colors.grid;
                ctx.lineWidth = 1;
                ctx.strokeRect(x, y, cellWidth, cellHeight);

                // Draw cell value
                if (value !== null && value !== undefined) {
                    ctx.fillStyle = this.colors.text;
                    ctx.font = 'bold 14px monospace';
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillText(
                        typeof value === 'number' ? value.toString() : value,
                        x + cellWidth / 2,
                        y + cellHeight / 2
                    );
                }
            }
        }

        // Draw legend
        this.drawLegend(highlightStates);
    }

    /**
     * Draw legend
     */
    drawLegend(highlightStates) {
        const ctx = this.ctx;
        const legendY = this.canvas.height - 30;
        const legendX = 20;

        const items = [
            { label: 'Computing', color: this.colors.cellComputing },
            { label: 'Computed', color: this.colors.cellComputed },
            { label: 'Result', color: this.colors.cellResult }
        ];

        ctx.font = '12px Inter, sans-serif';
        ctx.textAlign = 'left';

        let x = legendX;
        items.forEach(item => {
            // Draw color box
            ctx.fillStyle = item.color;
            ctx.fillRect(x, legendY, 15, 15);
            ctx.strokeStyle = this.colors.grid;
            ctx.strokeRect(x, legendY, 15, 15);

            // Draw label
            ctx.fillStyle = this.colors.text;
            ctx.fillText(item.label, x + 20, legendY + 12);

            x += 120;
        });
    }

    /**
     * Get problem title
     */
    getProblemTitle() {
        const titles = {
            fibonacci: 'Fibonacci Sequence',
            knapsack: '0/1 Knapsack Problem',
            lcs: 'Longest Common Subsequence',
            'edit-distance': 'Edit Distance (Levenshtein)',
            'coin-change': 'Coin Change Problem'
        };
        return titles[this.problem] || this.problem;
    }

    /**
     * Fibonacci with DP
     */
    async fibonacci(n) {
        this.inputA = `Computing Fibonacci(${n})`;
        this.inputB = '';

        // Initialize 1D table
        this.table = [new Array(n + 1).fill(null)];

        // Base cases
        this.table[0][0] = 0;
        this.table[0][1] = 1;

        this.core.addStep(() => {
            const computed = [{ row: 0, col: 0 }, { row: 0, col: 1 }];
            this.draw({ computed });
        });

        // Fill table
        for (let i = 2; i <= n; i++) {
            this.core.addStep(() => {
                this.core.recordAccess(2);
                const used = [{ row: 0, col: i - 1 }, { row: 0, col: i - 2 }];
                this.draw({ computing: { row: 0, col: i }, used });
            });

            this.table[0][i] = this.table[0][i - 1] + this.table[0][i - 2];

            this.core.addStep(() => {
                const computed = [];
                for (let j = 0; j <= i; j++) {
                    computed.push({ row: 0, col: j });
                }
                this.draw({ computed, result: { row: 0, col: i } });
            });
        }

        // Final result
        this.core.addStep(() => {
            const computed = [];
            for (let j = 0; j <= n; j++) {
                computed.push({ row: 0, col: j });
            }
            this.draw({ computed, result: { row: 0, col: n } });
        });
    }

    /**
     * 0/1 Knapsack Problem
     */
    async knapsack(weights, values, capacity) {
        const n = weights.length;
        this.inputA = `Values: [${values.join(', ')}]  Weights: [${weights.join(', ')}]  Capacity: ${capacity}`;
        this.inputB = '';

        // Initialize table: rows = items, cols = capacity
        this.table = Array(n + 1).fill(null).map(() => Array(capacity + 1).fill(0));

        // Fill table
        for (let i = 1; i <= n; i++) {
            for (let w = 0; w <= capacity; w++) {
                this.core.addStep(() => {
                    this.core.recordAccess();
                    this.draw({ computing: { row: i, col: w } });
                });

                if (weights[i - 1] <= w) {
                    this.table[i][w] = Math.max(
                        values[i - 1] + this.table[i - 1][w - weights[i - 1]],
                        this.table[i - 1][w]
                    );
                } else {
                    this.table[i][w] = this.table[i - 1][w];
                }

                this.core.addStep(() => {
                    const computed = [];
                    for (let ii = 0; ii <= i; ii++) {
                        for (let jj = 0; jj <= (ii === i ? w : capacity); jj++) {
                            computed.push({ row: ii, col: jj });
                        }
                    }
                    this.draw({ computed });
                });
            }
        }

        // Final result
        this.core.addStep(() => {
            const computed = [];
            for (let i = 0; i <= n; i++) {
                for (let j = 0; j <= capacity; j++) {
                    computed.push({ row: i, col: j });
                }
            }
            this.draw({ computed, result: { row: n, col: capacity } });
        });
    }

    /**
     * Longest Common Subsequence
     */
    async longestCommonSubsequence(str1, str2) {
        const m = str1.length;
        const n = str2.length;

        this.inputA = `  ${str1.split('').join('  ')}`;
        this.inputB = `  ${str2.split('').join('  ')}`;

        // Initialize table
        this.table = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));

        // Fill table
        for (let i = 1; i <= m; i++) {
            for (let j = 1; j <= n; j++) {
                this.core.addStep(() => {
                    this.core.recordAccess();
                    this.core.recordComparison();
                    this.draw({ computing: { row: i, col: j } });
                });

                if (str1[i - 1] === str2[j - 1]) {
                    this.table[i][j] = this.table[i - 1][j - 1] + 1;
                } else {
                    this.table[i][j] = Math.max(this.table[i - 1][j], this.table[i][j - 1]);
                }

                this.core.addStep(() => {
                    const computed = [];
                    for (let ii = 0; ii <= i; ii++) {
                        for (let jj = 0; jj <= (ii === i ? j : n); jj++) {
                            computed.push({ row: ii, col: jj });
                        }
                    }
                    this.draw({ computed });
                });
            }
        }

        // Final result
        this.core.addStep(() => {
            const computed = [];
            for (let i = 0; i <= m; i++) {
                for (let j = 0; j <= n; j++) {
                    computed.push({ row: i, col: j });
                }
            }
            this.draw({ computed, result: { row: m, col: n } });
        });
    }

    /**
     * Edit Distance (Levenshtein Distance)
     */
    async editDistance(str1, str2) {
        const m = str1.length;
        const n = str2.length;

        this.inputA = `  ${str1.split('').join('  ')}`;
        this.inputB = `  ${str2.split('').join('  ')}`;

        // Initialize table
        this.table = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));

        // Initialize first row and column
        for (let i = 0; i <= m; i++) this.table[i][0] = i;
        for (let j = 0; j <= n; j++) this.table[0][j] = j;

        // Fill table
        for (let i = 1; i <= m; i++) {
            for (let j = 1; j <= n; j++) {
                this.core.addStep(() => {
                    this.core.recordAccess();
                    this.core.recordComparison();
                    this.draw({ computing: { row: i, col: j } });
                });

                if (str1[i - 1] === str2[j - 1]) {
                    this.table[i][j] = this.table[i - 1][j - 1];
                } else {
                    this.table[i][j] = 1 + Math.min(
                        this.table[i - 1][j],     // Delete
                        this.table[i][j - 1],     // Insert
                        this.table[i - 1][j - 1]  // Replace
                    );
                }

                this.core.addStep(() => {
                    const computed = [];
                    for (let ii = 0; ii <= i; ii++) {
                        for (let jj = 0; jj <= (ii === i ? j : n); jj++) {
                            computed.push({ row: ii, col: jj });
                        }
                    }
                    this.draw({ computed });
                });
            }
        }

        // Final result
        this.core.addStep(() => {
            const computed = [];
            for (let i = 0; i <= m; i++) {
                for (let j = 0; j <= n; j++) {
                    computed.push({ row: i, col: j });
                }
            }
            this.draw({ computed, result: { row: m, col: n } });
        });
    }

    /**
     * Coin Change Problem
     */
    async coinChange(coins, amount) {
        const n = coins.length;
        this.inputA = `Coins: [${coins.join(', ')}]  Amount: ${amount}`;
        this.inputB = '';

        // Initialize table
        this.table = Array(n + 1).fill(null).map(() => Array(amount + 1).fill(Infinity));

        // Base case: 0 amount needs 0 coins
        for (let i = 0; i <= n; i++) {
            this.table[i][0] = 0;
        }

        // Fill table
        for (let i = 1; i <= n; i++) {
            for (let j = 1; j <= amount; j++) {
                this.core.addStep(() => {
                    this.core.recordAccess();
                    this.draw({ computing: { row: i, col: j } });
                });

                // Don't take current coin
                this.table[i][j] = this.table[i - 1][j];

                // Take current coin if possible
                if (j >= coins[i - 1]) {
                    const take = this.table[i][j - coins[i - 1]];
                    if (take !== Infinity) {
                        this.table[i][j] = Math.min(this.table[i][j], take + 1);
                    }
                }

                this.core.addStep(() => {
                    const computed = [];
                    for (let ii = 0; ii <= i; ii++) {
                        for (let jj = 0; jj <= (ii === i ? j : amount); jj++) {
                            computed.push({ row: ii, col: jj });
                        }
                    }
                    this.draw({ computed });
                });
            }
        }

        // Final result
        this.core.addStep(() => {
            const computed = [];
            for (let i = 0; i <= n; i++) {
                for (let j = 0; j <= amount; j++) {
                    computed.push({ row: i, col: j });
                }
            }
            const result = this.table[n][amount] === Infinity ? 'No solution' : this.table[n][amount];
            if (this.table[n][amount] !== Infinity) {
                this.draw({ computed, result: { row: n, col: amount } });
            } else {
                this.draw({ computed });
            }
        });
    }

    /**
     * Reset visualization
     */
    reset() {
        this.core.reset();
        this.table = [];
        this.inputA = '';
        this.inputB = '';
        this.draw();
    }

    /**
     * Pause visualization
     */
    pause() {
        this.core.pause();
    }
}
