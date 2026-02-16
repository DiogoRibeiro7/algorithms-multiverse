using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace AlgorithmsMultiverse.CSharp
{
    #region Linked List

    /// <summary>
    /// Generic doubly linked list implementation
    /// </summary>
    public class LinkedList<T> : IEnumerable<T>
    {
        private class Node
        {
            public T Data { get; set; }
            public Node Next { get; set; }
            public Node Previous { get; set; }

            public Node(T data)
            {
                Data = data;
            }
        }

        private Node head;
        private Node tail;
        public int Count { get; private set; }

        public void AddFirst(T data)
        {
            var node = new Node(data);
            if (head == null)
            {
                head = tail = node;
            }
            else
            {
                node.Next = head;
                head.Previous = node;
                head = node;
            }
            Count++;
        }

        public void AddLast(T data)
        {
            var node = new Node(data);
            if (tail == null)
            {
                head = tail = node;
            }
            else
            {
                node.Previous = tail;
                tail.Next = node;
                tail = node;
            }
            Count++;
        }

        public T RemoveFirst()
        {
            if (head == null)
                throw new InvalidOperationException("List is empty");

            T data = head.Data;
            head = head.Next;

            if (head == null)
                tail = null;
            else
                head.Previous = null;

            Count--;
            return data;
        }

        public T RemoveLast()
        {
            if (tail == null)
                throw new InvalidOperationException("List is empty");

            T data = tail.Data;
            tail = tail.Previous;

            if (tail == null)
                head = null;
            else
                tail.Next = null;

            Count--;
            return data;
        }

        public bool Remove(T data)
        {
            var current = head;
            while (current != null)
            {
                if (EqualityComparer<T>.Default.Equals(current.Data, data))
                {
                    if (current.Previous != null)
                        current.Previous.Next = current.Next;
                    else
                        head = current.Next;

                    if (current.Next != null)
                        current.Next.Previous = current.Previous;
                    else
                        tail = current.Previous;

                    Count--;
                    return true;
                }
                current = current.Next;
            }
            return false;
        }

        public bool Contains(T data)
        {
            return Find(data) != null;
        }

        public T Find(T data)
        {
            var current = head;
            while (current != null)
            {
                if (EqualityComparer<T>.Default.Equals(current.Data, data))
                    return current.Data;
                current = current.Next;
            }
            return default;
        }

        public void Clear()
        {
            head = tail = null;
            Count = 0;
        }

        public IEnumerator<T> GetEnumerator()
        {
            var current = head;
            while (current != null)
            {
                yield return current.Data;
                current = current.Next;
            }
        }

        IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
    }

    #endregion

    #region Stack

    /// <summary>
    /// Generic stack implementation with dynamic resizing
    /// </summary>
    public class Stack<T>
    {
        private T[] items;
        private int top = -1;
        private const int DefaultCapacity = 4;

        public int Count => top + 1;
        public bool IsEmpty => top == -1;

        public Stack(int capacity = DefaultCapacity)
        {
            items = new T[capacity];
        }

        public void Push(T item)
        {
            if (top == items.Length - 1)
                Resize(items.Length * 2);

            items[++top] = item;
        }

        public T Pop()
        {
            if (IsEmpty)
                throw new InvalidOperationException("Stack is empty");

            T item = items[top];
            items[top--] = default;

            if (Count > 0 && Count == items.Length / 4)
                Resize(items.Length / 2);

            return item;
        }

        public T Peek()
        {
            if (IsEmpty)
                throw new InvalidOperationException("Stack is empty");

            return items[top];
        }

        public bool TryPop(out T result)
        {
            if (IsEmpty)
            {
                result = default;
                return false;
            }

            result = Pop();
            return true;
        }

        public bool TryPeek(out T result)
        {
            if (IsEmpty)
            {
                result = default;
                return false;
            }

            result = Peek();
            return true;
        }

        private void Resize(int newCapacity)
        {
            Array.Resize(ref items, newCapacity);
        }

        public T[] ToArray()
        {
            T[] array = new T[Count];
            for (int i = 0; i < Count; i++)
                array[i] = items[i];
            return array;
        }
    }

    #endregion

    #region Queue

    /// <summary>
    /// Circular queue implementation with dynamic resizing
    /// </summary>
    public class Queue<T>
    {
        private T[] items;
        private int head;
        private int tail;
        private int count;

        public int Count => count;
        public bool IsEmpty => count == 0;

        public Queue(int capacity = 16)
        {
            items = new T[capacity];
        }

        public void Enqueue(T item)
        {
            if (count == items.Length)
                Resize(items.Length * 2);

            items[tail] = item;
            tail = (tail + 1) % items.Length;
            count++;
        }

        public T Dequeue()
        {
            if (IsEmpty)
                throw new InvalidOperationException("Queue is empty");

            T item = items[head];
            items[head] = default;
            head = (head + 1) % items.Length;
            count--;

            if (count > 0 && count == items.Length / 4)
                Resize(items.Length / 2);

            return item;
        }

        public T Peek()
        {
            if (IsEmpty)
                throw new InvalidOperationException("Queue is empty");

            return items[head];
        }

        public bool TryDequeue(out T result)
        {
            if (IsEmpty)
            {
                result = default;
                return false;
            }

            result = Dequeue();
            return true;
        }

        private void Resize(int newCapacity)
        {
            T[] newItems = new T[newCapacity];
            for (int i = 0; i < count; i++)
            {
                newItems[i] = items[(head + i) % items.Length];
            }
            items = newItems;
            head = 0;
            tail = count;
        }
    }

    #endregion

    #region Priority Queue

    /// <summary>
    /// Min-heap based priority queue
    /// </summary>
    public class PriorityQueue<T> where T : IComparable<T>
    {
        private List<T> heap = new List<T>();

        public int Count => heap.Count;
        public bool IsEmpty => heap.Count == 0;

        public void Enqueue(T item)
        {
            heap.Add(item);
            int childIndex = heap.Count - 1;

            while (childIndex > 0)
            {
                int parentIndex = (childIndex - 1) / 2;

                if (heap[childIndex].CompareTo(heap[parentIndex]) >= 0)
                    break;

                (heap[childIndex], heap[parentIndex]) = (heap[parentIndex], heap[childIndex]);
                childIndex = parentIndex;
            }
        }

        public T Dequeue()
        {
            if (IsEmpty)
                throw new InvalidOperationException("Priority queue is empty");

            T min = heap[0];
            heap[0] = heap[heap.Count - 1];
            heap.RemoveAt(heap.Count - 1);

            if (heap.Count > 0)
                HeapifyDown(0);

            return min;
        }

        public T Peek()
        {
            if (IsEmpty)
                throw new InvalidOperationException("Priority queue is empty");

            return heap[0];
        }

        private void HeapifyDown(int index)
        {
            while (true)
            {
                int smallest = index;
                int left = 2 * index + 1;
                int right = 2 * index + 2;

                if (left < heap.Count && heap[left].CompareTo(heap[smallest]) < 0)
                    smallest = left;

                if (right < heap.Count && heap[right].CompareTo(heap[smallest]) < 0)
                    smallest = right;

                if (smallest == index)
                    break;

                (heap[index], heap[smallest]) = (heap[smallest], heap[index]);
                index = smallest;
            }
        }
    }

    #endregion

    #region Binary Search Tree

    /// <summary>
    /// Generic Binary Search Tree implementation
    /// </summary>
    public class BinarySearchTree<T> where T : IComparable<T>
    {
        private class Node
        {
            public T Data { get; set; }
            public Node Left { get; set; }
            public Node Right { get; set; }

            public Node(T data)
            {
                Data = data;
            }
        }

        private Node root;
        public int Count { get; private set; }

        public void Insert(T data)
        {
            root = InsertRecursive(root, data);
            Count++;
        }

        private Node InsertRecursive(Node node, T data)
        {
            if (node == null)
                return new Node(data);

            int comparison = data.CompareTo(node.Data);

            if (comparison < 0)
                node.Left = InsertRecursive(node.Left, data);
            else if (comparison > 0)
                node.Right = InsertRecursive(node.Right, data);

            return node;
        }

        public bool Contains(T data)
        {
            return Search(root, data) != null;
        }

        private Node Search(Node node, T data)
        {
            if (node == null)
                return null;

            int comparison = data.CompareTo(node.Data);

            if (comparison == 0)
                return node;
            else if (comparison < 0)
                return Search(node.Left, data);
            else
                return Search(node.Right, data);
        }

        public bool Delete(T data)
        {
            int initialCount = Count;
            root = DeleteRecursive(root, data);
            return Count < initialCount;
        }

        private Node DeleteRecursive(Node node, T data)
        {
            if (node == null)
                return null;

            int comparison = data.CompareTo(node.Data);

            if (comparison < 0)
            {
                node.Left = DeleteRecursive(node.Left, data);
            }
            else if (comparison > 0)
            {
                node.Right = DeleteRecursive(node.Right, data);
            }
            else
            {
                Count--;

                if (node.Left == null)
                    return node.Right;

                if (node.Right == null)
                    return node.Left;

                // Node with two children
                node.Data = FindMin(node.Right).Data;
                node.Right = DeleteRecursive(node.Right, node.Data);
            }

            return node;
        }

        private Node FindMin(Node node)
        {
            while (node.Left != null)
                node = node.Left;
            return node;
        }

        public T FindMax()
        {
            if (root == null)
                throw new InvalidOperationException("Tree is empty");

            Node node = root;
            while (node.Right != null)
                node = node.Right;

            return node.Data;
        }

        public IEnumerable<T> InOrderTraversal()
        {
            return InOrderTraversalRecursive(root);
        }

        private IEnumerable<T> InOrderTraversalRecursive(Node node)
        {
            if (node == null)
                yield break;

            foreach (var item in InOrderTraversalRecursive(node.Left))
                yield return item;

            yield return node.Data;

            foreach (var item in InOrderTraversalRecursive(node.Right))
                yield return item;
        }

        public IEnumerable<T> PreOrderTraversal()
        {
            return PreOrderTraversalRecursive(root);
        }

        private IEnumerable<T> PreOrderTraversalRecursive(Node node)
        {
            if (node == null)
                yield break;

            yield return node.Data;

            foreach (var item in PreOrderTraversalRecursive(node.Left))
                yield return item;

            foreach (var item in PreOrderTraversalRecursive(node.Right))
                yield return item;
        }

        public IEnumerable<T> LevelOrderTraversal()
        {
            if (root == null)
                yield break;

            var queue = new System.Collections.Generic.Queue<Node>();
            queue.Enqueue(root);

            while (queue.Count > 0)
            {
                var node = queue.Dequeue();
                yield return node.Data;

                if (node.Left != null)
                    queue.Enqueue(node.Left);

                if (node.Right != null)
                    queue.Enqueue(node.Right);
            }
        }

        public int Height()
        {
            return HeightRecursive(root);
        }

        private int HeightRecursive(Node node)
        {
            if (node == null)
                return -1;

            return 1 + Math.Max(HeightRecursive(node.Left), HeightRecursive(node.Right));
        }

        public bool IsBalanced()
        {
            return IsBalancedRecursive(root) != -1;
        }

        private int IsBalancedRecursive(Node node)
        {
            if (node == null)
                return 0;

            int leftHeight = IsBalancedRecursive(node.Left);
            if (leftHeight == -1)
                return -1;

            int rightHeight = IsBalancedRecursive(node.Right);
            if (rightHeight == -1)
                return -1;

            if (Math.Abs(leftHeight - rightHeight) > 1)
                return -1;

            return Math.Max(leftHeight, rightHeight) + 1;
        }
    }

    #endregion

    #region Hash Table

    /// <summary>
    /// Hash table with separate chaining
    /// </summary>
    public class HashTable<TKey, TValue>
    {
        private class Entry
        {
            public TKey Key { get; set; }
            public TValue Value { get; set; }
            public Entry Next { get; set; }

            public Entry(TKey key, TValue value)
            {
                Key = key;
                Value = value;
            }
        }

        private Entry[] buckets;
        private int count;
        private const int DefaultCapacity = 16;
        private const double LoadFactorThreshold = 0.75;

        public int Count => count;

        public HashTable(int capacity = DefaultCapacity)
        {
            buckets = new Entry[capacity];
        }

        public void Add(TKey key, TValue value)
        {
            if (key == null)
                throw new ArgumentNullException(nameof(key));

            if ((double)count / buckets.Length > LoadFactorThreshold)
                Resize();

            int index = GetBucketIndex(key);
            Entry entry = buckets[index];

            // Check if key already exists
            while (entry != null)
            {
                if (entry.Key.Equals(key))
                {
                    entry.Value = value;
                    return;
                }
                entry = entry.Next;
            }

            // Add new entry
            Entry newEntry = new Entry(key, value)
            {
                Next = buckets[index]
            };
            buckets[index] = newEntry;
            count++;
        }

        public bool TryGetValue(TKey key, out TValue value)
        {
            if (key == null)
                throw new ArgumentNullException(nameof(key));

            int index = GetBucketIndex(key);
            Entry entry = buckets[index];

            while (entry != null)
            {
                if (entry.Key.Equals(key))
                {
                    value = entry.Value;
                    return true;
                }
                entry = entry.Next;
            }

            value = default;
            return false;
        }

        public bool Remove(TKey key)
        {
            if (key == null)
                throw new ArgumentNullException(nameof(key));

            int index = GetBucketIndex(key);
            Entry entry = buckets[index];
            Entry previous = null;

            while (entry != null)
            {
                if (entry.Key.Equals(key))
                {
                    if (previous == null)
                        buckets[index] = entry.Next;
                    else
                        previous.Next = entry.Next;

                    count--;
                    return true;
                }

                previous = entry;
                entry = entry.Next;
            }

            return false;
        }

        public bool ContainsKey(TKey key)
        {
            return TryGetValue(key, out _);
        }

        public void Clear()
        {
            buckets = new Entry[DefaultCapacity];
            count = 0;
        }

        public IEnumerable<TKey> Keys
        {
            get
            {
                foreach (var bucket in buckets)
                {
                    Entry entry = bucket;
                    while (entry != null)
                    {
                        yield return entry.Key;
                        entry = entry.Next;
                    }
                }
            }
        }

        public IEnumerable<TValue> Values
        {
            get
            {
                foreach (var bucket in buckets)
                {
                    Entry entry = bucket;
                    while (entry != null)
                    {
                        yield return entry.Value;
                        entry = entry.Next;
                    }
                }
            }
        }

        private int GetBucketIndex(TKey key)
        {
            return Math.Abs(key.GetHashCode()) % buckets.Length;
        }

        private void Resize()
        {
            Entry[] oldBuckets = buckets;
            buckets = new Entry[oldBuckets.Length * 2];
            count = 0;

            foreach (var bucket in oldBuckets)
            {
                Entry entry = bucket;
                while (entry != null)
                {
                    Add(entry.Key, entry.Value);
                    entry = entry.Next;
                }
            }
        }

        public TValue this[TKey key]
        {
            get
            {
                if (TryGetValue(key, out TValue value))
                    return value;
                throw new KeyNotFoundException($"Key '{key}' not found");
            }
            set
            {
                Add(key, value);
            }
        }
    }

    #endregion

    #region Trie

    /// <summary>
    /// Trie (Prefix Tree) implementation
    /// </summary>
    public class Trie
    {
        private class TrieNode
        {
            public Dictionary<char, TrieNode> Children { get; } = new Dictionary<char, TrieNode>();
            public bool IsEndOfWord { get; set; }
        }

        private readonly TrieNode root = new TrieNode();
        public int Count { get; private set; }

        public void Insert(string word)
        {
            if (string.IsNullOrEmpty(word))
                return;

            TrieNode current = root;

            foreach (char c in word)
            {
                if (!current.Children.ContainsKey(c))
                    current.Children[c] = new TrieNode();

                current = current.Children[c];
            }

            if (!current.IsEndOfWord)
            {
                current.IsEndOfWord = true;
                Count++;
            }
        }

        public bool Search(string word)
        {
            if (string.IsNullOrEmpty(word))
                return false;

            TrieNode node = SearchPrefix(word);
            return node != null && node.IsEndOfWord;
        }

        public bool StartsWith(string prefix)
        {
            return SearchPrefix(prefix) != null;
        }

        private TrieNode SearchPrefix(string prefix)
        {
            TrieNode current = root;

            foreach (char c in prefix)
            {
                if (!current.Children.ContainsKey(c))
                    return null;

                current = current.Children[c];
            }

            return current;
        }

        public List<string> GetWordsWithPrefix(string prefix)
        {
            List<string> results = new List<string>();
            TrieNode prefixNode = SearchPrefix(prefix);

            if (prefixNode != null)
                GetAllWords(prefixNode, prefix, results);

            return results;
        }

        private void GetAllWords(TrieNode node, string currentWord, List<string> results)
        {
            if (node.IsEndOfWord)
                results.Add(currentWord);

            foreach (var kvp in node.Children)
            {
                GetAllWords(kvp.Value, currentWord + kvp.Key, results);
            }
        }

        public bool Delete(string word)
        {
            if (string.IsNullOrEmpty(word))
                return false;

            return DeleteHelper(root, word, 0);
        }

        private bool DeleteHelper(TrieNode node, string word, int index)
        {
            if (index == word.Length)
            {
                if (!node.IsEndOfWord)
                    return false;

                node.IsEndOfWord = false;
                Count--;
                return node.Children.Count == 0;
            }

            char c = word[index];
            if (!node.Children.ContainsKey(c))
                return false;

            bool shouldDeleteChild = DeleteHelper(node.Children[c], word, index + 1);

            if (shouldDeleteChild)
            {
                node.Children.Remove(c);
                return node.Children.Count == 0 && !node.IsEndOfWord;
            }

            return false;
        }

        public List<string> GetAllWords()
        {
            List<string> results = new List<string>();
            GetAllWords(root, "", results);
            return results;
        }
    }

    #endregion

    #region Graph

    /// <summary>
    /// Generic graph implementation with adjacency list
    /// </summary>
    public class Graph<T>
    {
        private readonly Dictionary<T, HashSet<T>> adjacencyList = new Dictionary<T, HashSet<T>>();
        private readonly bool isDirected;

        public int VertexCount => adjacencyList.Count;
        public bool IsDirected => isDirected;

        public Graph(bool directed = false)
        {
            isDirected = directed;
        }

        public void AddVertex(T vertex)
        {
            if (!adjacencyList.ContainsKey(vertex))
                adjacencyList[vertex] = new HashSet<T>();
        }

        public void AddEdge(T from, T to)
        {
            AddVertex(from);
            AddVertex(to);

            adjacencyList[from].Add(to);

            if (!isDirected)
                adjacencyList[to].Add(from);
        }

        public bool RemoveVertex(T vertex)
        {
            if (!adjacencyList.ContainsKey(vertex))
                return false;

            // Remove all edges to this vertex
            foreach (var neighbors in adjacencyList.Values)
                neighbors.Remove(vertex);

            // Remove the vertex
            return adjacencyList.Remove(vertex);
        }

        public bool RemoveEdge(T from, T to)
        {
            if (!adjacencyList.ContainsKey(from))
                return false;

            bool removed = adjacencyList[from].Remove(to);

            if (!isDirected && adjacencyList.ContainsKey(to))
                adjacencyList[to].Remove(from);

            return removed;
        }

        public IEnumerable<T> GetNeighbors(T vertex)
        {
            return adjacencyList.ContainsKey(vertex)
                ? adjacencyList[vertex]
                : Enumerable.Empty<T>();
        }

        public IEnumerable<T> GetVertices()
        {
            return adjacencyList.Keys;
        }

        public bool HasVertex(T vertex)
        {
            return adjacencyList.ContainsKey(vertex);
        }

        public bool HasEdge(T from, T to)
        {
            return adjacencyList.ContainsKey(from) && adjacencyList[from].Contains(to);
        }

        public int GetDegree(T vertex)
        {
            if (!adjacencyList.ContainsKey(vertex))
                return 0;

            if (!isDirected)
                return adjacencyList[vertex].Count;

            // For directed graphs, return in-degree + out-degree
            int outDegree = adjacencyList[vertex].Count;
            int inDegree = adjacencyList.Values.Count(neighbors => neighbors.Contains(vertex));

            return outDegree + inDegree;
        }
    }

    #endregion
}