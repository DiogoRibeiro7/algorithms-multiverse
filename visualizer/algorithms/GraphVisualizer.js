/**
 * Graph Visualizer
 * Handles graph algorithm visualizations (BFS, DFS, Dijkstra, A*, Prim, Kruskal)
 */

export class GraphVisualizer {
    constructor(svg, core) {
        this.svg = svg;
        this.core = core;
        this.graph = null;
        this.graphType = 'random';

        this.colors = {
            node: '#3b82f6',
            nodeVisited: '#10b981',
            nodeCurrent: '#ef4444',
            nodeQueue: '#f59e0b',
            edge: '#9ca3af',
            edgeActive: '#3b82f6',
            edgeVisited: '#10b981',
            edgePath: '#ef4444'
        };

        this.generateGraph(this.graphType);
        console.log('✓ Graph visualizer initialized');
    }

    /**
     * Generate different types of graphs
     */
    generateGraph(type) {
        this.graphType = type;

        switch (type) {
            case 'random':
                this.graph = this.generateRandomGraph(12, 0.25);
                break;
            case 'grid':
                this.graph = this.generateGridGraph(4, 4);
                break;
            case 'tree':
                this.graph = this.generateTreeGraph(15);
                break;
            default:
                this.graph = this.generateRandomGraph(12, 0.25);
        }

        this.calculateNodePositions();
        this.draw();
    }

    /**
     * Generate random graph
     */
    generateRandomGraph(nodeCount, density) {
        const nodes = [];
        const edges = [];

        // Create nodes
        for (let i = 0; i < nodeCount; i++) {
            nodes.push({
                id: i,
                label: i.toString(),
                x: 0,
                y: 0
            });
        }

        // Create edges with random weights
        for (let i = 0; i < nodeCount; i++) {
            for (let j = i + 1; j < nodeCount; j++) {
                if (Math.random() < density) {
                    const weight = Math.floor(Math.random() * 20) + 1;
                    edges.push({
                        from: i,
                        to: j,
                        weight
                    });
                }
            }
        }

        // Ensure graph is connected
        for (let i = 1; i < nodeCount; i++) {
            const hasConnection = edges.some(e =>
                (e.from === i || e.to === i) ||
                (e.from === i - 1 || e.to === i - 1)
            );

            if (!hasConnection) {
                edges.push({
                    from: i - 1,
                    to: i,
                    weight: Math.floor(Math.random() * 20) + 1
                });
            }
        }

        return { nodes, edges };
    }

    /**
     * Generate grid graph
     */
    generateGridGraph(rows, cols) {
        const nodes = [];
        const edges = [];

        // Create grid nodes
        for (let r = 0; r < rows; r++) {
            for (let c = 0; c < cols; c++) {
                const id = r * cols + c;
                nodes.push({
                    id,
                    label: id.toString(),
                    x: 0,
                    y: 0,
                    gridRow: r,
                    gridCol: c
                });
            }
        }

        // Create edges (4-connected grid)
        for (let r = 0; r < rows; r++) {
            for (let c = 0; c < cols; c++) {
                const id = r * cols + c;

                // Right neighbor
                if (c < cols - 1) {
                    edges.push({
                        from: id,
                        to: id + 1,
                        weight: 1
                    });
                }

                // Bottom neighbor
                if (r < rows - 1) {
                    edges.push({
                        from: id,
                        to: id + cols,
                        weight: 1
                    });
                }
            }
        }

        return { nodes, edges };
    }

    /**
     * Generate tree graph
     */
    generateTreeGraph(nodeCount) {
        const nodes = [];
        const edges = [];

        // Create nodes
        for (let i = 0; i < nodeCount; i++) {
            nodes.push({
                id: i,
                label: i.toString(),
                x: 0,
                y: 0
            });
        }

        // Create tree edges (each node except root connects to one parent)
        for (let i = 1; i < nodeCount; i++) {
            const parent = Math.floor((i - 1) / 2);
            edges.push({
                from: parent,
                to: i,
                weight: Math.floor(Math.random() * 15) + 1
            });
        }

        return { nodes, edges };
    }

    /**
     * Calculate node positions based on graph type
     */
    calculateNodePositions() {
        if (!this.graph) return;

        const width = parseInt(this.svg.getAttribute('width')) || 800;
        const height = parseInt(this.svg.getAttribute('height')) || 500;
        const padding = 50;

        if (this.graphType === 'grid') {
            // Grid layout
            const rows = Math.max(...this.graph.nodes.map(n => n.gridRow)) + 1;
            const cols = Math.max(...this.graph.nodes.map(n => n.gridCol)) + 1;

            const cellWidth = (width - 2 * padding) / (cols - 1);
            const cellHeight = (height - 2 * padding) / (rows - 1);

            this.graph.nodes.forEach(node => {
                node.x = padding + node.gridCol * cellWidth;
                node.y = padding + node.gridRow * cellHeight;
            });
        } else {
            // Circular or force-directed layout
            const nodeCount = this.graph.nodes.length;
            const radius = Math.min(width, height) / 2 - padding;
            const centerX = width / 2;
            const centerY = height / 2;

            this.graph.nodes.forEach((node, i) => {
                const angle = (2 * Math.PI * i) / nodeCount - Math.PI / 2;
                node.x = centerX + radius * Math.cos(angle);
                node.y = centerY + radius * Math.sin(angle);
            });
        }
    }

    /**
     * Draw graph
     */
    draw(highlightStates = {}) {
        // Clear SVG
        this.svg.innerHTML = '';

        if (!this.graph) return;

        // Draw edges first
        this.graph.edges.forEach(edge => {
            const fromNode = this.graph.nodes[edge.from];
            const toNode = this.graph.nodes[edge.to];

            // Determine edge color
            let color = this.colors.edge;
            let strokeWidth = 2;

            if (highlightStates.pathEdges &&
                highlightStates.pathEdges.some(e => this.edgesEqual(e, edge))) {
                color = this.colors.edgePath;
                strokeWidth = 4;
            } else if (highlightStates.visitedEdges &&
                highlightStates.visitedEdges.some(e => this.edgesEqual(e, edge))) {
                color = this.colors.edgeVisited;
                strokeWidth = 3;
            } else if (highlightStates.currentEdge &&
                this.edgesEqual(highlightStates.currentEdge, edge)) {
                color = this.colors.edgeActive;
                strokeWidth = 4;
            }

            // Draw line
            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            line.setAttribute('x1', fromNode.x);
            line.setAttribute('y1', fromNode.y);
            line.setAttribute('x2', toNode.x);
            line.setAttribute('y2', toNode.y);
            line.setAttribute('stroke', color);
            line.setAttribute('stroke-width', strokeWidth);
            line.setAttribute('class', 'graph-edge');
            this.svg.appendChild(line);

            // Draw weight label
            if (edge.weight > 1) {
                const midX = (fromNode.x + toNode.x) / 2;
                const midY = (fromNode.y + toNode.y) / 2;

                const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                text.setAttribute('x', midX);
                text.setAttribute('y', midY - 5);
                text.setAttribute('text-anchor', 'middle');
                text.setAttribute('font-size', '12');
                text.setAttribute('fill', '#6b7280');
                text.setAttribute('font-weight', 'bold');
                text.textContent = edge.weight;
                this.svg.appendChild(text);
            }
        });

        // Draw nodes
        this.graph.nodes.forEach(node => {
            // Determine node color
            let color = this.colors.node;

            if (highlightStates.current === node.id) {
                color = this.colors.nodeCurrent;
            } else if (highlightStates.visited && highlightStates.visited.includes(node.id)) {
                color = this.colors.nodeVisited;
            } else if (highlightStates.queue && highlightStates.queue.includes(node.id)) {
                color = this.colors.nodeQueue;
            }

            // Create node group
            const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
            g.setAttribute('class', 'graph-node');

            // Draw circle
            const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            circle.setAttribute('cx', node.x);
            circle.setAttribute('cy', node.y);
            circle.setAttribute('r', '20');
            circle.setAttribute('fill', color);
            circle.setAttribute('stroke', '#ffffff');
            circle.setAttribute('stroke-width', '3');

            // Draw label
            const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            text.setAttribute('x', node.x);
            text.setAttribute('y', node.y);
            text.setAttribute('text-anchor', 'middle');
            text.setAttribute('dominant-baseline', 'middle');
            text.setAttribute('fill', '#ffffff');
            text.setAttribute('font-size', '14');
            text.setAttribute('font-weight', 'bold');
            text.textContent = node.label;

            g.appendChild(circle);
            g.appendChild(text);
            this.svg.appendChild(g);
        });
    }

    /**
     * Check if two edges are equal (undirected)
     */
    edgesEqual(e1, e2) {
        return (e1.from === e2.from && e1.to === e2.to) ||
               (e1.from === e2.to && e1.to === e2.from);
    }

    /**
     * Get neighbors of a node
     */
    getNeighbors(nodeId) {
        const neighbors = [];

        this.graph.edges.forEach(edge => {
            if (edge.from === nodeId) {
                neighbors.push({ id: edge.to, weight: edge.weight });
            } else if (edge.to === nodeId) {
                neighbors.push({ id: edge.from, weight: edge.weight });
            }
        });

        return neighbors;
    }

    /**
     * Start graph algorithm visualization
     */
    async start(algorithm) {
        this.core.reset();
        const startNode = 0; // Always start from node 0

        switch (algorithm) {
            case 'bfs':
                await this.breadthFirstSearch(startNode);
                break;
            case 'dfs':
                await this.depthFirstSearch(startNode);
                break;
            case 'dijkstra':
                await this.dijkstra(startNode);
                break;
            case 'astar':
                await this.aStar(startNode, this.graph.nodes.length - 1);
                break;
            case 'prim':
                await this.primMST();
                break;
            case 'kruskal':
                await this.kruskalMST();
                break;
            default:
                console.error('Unknown graph algorithm:', algorithm);
                return;
        }

        this.core.start();
    }

    /**
     * Breadth-First Search
     */
    async breadthFirstSearch(startNode) {
        const visited = [];
        const queue = [startNode];
        const visitedEdges = [];

        while (queue.length > 0) {
            const current = queue.shift();

            if (visited.includes(current)) continue;

            // Visit current node
            this.core.addStep(() => {
                this.core.recordAccess();
                visited.push(current);
                this.draw({
                    current,
                    visited: [...visited],
                    queue: [...queue],
                    visitedEdges: [...visitedEdges]
                });
            });

            // Explore neighbors
            const neighbors = this.getNeighbors(current);
            neighbors.forEach(neighbor => {
                if (!visited.includes(neighbor.id) && !queue.includes(neighbor.id)) {
                    queue.push(neighbor.id);
                    visitedEdges.push({ from: current, to: neighbor.id });
                }
            });
        }

        // Final state
        this.core.addStep(() => {
            this.draw({ visited: [...visited], visitedEdges });
        });
    }

    /**
     * Depth-First Search
     */
    async depthFirstSearch(startNode) {
        const visited = [];
        const visitedEdges = [];

        const dfs = (nodeId) => {
            // Visit node
            this.core.addStep(() => {
                this.core.recordAccess();
                visited.push(nodeId);
                this.draw({
                    current: nodeId,
                    visited: [...visited],
                    visitedEdges: [...visitedEdges]
                });
            });

            // Explore neighbors
            const neighbors = this.getNeighbors(nodeId);
            neighbors.forEach(neighbor => {
                if (!visited.includes(neighbor.id)) {
                    visitedEdges.push({ from: nodeId, to: neighbor.id });
                    dfs(neighbor.id);
                }
            });
        };

        dfs(startNode);

        // Final state
        this.core.addStep(() => {
            this.draw({ visited: [...visited], visitedEdges });
        });
    }

    /**
     * Dijkstra's Shortest Path Algorithm
     */
    async dijkstra(startNode) {
        const distances = new Array(this.graph.nodes.length).fill(Infinity);
        const previous = new Array(this.graph.nodes.length).fill(null);
        const visited = [];
        const unvisited = this.graph.nodes.map(n => n.id);

        distances[startNode] = 0;

        while (unvisited.length > 0) {
            // Find node with minimum distance
            let current = unvisited[0];
            unvisited.forEach(nodeId => {
                if (distances[nodeId] < distances[current]) {
                    current = nodeId;
                }
            });

            if (distances[current] === Infinity) break;

            unvisited.splice(unvisited.indexOf(current), 1);

            // Visit current node
            this.core.addStep(() => {
                this.core.recordAccess();
                visited.push(current);
                this.draw({
                    current,
                    visited: [...visited]
                });
            });

            // Update neighbors
            const neighbors = this.getNeighbors(current);
            neighbors.forEach(neighbor => {
                if (!visited.includes(neighbor.id)) {
                    const newDist = distances[current] + neighbor.weight;

                    if (newDist < distances[neighbor.id]) {
                        distances[neighbor.id] = newDist;
                        previous[neighbor.id] = current;
                    }
                }
            });
        }

        // Show final shortest path tree
        const pathEdges = [];
        previous.forEach((prev, nodeId) => {
            if (prev !== null) {
                pathEdges.push({ from: prev, to: nodeId });
            }
        });

        this.core.addStep(() => {
            this.draw({ visited: [...visited], pathEdges });
        });
    }

    /**
     * A* Search Algorithm (simplified - uses node ID as heuristic)
     */
    async aStar(startNode, goalNode) {
        const gScore = new Array(this.graph.nodes.length).fill(Infinity);
        const fScore = new Array(this.graph.nodes.length).fill(Infinity);
        const cameFrom = new Array(this.graph.nodes.length).fill(null);
        const visited = [];
        const openSet = [startNode];

        gScore[startNode] = 0;
        fScore[startNode] = Math.abs(goalNode - startNode); // Simple heuristic

        while (openSet.length > 0) {
            // Find node in openSet with lowest fScore
            let current = openSet[0];
            openSet.forEach(nodeId => {
                if (fScore[nodeId] < fScore[current]) {
                    current = nodeId;
                }
            });

            // Goal reached
            if (current === goalNode) {
                const path = [];
                let temp = current;
                while (temp !== null) {
                    path.unshift(temp);
                    temp = cameFrom[temp];
                }

                const pathEdges = [];
                for (let i = 0; i < path.length - 1; i++) {
                    pathEdges.push({ from: path[i], to: path[i + 1] });
                }

                this.core.addStep(() => {
                    this.draw({ visited: path, pathEdges });
                });
                return;
            }

            openSet.splice(openSet.indexOf(current), 1);
            visited.push(current);

            this.core.addStep(() => {
                this.core.recordAccess();
                this.draw({
                    current,
                    visited: [...visited],
                    queue: [...openSet]
                });
            });

            // Explore neighbors
            const neighbors = this.getNeighbors(current);
            neighbors.forEach(neighbor => {
                const tentativeGScore = gScore[current] + neighbor.weight;

                if (tentativeGScore < gScore[neighbor.id]) {
                    cameFrom[neighbor.id] = current;
                    gScore[neighbor.id] = tentativeGScore;
                    fScore[neighbor.id] = gScore[neighbor.id] + Math.abs(goalNode - neighbor.id);

                    if (!openSet.includes(neighbor.id)) {
                        openSet.push(neighbor.id);
                    }
                }
            });
        }

        // No path found
        this.core.addStep(() => {
            this.draw({ visited: [...visited] });
        });
    }

    /**
     * Prim's Minimum Spanning Tree
     */
    async primMST() {
        const visited = [0];
        const mstEdges = [];

        while (visited.length < this.graph.nodes.length) {
            let minEdge = null;
            let minWeight = Infinity;

            // Find minimum weight edge connecting visited to unvisited
            this.graph.edges.forEach(edge => {
                const fromVisited = visited.includes(edge.from);
                const toVisited = visited.includes(edge.to);

                if (fromVisited !== toVisited && edge.weight < minWeight) {
                    minWeight = edge.weight;
                    minEdge = edge;
                }
            });

            if (!minEdge) break;

            // Add edge to MST
            mstEdges.push(minEdge);
            const newNode = visited.includes(minEdge.from) ? minEdge.to : minEdge.from;
            visited.push(newNode);

            this.core.addStep(() => {
                this.core.recordAccess();
                this.draw({
                    visited: [...visited],
                    pathEdges: [...mstEdges],
                    currentEdge: minEdge
                });
            });
        }

        // Final MST
        this.core.addStep(() => {
            this.draw({ visited: [...visited], pathEdges: mstEdges });
        });
    }

    /**
     * Kruskal's Minimum Spanning Tree
     */
    async kruskalMST() {
        const parent = Array.from({ length: this.graph.nodes.length }, (_, i) => i);
        const mstEdges = [];

        const find = (x) => {
            if (parent[x] !== x) {
                parent[x] = find(parent[x]);
            }
            return parent[x];
        };

        const union = (x, y) => {
            parent[find(x)] = find(y);
        };

        // Sort edges by weight
        const sortedEdges = [...this.graph.edges].sort((a, b) => a.weight - b.weight);

        for (const edge of sortedEdges) {
            const rootFrom = find(edge.from);
            const rootTo = find(edge.to);

            this.core.addStep(() => {
                this.core.recordAccess();
                this.draw({
                    currentEdge: edge,
                    pathEdges: [...mstEdges]
                });
            });

            if (rootFrom !== rootTo) {
                mstEdges.push(edge);
                union(edge.from, edge.to);

                this.core.addStep(() => {
                    this.draw({ pathEdges: [...mstEdges] });
                });
            }
        }

        // Final MST
        this.core.addStep(() => {
            this.draw({ pathEdges: mstEdges });
        });
    }

    /**
     * Reset visualization
     */
    reset() {
        this.core.reset();
        this.generateGraph(this.graphType);
    }

    /**
     * Resize handler
     */
    resize() {
        this.calculateNodePositions();
        this.draw();
    }
}
