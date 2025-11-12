/**
 * UI Controller - Manages UI state and interactions
 */

export class UIController {
    constructor() {
        this.algorithmDescriptions = {
            bubble: {
                title: 'Bubble Sort',
                description: 'Repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order.',
                complexity: {
                    time: 'O(n²)',
                    space: 'O(1)',
                    stable: 'Yes'
                }
            },
            selection: {
                title: 'Selection Sort',
                description: 'Divides the input into sorted and unsorted regions, repeatedly selecting the smallest element.',
                complexity: {
                    time: 'O(n²)',
                    space: 'O(1)',
                    stable: 'No'
                }
            },
            insertion: {
                title: 'Insertion Sort',
                description: 'Builds the final sorted array one item at a time, inserting each element into its correct position.',
                complexity: {
                    time: 'O(n²)',
                    space: 'O(1)',
                    stable: 'Yes'
                }
            },
            merge: {
                title: 'Merge Sort',
                description: 'Divide and conquer algorithm that divides the array into halves, sorts them, and merges them back.',
                complexity: {
                    time: 'O(n log n)',
                    space: 'O(n)',
                    stable: 'Yes'
                }
            },
            quick: {
                title: 'Quick Sort',
                description: 'Divide and conquer algorithm that picks a pivot and partitions the array around it.',
                complexity: {
                    time: 'O(n log n)',
                    space: 'O(log n)',
                    stable: 'No'
                }
            },
            heap: {
                title: 'Heap Sort',
                description: 'Uses a binary heap data structure, building a max heap and extracting elements one by one.',
                complexity: {
                    time: 'O(n log n)',
                    space: 'O(1)',
                    stable: 'No'
                }
            }
        };
    }

    /**
     * Initialize UI controller
     */
    init() {
        console.log('✓ UI Controller initialized');
    }

    /**
     * Update button states based on visualization state
     */
    updateButtonStates(section, state) {
        const startBtn = document.getElementById(`${section === 'sorting' ? '' : section + '-'}start-btn`);
        const pauseBtn = document.getElementById(`${section === 'sorting' ? '' : section + '-'}pause-btn`);
        const resetBtn = document.getElementById(`${section === 'sorting' ? '' : section + '-'}reset-btn`);

        switch (state) {
            case 'running':
                if (startBtn) {
                    startBtn.disabled = true;
                    startBtn.textContent = 'Running...';
                }
                if (pauseBtn) {
                    pauseBtn.disabled = false;
                    pauseBtn.innerHTML = `
                        <svg class="btn-icon" viewBox="0 0 24 24" fill="currentColor">
                            <rect x="6" y="4" width="4" height="16"/>
                            <rect x="14" y="4" width="4" height="16"/>
                        </svg>
                        Pause
                    `;
                }
                break;

            case 'paused':
                if (pauseBtn) {
                    pauseBtn.innerHTML = `
                        <svg class="btn-icon" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M8 5v14l11-7z"/>
                        </svg>
                        Resume
                    `;
                }
                break;

            case 'idle':
                if (startBtn) {
                    startBtn.disabled = false;
                    startBtn.innerHTML = `
                        <svg class="btn-icon" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M8 5v14l11-7z"/>
                        </svg>
                        Start
                    `;
                }
                if (pauseBtn) {
                    pauseBtn.disabled = true;
                }
                break;
        }
    }

    /**
     * Update algorithm information display
     */
    updateAlgorithmInfo(algorithmName) {
        const infoContainer = document.getElementById('algorithm-description');
        const complexityEl = document.getElementById('complexity');

        if (!infoContainer) return;

        const info = this.algorithmDescriptions[algorithmName];
        if (!info) return;

        infoContainer.innerHTML = `
            <p><strong>${info.title}</strong></p>
            <p>${info.description}</p>
            <ul>
                <li>Time: ${info.complexity.time}</li>
                <li>Space: ${info.complexity.space}</li>
                <li>Stable: ${info.complexity.stable}</li>
            </ul>
        `;

        if (complexityEl) {
            complexityEl.textContent = info.complexity.time;
        }
    }

    /**
     * Show notification
     */
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;

        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => notification.classList.add('show'), 100);

        // Remove after 3 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    /**
     * Show loading state
     */
    showLoading(container) {
        const overlay = document.createElement('div');
        overlay.className = 'loading-overlay';
        overlay.innerHTML = '<div class="loading-spinner"></div>';

        container.appendChild(overlay);
        return overlay;
    }

    /**
     * Hide loading state
     */
    hideLoading(overlay) {
        if (overlay && overlay.parentElement) {
            overlay.remove();
        }
    }
}
