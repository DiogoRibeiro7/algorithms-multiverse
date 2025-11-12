/**
 * Algorithm Visualizer - Main Entry Point
 * Coordinates all visualizations and manages application state
 */

import { VisualizerCore } from './VisualizerCore.js';
import { SortingVisualizer } from '../algorithms/SortingVisualizer.js';
import { TreeVisualizer } from '../algorithms/TreeVisualizer.js';
import { GraphVisualizer } from '../algorithms/GraphVisualizer.js';
import { SearchVisualizer } from '../algorithms/SearchVisualizer.js';
import { DPVisualizer } from '../algorithms/DPVisualizer.js';
import { ComparisonManager } from './ComparisonManager.js';
import { ThemeManager } from './ThemeManager.js';
import { UIController } from './UIController.js';

/**
 * Main Application Class
 */
class AlgorithmVisualizer {
    constructor() {
        this.core = new VisualizerCore();
        this.visualizers = {};
        this.currentSection = 'sorting';
        this.themeManager = new ThemeManager();
        this.uiController = new UIController();

        this.init();
    }

    /**
     * Initialize the application
     */
    init() {
        console.log('🚀 Initializing Algorithm Visualizer...');

        // Initialize visualizers
        this.initVisualizers();

        // Setup event listeners
        this.setupEventListeners();

        // Initialize theme
        this.themeManager.init();

        // Initialize UI
        this.uiController.init();

        console.log('✅ Algorithm Visualizer ready!');
    }

    /**
     * Initialize all visualizers
     */
    initVisualizers() {
        try {
            // Sorting visualizer
            const sortCanvas = document.getElementById('sort-canvas');
            if (sortCanvas) {
                this.visualizers.sorting = new SortingVisualizer(sortCanvas, this.core);
                console.log('✓ Sorting visualizer initialized');
            }

            // Tree visualizer
            const treeSvg = document.getElementById('tree-svg');
            if (treeSvg) {
                this.visualizers.tree = new TreeVisualizer(treeSvg, this.core);
                console.log('✓ Tree visualizer initialized');
            }

            // Graph visualizer
            const graphSvg = document.getElementById('graph-svg');
            if (graphSvg) {
                this.visualizers.graph = new GraphVisualizer(graphSvg, this.core);
                console.log('✓ Graph visualizer initialized');
            }

            // Search visualizer
            const searchCanvas = document.getElementById('search-canvas');
            if (searchCanvas) {
                this.visualizers.search = new SearchVisualizer(searchCanvas, this.core);
                console.log('✓ Search visualizer initialized');
            }

            // DP visualizer
            const dpCanvas = document.getElementById('dp-canvas');
            if (dpCanvas) {
                this.visualizers.dp = new DPVisualizer(dpCanvas, this.core);
                console.log('✓ DP visualizer initialized');
            }

            // Comparison manager
            this.comparisonManager = new ComparisonManager(this.core);
            console.log('✓ Comparison manager initialized');

        } catch (error) {
            console.error('Error initializing visualizers:', error);
        }
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.handleNavigation(e));
        });

        // Theme toggle
        const themeToggle = document.querySelector('.theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                this.themeManager.toggle();
            });
        }

        // Sorting controls
        this.setupSortingControls();

        // Tree controls
        this.setupTreeControls();

        // Graph controls
        this.setupGraphControls();

        // Search controls
        this.setupSearchControls();

        // DP controls
        this.setupDPControls();

        // Comparison controls
        this.setupComparisonControls();

        // Window resize
        window.addEventListener('resize', () => this.handleResize());
    }

    /**
     * Handle navigation between sections
     */
    handleNavigation(e) {
        const section = e.target.dataset.section;
        if (!section) return;

        // Update active nav button
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        e.target.classList.add('active');

        // Show corresponding section
        document.querySelectorAll('.content-section').forEach(sec => {
            sec.classList.remove('active');
        });

        const targetSection = document.getElementById(`${section}-section`);
        if (targetSection) {
            targetSection.classList.add('active');
            this.currentSection = section;

            // Trigger resize to adjust canvas/svg
            setTimeout(() => this.handleResize(), 100);
        }
    }

    /**
     * Setup sorting controls
     */
    setupSortingControls() {
        const startBtn = document.getElementById('start-btn');
        const pauseBtn = document.getElementById('pause-btn');
        const resetBtn = document.getElementById('reset-btn');
        const algorithmSelect = document.getElementById('sort-algorithm');
        const arraySizeSlider = document.getElementById('array-size');
        const speedSlider = document.getElementById('speed');

        if (startBtn) {
            startBtn.addEventListener('click', () => {
                if (this.visualizers.sorting) {
                    const algorithm = algorithmSelect?.value || 'bubble';
                    this.visualizers.sorting.start(algorithm);
                    this.uiController.updateButtonStates('sorting', 'running');
                }
            });
        }

        if (pauseBtn) {
            pauseBtn.addEventListener('click', () => {
                if (this.visualizers.sorting) {
                    this.visualizers.sorting.pause();
                    this.uiController.updateButtonStates('sorting', 'paused');
                }
            });
        }

        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                if (this.visualizers.sorting) {
                    this.visualizers.sorting.reset();
                    this.uiController.updateButtonStates('sorting', 'idle');
                }
            });
        }

        if (algorithmSelect) {
            algorithmSelect.addEventListener('change', () => {
                this.uiController.updateAlgorithmInfo(algorithmSelect.value);
            });
        }

        if (arraySizeSlider) {
            arraySizeSlider.addEventListener('input', (e) => {
                document.getElementById('array-size-value').textContent = e.target.value;
                if (this.visualizers.sorting) {
                    this.visualizers.sorting.setArraySize(parseInt(e.target.value));
                }
            });
        }

        if (speedSlider) {
            speedSlider.addEventListener('input', (e) => {
                const speed = parseInt(e.target.value);
                document.getElementById('speed-value').textContent = `${speed}x`;
                if (this.visualizers.sorting) {
                    this.visualizers.sorting.setSpeed(speed);
                }
            });
        }

        // Data generation buttons
        document.querySelectorAll('[data-action]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const action = e.target.dataset.action;
                if (this.visualizers.sorting) {
                    this.visualizers.sorting.generateData(action);
                }
            });
        });
    }

    /**
     * Setup tree controls
     */
    setupTreeControls() {
        const startBtn = document.getElementById('tree-start-btn');
        const resetBtn = document.getElementById('tree-reset-btn');
        const treeTypeSelect = document.getElementById('tree-type');

        if (startBtn) {
            startBtn.addEventListener('click', () => {
                if (this.visualizers.tree) {
                    const algorithm = document.getElementById('tree-algorithm')?.value || 'inorder';
                    this.visualizers.tree.start(algorithm);
                }
            });
        }

        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                if (this.visualizers.tree) {
                    this.visualizers.tree.reset();
                }
            });
        }

        if (treeTypeSelect) {
            treeTypeSelect.addEventListener('change', (e) => {
                if (this.visualizers.tree) {
                    this.visualizers.tree.setTreeType(e.target.value);
                }
            });
        }
    }

    /**
     * Setup graph controls
     */
    setupGraphControls() {
        const startBtn = document.getElementById('graph-start-btn');
        const resetBtn = document.getElementById('graph-reset-btn');

        if (startBtn) {
            startBtn.addEventListener('click', () => {
                if (this.visualizers.graph) {
                    const algorithm = document.getElementById('graph-algorithm')?.value || 'bfs';
                    this.visualizers.graph.start(algorithm);
                }
            });
        }

        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                if (this.visualizers.graph) {
                    this.visualizers.graph.reset();
                }
            });
        }

        // Graph generation buttons
        document.querySelectorAll('[data-graph]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const type = e.target.dataset.graph;
                if (this.visualizers.graph) {
                    this.visualizers.graph.generateGraph(type);
                }
            });
        });
    }

    /**
     * Setup search controls
     */
    setupSearchControls() {
        const startBtn = document.getElementById('search-start-btn');
        const resetBtn = document.getElementById('search-reset-btn');

        if (startBtn) {
            startBtn.addEventListener('click', () => {
                if (this.visualizers.search) {
                    const algorithm = document.getElementById('search-algorithm')?.value || 'linear';
                    const target = parseInt(document.getElementById('search-target')?.value) || 50;
                    this.visualizers.search.start(algorithm, target);
                }
            });
        }

        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                if (this.visualizers.search) {
                    this.visualizers.search.reset();
                }
            });
        }
    }

    /**
     * Setup DP controls
     */
    setupDPControls() {
        const startBtn = document.getElementById('dp-start-btn');
        const resetBtn = document.getElementById('dp-reset-btn');

        if (startBtn) {
            startBtn.addEventListener('click', () => {
                if (this.visualizers.dp) {
                    const problem = document.getElementById('dp-algorithm')?.value || 'fibonacci';
                    this.visualizers.dp.start(problem);
                }
            });
        }

        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                if (this.visualizers.dp) {
                    this.visualizers.dp.reset();
                }
            });
        }
    }

    /**
     * Setup comparison controls
     */
    setupComparisonControls() {
        const startBtn = document.getElementById('compare-start-btn');

        if (startBtn) {
            startBtn.addEventListener('click', () => {
                const selectedAlgorithms = [];
                document.querySelectorAll('#compare-section input[type="checkbox"]:checked').forEach(checkbox => {
                    selectedAlgorithms.push(checkbox.value);
                });

                if (selectedAlgorithms.length > 0 && this.comparisonManager) {
                    this.comparisonManager.compare(selectedAlgorithms);
                }
            });
        }
    }

    /**
     * Handle window resize
     */
    handleResize() {
        // Resize canvases
        Object.values(this.visualizers).forEach(visualizer => {
            if (visualizer && typeof visualizer.resize === 'function') {
                visualizer.resize();
            }
        });
    }
}

// Initialize the application when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.algorithmVisualizer = new AlgorithmVisualizer();
    });
} else {
    window.algorithmVisualizer = new AlgorithmVisualizer();
}

export { AlgorithmVisualizer };
