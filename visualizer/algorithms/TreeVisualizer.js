/**
 * Tree Visualizer
 * Handles tree traversal visualizations with interactive SVG rendering
 */

export class TreeVisualizer {
    constructor(svg, core) {
        this.svg = svg;
        this.core = core;
        this.tree = null;
        this.treeType = 'bst';

        this.colors = {
            default: '#3b82f6',
            visiting: '#f59e0b',
            visited: '#10b981',
            current: '#ef4444',
            edge: '#9ca3af'
        };

        this.initializeTree();
        console.log('✓ Tree visualizer initialized');
    }

    /**
     * Tree Node class
     */
    createNode(value, x = 0, y = 0) {
        return {
            value,
            x,
            y,
            left: null,
            right: null
        };
    }

    /**
     * Initialize tree with sample data
     */
    initializeTree() {
        this.generateTree(this.treeType);
    }

    /**
     * Generate different tree types
     */
    generateTree(type) {
        this.treeType = type;

        switch (type) {
            case 'bst':
                this.tree = this.generateBST();
                break;
            case 'complete':
                this.tree = this.generateCompleteTree();
                break;
            case 'balanced':
                this.tree = this.generateBalancedTree();
                break;
            default:
                this.tree = this.generateBST();
        }

        this.calculatePositions();
        this.draw();
    }

    /**
     * Generate Binary Search Tree
     */
    generateBST() {
        const values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45];
        let root = null;

        const insertBST = (node, value) => {
            if (!node) {
                return this.createNode(value);
            }

            if (value < node.value) {
                node.left = insertBST(node.left, value);
            } else {
                node.right = insertBST(node.right, value);
            }

            return node;
        };

        values.forEach(val => {
            root = insertBST(root, val);
        });

        return root;
    }

    /**
     * Generate Complete Binary Tree
     */
    generateCompleteTree() {
        const values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65];

        if (values.length === 0) return null;

        const buildComplete = (arr, index) => {
            if (index >= arr.length) return null;

            const node = this.createNode(arr[index]);
            node.left = buildComplete(arr, 2 * index + 1);
            node.right = buildComplete(arr, 2 * index + 2);

            return node;
        };

        return buildComplete(values, 0);
    }

    /**
     * Generate Balanced Tree
     */
    generateBalancedTree() {
        const values = [10, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 80];

        const buildBalanced = (arr, start, end) => {
            if (start > end) return null;

            const mid = Math.floor((start + end) / 2);
            const node = this.createNode(arr[mid]);

            node.left = buildBalanced(arr, start, mid - 1);
            node.right = buildBalanced(arr, mid + 1, end);

            return node;
        };

        return buildBalanced(values, 0, values.length - 1);
    }

    /**
     * Calculate node positions using recursive layout
     */
    calculatePositions() {
        if (!this.tree) return;

        const width = parseInt(this.svg.getAttribute('width')) || 800;
        const height = parseInt(this.svg.getAttribute('height')) || 500;

        const assignPositions = (node, x, y, xOffset, level) => {
            if (!node) return;

            node.x = x;
            node.y = y;

            const nextY = y + 80;
            const nextOffset = xOffset / 2;

            if (node.left) {
                assignPositions(node.left, x - xOffset, nextY, nextOffset, level + 1);
            }

            if (node.right) {
                assignPositions(node.right, x + xOffset, nextY, nextOffset, level + 1);
            }
        };

        assignPositions(this.tree, width / 2, 50, width / 4, 0);
    }

    /**
     * Draw tree
     */
    draw(highlightStates = {}) {
        // Clear SVG
        this.svg.innerHTML = '';

        if (!this.tree) return;

        // Create definitions for arrowheads
        const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
        defs.innerHTML = `
            <marker id="arrowhead" markerWidth="10" markerHeight="10"
                    refX="9" refY="3" orient="auto">
                <polygon points="0 0, 10 3, 0 6" fill="${this.colors.edge}" />
            </marker>
        `;
        this.svg.appendChild(defs);

        // Draw edges first (so they appear behind nodes)
        this.drawEdges(this.tree);

        // Draw nodes
        this.drawNodes(this.tree, highlightStates);
    }

    /**
     * Draw edges recursively
     */
    drawEdges(node) {
        if (!node) return;

        // Draw edge to left child
        if (node.left) {
            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            line.setAttribute('x1', node.x);
            line.setAttribute('y1', node.y);
            line.setAttribute('x2', node.left.x);
            line.setAttribute('y2', node.left.y);
            line.setAttribute('stroke', this.colors.edge);
            line.setAttribute('stroke-width', '2');
            line.setAttribute('class', 'tree-edge');
            this.svg.appendChild(line);

            this.drawEdges(node.left);
        }

        // Draw edge to right child
        if (node.right) {
            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            line.setAttribute('x1', node.x);
            line.setAttribute('y1', node.y);
            line.setAttribute('x2', node.right.x);
            line.setAttribute('y2', node.right.y);
            line.setAttribute('stroke', this.colors.edge);
            line.setAttribute('stroke-width', '2');
            line.setAttribute('class', 'tree-edge');
            this.svg.appendChild(line);

            this.drawEdges(node.right);
        }
    }

    /**
     * Draw nodes recursively
     */
    drawNodes(node, highlightStates = {}) {
        if (!node) return;

        // Recursively draw children first
        if (node.left) this.drawNodes(node.left, highlightStates);
        if (node.right) this.drawNodes(node.right, highlightStates);

        // Determine color
        let color = this.colors.default;
        if (highlightStates.current === node.value) {
            color = this.colors.current;
        } else if (highlightStates.visiting && highlightStates.visiting.includes(node.value)) {
            color = this.colors.visiting;
        } else if (highlightStates.visited && highlightStates.visited.includes(node.value)) {
            color = this.colors.visited;
        }

        // Create node group
        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        g.setAttribute('class', 'tree-node');

        // Draw circle
        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circle.setAttribute('cx', node.x);
        circle.setAttribute('cy', node.y);
        circle.setAttribute('r', '25');
        circle.setAttribute('fill', color);
        circle.setAttribute('stroke', '#ffffff');
        circle.setAttribute('stroke-width', '3');

        // Draw text
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', node.x);
        text.setAttribute('y', node.y);
        text.setAttribute('text-anchor', 'middle');
        text.setAttribute('dominant-baseline', 'middle');
        text.setAttribute('fill', '#ffffff');
        text.setAttribute('font-size', '16');
        text.setAttribute('font-weight', 'bold');
        text.textContent = node.value;

        g.appendChild(circle);
        g.appendChild(text);
        this.svg.appendChild(g);
    }

    /**
     * Start traversal visualization
     */
    async start(algorithm) {
        this.core.reset();

        switch (algorithm) {
            case 'inorder':
                await this.inorderTraversal();
                break;
            case 'preorder':
                await this.preorderTraversal();
                break;
            case 'postorder':
                await this.postorderTraversal();
                break;
            case 'levelorder':
                await this.levelorderTraversal();
                break;
            default:
                console.error('Unknown traversal:', algorithm);
                return;
        }

        this.core.start();
    }

    /**
     * In-order traversal (Left, Root, Right)
     */
    async inorderTraversal() {
        const visited = [];

        const traverse = (node) => {
            if (!node) return;

            // Visit left
            traverse(node.left);

            // Visit current
            this.core.addStep(() => {
                this.core.recordAccess();
                visited.push(node.value);
                this.draw({ current: node.value, visited: [...visited] });
            });

            // Visit right
            traverse(node.right);
        };

        traverse(this.tree);

        // Final state
        this.core.addStep(() => {
            this.draw({ visited: [...visited] });
        });
    }

    /**
     * Pre-order traversal (Root, Left, Right)
     */
    async preorderTraversal() {
        const visited = [];

        const traverse = (node) => {
            if (!node) return;

            // Visit current first
            this.core.addStep(() => {
                this.core.recordAccess();
                visited.push(node.value);
                this.draw({ current: node.value, visited: [...visited] });
            });

            // Visit left
            traverse(node.left);

            // Visit right
            traverse(node.right);
        };

        traverse(this.tree);

        // Final state
        this.core.addStep(() => {
            this.draw({ visited: [...visited] });
        });
    }

    /**
     * Post-order traversal (Left, Right, Root)
     */
    async postorderTraversal() {
        const visited = [];

        const traverse = (node) => {
            if (!node) return;

            // Visit left
            traverse(node.left);

            // Visit right
            traverse(node.right);

            // Visit current last
            this.core.addStep(() => {
                this.core.recordAccess();
                visited.push(node.value);
                this.draw({ current: node.value, visited: [...visited] });
            });
        };

        traverse(this.tree);

        // Final state
        this.core.addStep(() => {
            this.draw({ visited: [...visited] });
        });
    }

    /**
     * Level-order traversal (Breadth-First Search)
     */
    async levelorderTraversal() {
        if (!this.tree) return;

        const visited = [];
        const queue = [this.tree];

        while (queue.length > 0) {
            const node = queue.shift();

            this.core.addStep(() => {
                this.core.recordAccess();
                visited.push(node.value);
                this.draw({ current: node.value, visited: [...visited] });
            });

            if (node.left) queue.push(node.left);
            if (node.right) queue.push(node.right);
        }

        // Final state
        this.core.addStep(() => {
            this.draw({ visited: [...visited] });
        });
    }

    /**
     * Reset visualization
     */
    reset() {
        this.core.reset();
        this.generateTree(this.treeType);
    }

    /**
     * Change tree type
     */
    setTreeType(type) {
        this.generateTree(type);
    }

    /**
     * Resize handler
     */
    resize() {
        this.calculatePositions();
        this.draw();
    }
}
