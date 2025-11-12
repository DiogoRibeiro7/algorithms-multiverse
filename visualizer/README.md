# Algorithm Visualizer

An interactive web-based algorithm visualization tool for learning and understanding various algorithms through step-by-step animations.

## Features

### Sorting Algorithms
- **Bubble Sort** - O(n²) time complexity
- **Selection Sort** - O(n²) time complexity
- **Insertion Sort** - O(n²) time complexity
- **Merge Sort** - O(n log n) time complexity
- **Quick Sort** - O(n log n) average time complexity
- **Heap Sort** - O(n log n) time complexity

**Interactive Controls:**
- Adjustable array size (5-100 elements)
- Variable animation speed (1x-10x)
- Different initial data patterns (random, nearly sorted, reversed)
- Real-time statistics (comparisons, array accesses, time elapsed)
- Code display in JavaScript, Python, and Java

### Tree Algorithms
- **In-Order Traversal** (Left, Root, Right)
- **Pre-Order Traversal** (Root, Left, Right)
- **Post-Order Traversal** (Left, Right, Root)
- **Level-Order Traversal** (Breadth-First Search)

**Tree Types:**
- Binary Search Tree (BST)
- Complete Binary Tree
- Balanced Tree

### Graph Algorithms
- **BFS** - Breadth-First Search
- **DFS** - Depth-First Search
- **Dijkstra's Algorithm** - Shortest path
- **A* Search** - Informed search
- **Prim's MST** - Minimum Spanning Tree
- **Kruskal's MST** - Minimum Spanning Tree

**Graph Types:**
- Random graph with adjustable density
- Grid graph (4x4)
- Tree graph

### Search Algorithms
- **Linear Search** - O(n) time complexity
- **Binary Search** - O(log n) time complexity
- **Jump Search** - O(√n) time complexity
- **Interpolation Search** - O(log log n) average case

### Dynamic Programming
- **Fibonacci Sequence** - Classic DP example
- **0/1 Knapsack Problem** - Optimization problem
- **Longest Common Subsequence** - String matching
- **Edit Distance** - Levenshtein distance
- **Coin Change Problem** - Minimum coins

**Features:**
- Visual DP table filling
- Cell-by-cell computation highlighting
- Input string/array display
- Result highlighting

### Comparison Mode
Compare multiple sorting algorithms side-by-side to see:
- Execution time differences
- Number of comparisons
- Performance characteristics

## Technologies Used

- **HTML5** - Structure and canvas/SVG elements
- **CSS3** - Modern styling with CSS variables
- **Vanilla JavaScript** - No frameworks, modular ES6+ code
- **Canvas API** - For sorting and search visualizations
- **SVG** - For tree and graph visualizations

## File Structure

```
visualizer/
├── index.html              # Main HTML file
├── README.md              # This file
├── css/
│   ├── main.css          # Core styles and theme
│   ├── controls.css      # Control panel styles
│   ├── visualizations.css # Canvas/SVG styles
│   └── charts.css        # Comparison chart styles
├── js/
│   ├── main.js           # Application entry point
│   ├── VisualizerCore.js # Core animation engine
│   ├── UIController.js   # UI state management
│   ├── ThemeManager.js   # Dark/light mode
│   └── ComparisonManager.js # Algorithm comparison
└── algorithms/
    ├── SortingVisualizer.js  # Sorting algorithms
    ├── TreeVisualizer.js     # Tree traversals
    ├── GraphVisualizer.js    # Graph algorithms
    ├── SearchVisualizer.js   # Search algorithms
    └── DPVisualizer.js       # Dynamic programming
```

## Usage

1. **Open the visualizer:**
   ```bash
   # Simply open index.html in a modern web browser
   # Or use a local server:
   python -m http.server 8000
   # Then navigate to http://localhost:8000
   ```

2. **Select an algorithm category** from the navigation bar

3. **Configure parameters:**
   - Choose specific algorithm
   - Adjust size/speed settings
   - Generate test data

4. **Start visualization** and observe step-by-step execution

5. **Control playback:**
   - Start/Pause the animation
   - Adjust speed in real-time
   - Reset to generate new data

## Features in Detail

### Animation System
- Smooth step-by-step visualization
- Adjustable playback speed (50ms - 500ms per step)
- Pause/resume capability
- Color-coded state highlighting

### Statistics Tracking
- Real-time operation counting
- Time complexity display
- Performance metrics

### Responsive Design
- Works on desktop and tablet devices
- Adaptive canvas sizing
- Mobile-friendly controls

### Dark Mode Support
- Auto-detects system preference
- Manual toggle available
- Persistent across sessions

### Code Display
- Syntax-highlighted pseudocode
- Multiple language support
- Synchronized with visualization

## Algorithm Complexity Reference

| Algorithm | Best | Average | Worst | Space |
|-----------|------|---------|-------|-------|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) |
| Linear Search | O(1) | O(n) | O(n) | O(1) |
| Binary Search | O(1) | O(log n) | O(log n) | O(1) |

## Browser Compatibility

- Chrome/Edge (recommended) - v90+
- Firefox - v88+
- Safari - v14+
- Opera - v76+

## Educational Value

This visualizer helps students and developers:
- **Understand** how algorithms work internally
- **Compare** different algorithmic approaches
- **Analyze** time and space complexity
- **Learn** through interactive exploration
- **Debug** algorithm implementations

## Future Enhancements

Potential additions:
- More sorting algorithms (Radix, Bucket, Shell Sort)
- Advanced graph algorithms (Floyd-Warshall, Bellman-Ford)
- String algorithms (KMP, Rabin-Karp)
- More DP problems (Matrix Chain, Rod Cutting)
- Step-by-step code execution highlighting
- Custom input data
- Export visualization as GIF/video
- Algorithm complexity graphs
- Interactive tutorials

## Contributing

This is part of the algorithms-multiverse repository. Contributions are welcome!

## License

Part of the algorithms-multiverse educational project.

## Acknowledgments

Built for educational purposes to help visualize and understand fundamental algorithms and data structures.
