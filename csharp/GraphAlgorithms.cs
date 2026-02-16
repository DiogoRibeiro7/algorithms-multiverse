using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace AlgorithmsMultiverse.CSharp
{
    /// <summary>
    /// Comprehensive graph algorithms implementation with LINQ optimizations
    /// </summary>
    public static class GraphAlgorithms
    {
        #region Graph Traversal

        /// <summary>
        /// Breadth-First Search traversal
        /// </summary>
        public static IEnumerable<T> BFS<T>(Graph<T> graph, T start)
        {
            if (!graph.HasVertex(start))
                throw new ArgumentException($"Vertex {start} not found in graph");

            var visited = new HashSet<T>();
            var queue = new Queue<T>();
            queue.Enqueue(start);
            visited.Add(start);

            while (queue.Count > 0)
            {
                var vertex = queue.Dequeue();
                yield return vertex;

                foreach (var neighbor in graph.GetNeighbors(vertex).Where(n => !visited.Contains(n)))
                {
                    visited.Add(neighbor);
                    queue.Enqueue(neighbor);
                }
            }
        }

        /// <summary>
        /// Depth-First Search traversal (iterative)
        /// </summary>
        public static IEnumerable<T> DFS<T>(Graph<T> graph, T start)
        {
            if (!graph.HasVertex(start))
                throw new ArgumentException($"Vertex {start} not found in graph");

            var visited = new HashSet<T>();
            var stack = new Stack<T>();
            stack.Push(start);

            while (stack.Count > 0)
            {
                var vertex = stack.Pop();

                if (!visited.Contains(vertex))
                {
                    visited.Add(vertex);
                    yield return vertex;

                    foreach (var neighbor in graph.GetNeighbors(vertex).Where(n => !visited.Contains(n)))
                    {
                        stack.Push(neighbor);
                    }
                }
            }
        }

        /// <summary>
        /// Depth-First Search traversal (recursive) using LINQ
        /// </summary>
        public static IEnumerable<T> DFSRecursive<T>(Graph<T> graph, T start, HashSet<T> visited = null)
        {
            visited ??= new HashSet<T>();

            if (!visited.Contains(start))
            {
                visited.Add(start);
                yield return start;

                foreach (var item in graph.GetNeighbors(start)
                    .Where(n => !visited.Contains(n))
                    .SelectMany(n => DFSRecursive(graph, n, visited)))
                {
                    yield return item;
                }
            }
        }

        #endregion

        #region Shortest Path Algorithms

        /// <summary>
        /// Dijkstra's shortest path algorithm
        /// </summary>
        public static Dictionary<T, (double Distance, T Previous)> Dijkstra<T>(
            Dictionary<T, List<(T Neighbor, double Weight)>> graph,
            T start) where T : IComparable<T>
        {
            var distances = graph.Keys.ToDictionary(
                vertex => vertex,
                vertex => (Distance: double.PositiveInfinity, Previous: default(T))
            );

            distances[start] = (0, default);

            var priorityQueue = new SortedSet<(double Distance, T Vertex)>(
                Comparer<(double, T)>.Create((a, b) =>
                {
                    int distCompare = a.Item1.CompareTo(b.Item1);
                    return distCompare != 0 ? distCompare : a.Item2.CompareTo(b.Item2);
                })
            );

            priorityQueue.Add((0, start));

            while (priorityQueue.Count > 0)
            {
                var current = priorityQueue.Min;
                priorityQueue.Remove(current);

                if (current.Distance > distances[current.Vertex].Distance)
                    continue;

                foreach (var (neighbor, weight) in graph[current.Vertex])
                {
                    double altDistance = distances[current.Vertex].Distance + weight;

                    if (altDistance < distances[neighbor].Distance)
                    {
                        distances[neighbor] = (altDistance, current.Vertex);
                        priorityQueue.Add((altDistance, neighbor));
                    }
                }
            }

            return distances;
        }

        /// <summary>
        /// Bellman-Ford algorithm for graphs with negative weights
        /// </summary>
        public static Dictionary<T, (double Distance, T Previous)> BellmanFord<T>(
            List<(T From, T To, double Weight)> edges,
            IEnumerable<T> vertices,
            T start)
        {
            var distances = vertices.ToDictionary(
                vertex => vertex,
                vertex => (Distance: double.PositiveInfinity, Previous: default(T))
            );

            distances[start] = (0, default);

            // Relax edges V-1 times
            int vertexCount = vertices.Count();
            for (int i = 0; i < vertexCount - 1; i++)
            {
                foreach (var (from, to, weight) in edges)
                {
                    if (distances[from].Distance != double.PositiveInfinity &&
                        distances[from].Distance + weight < distances[to].Distance)
                    {
                        distances[to] = (distances[from].Distance + weight, from);
                    }
                }
            }

            // Check for negative cycles
            foreach (var (from, to, weight) in edges)
            {
                if (distances[from].Distance != double.PositiveInfinity &&
                    distances[from].Distance + weight < distances[to].Distance)
                {
                    throw new InvalidOperationException("Graph contains negative cycle");
                }
            }

            return distances;
        }

        /// <summary>
        /// Floyd-Warshall algorithm for all-pairs shortest paths
        /// </summary>
        public static double[,] FloydWarshall<T>(Dictionary<T, List<(T Neighbor, double Weight)>> graph)
        {
            var vertices = graph.Keys.ToList();
            int n = vertices.Count;
            var indexMap = vertices.Select((v, i) => new { v, i }).ToDictionary(x => x.v, x => x.i);

            // Initialize distance matrix
            double[,] dist = new double[n, n];
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    dist[i, j] = i == j ? 0 : double.PositiveInfinity;

            // Fill in edge weights
            foreach (var vertex in graph.Keys)
            {
                int i = indexMap[vertex];
                foreach (var (neighbor, weight) in graph[vertex])
                {
                    int j = indexMap[neighbor];
                    dist[i, j] = weight;
                }
            }

            // Dynamic programming
            for (int k = 0; k < n; k++)
                for (int i = 0; i < n; i++)
                    for (int j = 0; j < n; j++)
                        if (dist[i, k] + dist[k, j] < dist[i, j])
                            dist[i, j] = dist[i, k] + dist[k, j];

            return dist;
        }

        /// <summary>
        /// A* pathfinding algorithm
        /// </summary>
        public static List<T> AStar<T>(
            Dictionary<T, List<(T Neighbor, double Weight)>> graph,
            T start,
            T goal,
            Func<T, T, double> heuristic) where T : IComparable<T>
        {
            var openSet = new SortedSet<(double F, T Vertex)>(
                Comparer<(double, T)>.Create((a, b) =>
                {
                    int fCompare = a.Item1.CompareTo(b.Item1);
                    return fCompare != 0 ? fCompare : a.Item2.CompareTo(b.Item2);
                })
            );

            var cameFrom = new Dictionary<T, T>();
            var gScore = graph.Keys.ToDictionary(v => v, v => double.PositiveInfinity);
            var fScore = graph.Keys.ToDictionary(v => v, v => double.PositiveInfinity);

            gScore[start] = 0;
            fScore[start] = heuristic(start, goal);
            openSet.Add((fScore[start], start));

            while (openSet.Count > 0)
            {
                var current = openSet.Min;
                openSet.Remove(current);

                if (current.Vertex.Equals(goal))
                {
                    // Reconstruct path
                    var path = new List<T> { goal };
                    T node = goal;

                    while (cameFrom.ContainsKey(node))
                    {
                        node = cameFrom[node];
                        path.Insert(0, node);
                    }

                    return path;
                }

                foreach (var (neighbor, weight) in graph[current.Vertex])
                {
                    double tentativeGScore = gScore[current.Vertex] + weight;

                    if (tentativeGScore < gScore[neighbor])
                    {
                        cameFrom[neighbor] = current.Vertex;
                        gScore[neighbor] = tentativeGScore;
                        fScore[neighbor] = tentativeGScore + heuristic(neighbor, goal);

                        openSet.Add((fScore[neighbor], neighbor));
                    }
                }
            }

            return null; // No path found
        }

        #endregion

        #region Minimum Spanning Tree

        /// <summary>
        /// Kruskal's algorithm for Minimum Spanning Tree
        /// </summary>
        public static List<(T From, T To, double Weight)> Kruskal<T>(
            List<(T From, T To, double Weight)> edges,
            IEnumerable<T> vertices)
        {
            var parent = vertices.ToDictionary(v => v, v => v);
            var rank = vertices.ToDictionary(v => v, v => 0);

            T Find(T vertex)
            {
                if (!parent[vertex].Equals(vertex))
                    parent[vertex] = Find(parent[vertex]);
                return parent[vertex];
            }

            bool Union(T v1, T v2)
            {
                T root1 = Find(v1);
                T root2 = Find(v2);

                if (root1.Equals(root2))
                    return false;

                if (rank[root1] < rank[root2])
                    parent[root1] = root2;
                else if (rank[root1] > rank[root2])
                    parent[root2] = root1;
                else
                {
                    parent[root2] = root1;
                    rank[root1]++;
                }

                return true;
            }

            var mst = new List<(T From, T To, double Weight)>();
            var sortedEdges = edges.OrderBy(e => e.Weight);

            foreach (var edge in sortedEdges)
            {
                if (Union(edge.From, edge.To))
                {
                    mst.Add(edge);

                    if (mst.Count == vertices.Count() - 1)
                        break;
                }
            }

            return mst;
        }

        /// <summary>
        /// Prim's algorithm for Minimum Spanning Tree using LINQ
        /// </summary>
        public static List<(T From, T To, double Weight)> Prim<T>(
            Dictionary<T, List<(T Neighbor, double Weight)>> graph,
            T start) where T : IComparable<T>
        {
            var mst = new List<(T From, T To, double Weight)>();
            var visited = new HashSet<T> { start };
            var edges = new SortedSet<(double Weight, T From, T To)>(
                Comparer<(double, T, T)>.Create((a, b) =>
                {
                    int weightCompare = a.Item1.CompareTo(b.Item1);
                    if (weightCompare != 0) return weightCompare;
                    int fromCompare = a.Item2.CompareTo(b.Item2);
                    if (fromCompare != 0) return fromCompare;
                    return a.Item3.CompareTo(b.Item3);
                })
            );

            // Add initial edges
            foreach (var (neighbor, weight) in graph[start])
                edges.Add((weight, start, neighbor));

            while (edges.Count > 0 && visited.Count < graph.Count)
            {
                var minEdge = edges.Min;
                edges.Remove(minEdge);

                if (!visited.Contains(minEdge.To))
                {
                    visited.Add(minEdge.To);
                    mst.Add((minEdge.From, minEdge.To, minEdge.Weight));

                    // Add new edges
                    foreach (var (neighbor, weight) in graph[minEdge.To])
                    {
                        if (!visited.Contains(neighbor))
                            edges.Add((weight, minEdge.To, neighbor));
                    }
                }
            }

            return mst;
        }

        #endregion

        #region Graph Analysis

        /// <summary>
        /// Detect cycles in a directed graph
        /// </summary>
        public static bool HasCycle<T>(Graph<T> graph)
        {
            var visited = new HashSet<T>();
            var recursionStack = new HashSet<T>();

            bool HasCycleDFS(T vertex)
            {
                visited.Add(vertex);
                recursionStack.Add(vertex);

                foreach (var neighbor in graph.GetNeighbors(vertex))
                {
                    if (!visited.Contains(neighbor))
                    {
                        if (HasCycleDFS(neighbor))
                            return true;
                    }
                    else if (recursionStack.Contains(neighbor))
                    {
                        return true;
                    }
                }

                recursionStack.Remove(vertex);
                return false;
            }

            return graph.GetVertices().Any(vertex => !visited.Contains(vertex) && HasCycleDFS(vertex));
        }

        /// <summary>
        /// Topological sort for DAG using LINQ
        /// </summary>
        public static List<T> TopologicalSort<T>(Graph<T> graph)
        {
            var inDegree = graph.GetVertices().ToDictionary(v => v, v => 0);

            foreach (var vertex in graph.GetVertices())
                foreach (var neighbor in graph.GetNeighbors(vertex))
                    inDegree[neighbor]++;

            var queue = new Queue<T>(inDegree.Where(kvp => kvp.Value == 0).Select(kvp => kvp.Key));
            var result = new List<T>();

            while (queue.Count > 0)
            {
                var vertex = queue.Dequeue();
                result.Add(vertex);

                foreach (var neighbor in graph.GetNeighbors(vertex))
                {
                    inDegree[neighbor]--;
                    if (inDegree[neighbor] == 0)
                        queue.Enqueue(neighbor);
                }
            }

            return result.Count == graph.VertexCount ? result : null; // null if cycle exists
        }

        /// <summary>
        /// Find strongly connected components using Kosaraju's algorithm
        /// </summary>
        public static List<List<T>> StronglyConnectedComponents<T>(Graph<T> graph)
        {
            var stack = new Stack<T>();
            var visited = new HashSet<T>();

            // First DFS to fill stack
            void FillStack(T vertex)
            {
                visited.Add(vertex);
                foreach (var neighbor in graph.GetNeighbors(vertex).Where(n => !visited.Contains(n)))
                    FillStack(neighbor);
                stack.Push(vertex);
            }

            foreach (var vertex in graph.GetVertices().Where(v => !visited.Contains(v)))
                FillStack(vertex);

            // Create transpose graph
            var transpose = new Graph<T>(true);
            foreach (var vertex in graph.GetVertices())
            {
                transpose.AddVertex(vertex);
                foreach (var neighbor in graph.GetNeighbors(vertex))
                    transpose.AddEdge(neighbor, vertex);
            }

            // Second DFS on transpose
            visited.Clear();
            var components = new List<List<T>>();

            void DFSTranspose(T vertex, List<T> component)
            {
                visited.Add(vertex);
                component.Add(vertex);
                foreach (var neighbor in transpose.GetNeighbors(vertex).Where(n => !visited.Contains(n)))
                    DFSTranspose(neighbor, component);
            }

            while (stack.Count > 0)
            {
                var vertex = stack.Pop();
                if (!visited.Contains(vertex))
                {
                    var component = new List<T>();
                    DFSTranspose(vertex, component);
                    components.Add(component);
                }
            }

            return components;
        }

        /// <summary>
        /// Check if graph is bipartite using coloring
        /// </summary>
        public static bool IsBipartite<T>(Graph<T> graph)
        {
            var colors = new Dictionary<T, int>();

            bool BFSColoring(T start)
            {
                var queue = new Queue<T>();
                queue.Enqueue(start);
                colors[start] = 0;

                while (queue.Count > 0)
                {
                    var vertex = queue.Dequeue();
                    int currentColor = colors[vertex];

                    foreach (var neighbor in graph.GetNeighbors(vertex))
                    {
                        if (!colors.ContainsKey(neighbor))
                        {
                            colors[neighbor] = 1 - currentColor;
                            queue.Enqueue(neighbor);
                        }
                        else if (colors[neighbor] == currentColor)
                        {
                            return false;
                        }
                    }
                }

                return true;
            }

            return graph.GetVertices()
                .Where(v => !colors.ContainsKey(v))
                .All(v => BFSColoring(v));
        }

        /// <summary>
        /// Find all paths between two vertices using LINQ
        /// </summary>
        public static IEnumerable<List<T>> FindAllPaths<T>(Graph<T> graph, T start, T end)
        {
            var visited = new HashSet<T>();
            var path = new List<T>();

            IEnumerable<List<T>> DFS(T current)
            {
                visited.Add(current);
                path.Add(current);

                if (current.Equals(end))
                {
                    yield return new List<T>(path);
                }
                else
                {
                    foreach (var result in graph.GetNeighbors(current)
                        .Where(n => !visited.Contains(n))
                        .SelectMany(n => DFS(n)))
                    {
                        yield return result;
                    }
                }

                path.RemoveAt(path.Count - 1);
                visited.Remove(current);
            }

            return DFS(start);
        }

        #endregion

        #region Parallel Graph Algorithms

        /// <summary>
        /// Parallel BFS traversal
        /// </summary>
        public static async Task<List<T>> ParallelBFS<T>(Graph<T> graph, T start)
        {
            var visited = new System.Collections.Concurrent.ConcurrentDictionary<T, bool>();
            var result = new System.Collections.Concurrent.ConcurrentBag<T>();
            var currentLevel = new List<T> { start };

            visited.TryAdd(start, true);

            while (currentLevel.Count > 0)
            {
                foreach (var vertex in currentLevel)
                    result.Add(vertex);

                var nextLevel = new System.Collections.Concurrent.ConcurrentBag<T>();

                await Task.Run(() =>
                {
                    Parallel.ForEach(currentLevel, vertex =>
                    {
                        foreach (var neighbor in graph.GetNeighbors(vertex))
                        {
                            if (visited.TryAdd(neighbor, true))
                                nextLevel.Add(neighbor);
                        }
                    });
                });

                currentLevel = nextLevel.ToList();
            }

            return result.ToList();
        }

        /// <summary>
        /// Parallel shortest paths computation
        /// </summary>
        public static async Task<Dictionary<T, double>> ParallelDijkstraFromAllVertices<T>(
            Dictionary<T, List<(T Neighbor, double Weight)>> graph) where T : IComparable<T>
        {
            var tasks = graph.Keys.Select(async vertex =>
            {
                var result = await Task.Run(() => Dijkstra(graph, vertex));
                return (vertex, result);
            });

            var results = await Task.WhenAll(tasks);

            return results.ToDictionary(
                r => r.vertex,
                r => r.result.Values.Max(v => v.Distance == double.PositiveInfinity ? 0 : v.Distance)
            );
        }

        #endregion
    }

    /// <summary>
    /// Graph extensions for LINQ operations
    /// </summary>
    public static class GraphExtensions
    {
        /// <summary>
        /// Get all vertices reachable from a given vertex
        /// </summary>
        public static IEnumerable<T> GetReachableVertices<T>(this Graph<T> graph, T start)
        {
            return GraphAlgorithms.BFS(graph, start);
        }

        /// <summary>
        /// Check if path exists between two vertices
        /// </summary>
        public static bool HasPath<T>(this Graph<T> graph, T start, T end)
        {
            return GraphAlgorithms.BFS(graph, start).Contains(end);
        }

        /// <summary>
        /// Get vertex with maximum degree
        /// </summary>
        public static T GetMaxDegreeVertex<T>(this Graph<T> graph)
        {
            return graph.GetVertices()
                .OrderByDescending(v => graph.GetDegree(v))
                .FirstOrDefault();
        }

        /// <summary>
        /// Get connected components for undirected graph
        /// </summary>
        public static List<List<T>> GetConnectedComponents<T>(this Graph<T> graph)
        {
            var visited = new HashSet<T>();
            var components = new List<List<T>>();

            foreach (var vertex in graph.GetVertices())
            {
                if (!visited.Contains(vertex))
                {
                    var component = GraphAlgorithms.BFS(graph, vertex).ToList();
                    components.Add(component);
                    visited.UnionWith(component);
                }
            }

            return components;
        }

        /// <summary>
        /// Convert graph to adjacency matrix
        /// </summary>
        public static int[,] ToAdjacencyMatrix<T>(this Graph<T> graph)
        {
            var vertices = graph.GetVertices().ToList();
            var indexMap = vertices.Select((v, i) => new { v, i }).ToDictionary(x => x.v, x => x.i);
            int n = vertices.Count;
            var matrix = new int[n, n];

            foreach (var vertex in vertices)
            {
                int i = indexMap[vertex];
                foreach (var neighbor in graph.GetNeighbors(vertex))
                {
                    int j = indexMap[neighbor];
                    matrix[i, j] = 1;
                }
            }

            return matrix;
        }
    }
}