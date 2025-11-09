/**
 * Binary Tree Implementation in Java
 * 
 * Time Complexity:
 * - Insert: O(log n) average, O(n) worst case
 * - Search: O(log n) average, O(n) worst case
 * - Delete: O(log n) average, O(n) worst case
 * 
 * Space Complexity: O(n) for storage, O(log n) for recursion stack
 * 
 * Java features:
 * - Generic types with bounded wildcards
 * - Object-oriented design patterns
 * - Iterator and Iterable interfaces
 * - Functional programming with Stream API
 * - Exception handling
 */

import java.util.*;
import java.util.function.*;
import java.util.stream.*;

/**
 * Generic Binary Search Tree implementation
 */
public class BinaryTree<T extends Comparable<T>> implements Iterable<T> {
    
    /**
     * TreeNode inner class
     */
    public static class TreeNode<T extends Comparable<T>> {
        T data;
        TreeNode<T> left;
        TreeNode<T> right;
        
        public TreeNode(T data) {
            this.data = data;
            this.left = null;
            this.right = null;
        }
        
        public T getData() { return data; }
        public TreeNode<T> getLeft() { return left; }
        public TreeNode<T> getRight() { return right; }
        
        @Override
        public String toString() {
            return data.toString();
        }
    }
    
    private TreeNode<T> root;
    private int size;
    
    // Event listeners for tree operations
    private final List<Consumer<T>> insertListeners = new ArrayList<>();
    private final List<Consumer<T>> deleteListeners = new ArrayList<>();
    private final List<Consumer<T>> searchListeners = new ArrayList<>();
    
    // Constructors
    public BinaryTree() {
        this.root = null;
        this.size = 0;
    }
    
    @SafeVarargs
    public BinaryTree(T... elements) {
        this();
        for (T element : elements) {
            insert(element);
        }
    }
    
    public BinaryTree(Collection<T> elements) {
        this();
        for (T element : elements) {
            insert(element);
        }
    }
    
    // MARK: - Core Operations
    
    /**
     * Insert a new element into the tree
     */
    public void insert(T data) {
        Objects.requireNonNull(data, "Data cannot be null");
        
        root = insertRecursive(root, data);
        size++;
        
        // Notify listeners
        insertListeners.forEach(listener -> listener.accept(data));
    }
    
    private TreeNode<T> insertRecursive(TreeNode<T> node, T data) {
        if (node == null) {
            return new TreeNode<>(data);
        }
        
        int comparison = data.compareTo(node.data);
        if (comparison < 0) {
            node.left = insertRecursive(node.left, data);
        } else {
            node.right = insertRecursive(node.right, data);
        }
        
        return node;
    }
    
    /**
     * Search for an element in the tree
     */
    public boolean search(T data) {
        Objects.requireNonNull(data, "Data cannot be null");
        
        // Notify listeners
        searchListeners.forEach(listener -> listener.accept(data));
        
        return searchRecursive(root, data);
    }
    
    private boolean searchRecursive(TreeNode<T> node, T data) {
        if (node == null) {
            return false;
        }
        
        int comparison = data.compareTo(node.data);
        if (comparison == 0) {
            return true;
        } else if (comparison < 0) {
            return searchRecursive(node.left, data);
        } else {
            return searchRecursive(node.right, data);
        }
    }
    
    /**
     * Delete an element from the tree
     */
    public boolean delete(T data) {
        Objects.requireNonNull(data, "Data cannot be null");
        
        int initialSize = size;
        root = deleteRecursive(root, data);
        
        boolean deleted = size < initialSize;
        if (deleted) {
            deleteListeners.forEach(listener -> listener.accept(data));
        }
        
        return deleted;
    }
    
    private TreeNode<T> deleteRecursive(TreeNode<T> node, T data) {
        if (node == null) {
            return null;
        }
        
        int comparison = data.compareTo(node.data);
        
        if (comparison < 0) {
            node.left = deleteRecursive(node.left, data);
        } else if (comparison > 0) {
            node.right = deleteRecursive(node.right, data);
        } else {
            // Node to delete found
            size--;
            
            if (node.left == null) {
                return node.right;
            } else if (node.right == null) {
                return node.left;
            } else {
                // Node has two children
                TreeNode<T> minNode = findMin(node.right);
                node.data = minNode.data;
                node.right = deleteRecursive(node.right, minNode.data);
                size++; // Compensate for the decrement above
            }
        }
        
        return node;
    }
    
    private TreeNode<T> findMin(TreeNode<T> node) {
        while (node.left != null) {
            node = node.left;
        }
        return node;
    }
    
    private TreeNode<T> findMax(TreeNode<T> node) {
        while (node.right != null) {
            node = node.right;
        }
        return node;
    }
    
    // MARK: - Tree Properties
    
    /**
     * Get the height of the tree
     */
    public int height() {
        return heightRecursive(root);
    }
    
    private int heightRecursive(TreeNode<T> node) {
        if (node == null) {
            return -1;
        }
        
        int leftHeight = heightRecursive(node.left);
        int rightHeight = heightRecursive(node.right);
        
        return 1 + Math.max(leftHeight, rightHeight);
    }
    
    /**
     * Get the depth of a specific element
     */
    public int depth(T data) {
        Objects.requireNonNull(data, "Data cannot be null");
        return depthRecursive(root, data, 0);
    }
    
    private int depthRecursive(TreeNode<T> node, T data, int currentDepth) {
        if (node == null) {
            return -1;
        }
        
        int comparison = data.compareTo(node.data);
        if (comparison == 0) {
            return currentDepth;
        } else if (comparison < 0) {
            return depthRecursive(node.left, data, currentDepth + 1);
        } else {
            return depthRecursive(node.right, data, currentDepth + 1);
        }
    }
    
    /**
     * Check if the tree is balanced
     */
    public boolean isBalanced() {
        return isBalancedRecursive(root).isBalanced;
    }
    
    private BalanceResult isBalancedRecursive(TreeNode<T> node) {
        if (node == null) {
            return new BalanceResult(true, -1);
        }
        
        BalanceResult leftResult = isBalancedRecursive(node.left);
        BalanceResult rightResult = isBalancedRecursive(node.right);
        
        boolean balanced = leftResult.isBalanced && 
                          rightResult.isBalanced && 
                          Math.abs(leftResult.height - rightResult.height) <= 1;
        
        int height = 1 + Math.max(leftResult.height, rightResult.height);
        
        return new BalanceResult(balanced, height);
    }
    
    private static class BalanceResult {
        final boolean isBalanced;
        final int height;
        
        BalanceResult(boolean isBalanced, int height) {
            this.isBalanced = isBalanced;
            this.height = height;
        }
    }
    
    /**
     * Count the number of leaf nodes
     */
    public int countLeaves() {
        return countLeavesRecursive(root);
    }
    
    private int countLeavesRecursive(TreeNode<T> node) {
        if (node == null) {
            return 0;
        }
        
        if (node.left == null && node.right == null) {
            return 1;
        }
        
        return countLeavesRecursive(node.left) + countLeavesRecursive(node.right);
    }
    
    // MARK: - Traversal Methods
    
    /**
     * In-order traversal
     */
    public List<T> inorderTraversal() {
        List<T> result = new ArrayList<>();
        inorderRecursive(root, result);
        return result;
    }
    
    private void inorderRecursive(TreeNode<T> node, List<T> result) {
        if (node != null) {
            inorderRecursive(node.left, result);
            result.add(node.data);
            inorderRecursive(node.right, result);
        }
    }
    
    /**
     * Pre-order traversal
     */
    public List<T> preorderTraversal() {
        List<T> result = new ArrayList<>();
        preorderRecursive(root, result);
        return result;
    }
    
    private void preorderRecursive(TreeNode<T> node, List<T> result) {
        if (node != null) {
            result.add(node.data);
            preorderRecursive(node.left, result);
            preorderRecursive(node.right, result);
        }
    }
    
    /**
     * Post-order traversal
     */
    public List<T> postorderTraversal() {
        List<T> result = new ArrayList<>();
        postorderRecursive(root, result);
        return result;
    }
    
    private void postorderRecursive(TreeNode<T> node, List<T> result) {
        if (node != null) {
            postorderRecursive(node.left, result);
            postorderRecursive(node.right, result);
            result.add(node.data);
        }
    }
    
    /**
     * Level-order (breadth-first) traversal
     */
    public List<T> levelOrderTraversal() {
        List<T> result = new ArrayList<>();
        if (root == null) return result;
        
        Queue<TreeNode<T>> queue = new LinkedList<>();
        queue.offer(root);
        
        while (!queue.isEmpty()) {
            TreeNode<T> node = queue.poll();
            result.add(node.data);
            
            if (node.left != null) {
                queue.offer(node.left);
            }
            if (node.right != null) {
                queue.offer(node.right);
            }
        }
        
        return result;
    }
    
    // MARK: - Advanced Operations
    
    /**
     * Find the lowest common ancestor of two nodes
     */
    public Optional<T> lowestCommonAncestor(T data1, T data2) {
        Objects.requireNonNull(data1, "First data cannot be null");
        Objects.requireNonNull(data2, "Second data cannot be null");
        
        TreeNode<T> lca = lcaRecursive(root, data1, data2);
        return lca != null ? Optional.of(lca.data) : Optional.empty();
    }
    
    private TreeNode<T> lcaRecursive(TreeNode<T> node, T data1, T data2) {
        if (node == null) {
            return null;
        }
        
        int comp1 = data1.compareTo(node.data);
        int comp2 = data2.compareTo(node.data);
        
        if (comp1 < 0 && comp2 < 0) {
            return lcaRecursive(node.left, data1, data2);
        } else if (comp1 > 0 && comp2 > 0) {
            return lcaRecursive(node.right, data1, data2);
        } else {
            return node;
        }
    }
    
    /**
     * Get path from root to a specific node
     */
    public Optional<List<T>> getPathToNode(T data) {
        Objects.requireNonNull(data, "Data cannot be null");
        
        List<T> path = new ArrayList<>();
        if (findPath(root, data, path)) {
            return Optional.of(path);
        }
        return Optional.empty();
    }
    
    private boolean findPath(TreeNode<T> node, T data, List<T> path) {
        if (node == null) {
            return false;
        }
        
        path.add(node.data);
        
        if (node.data.compareTo(data) == 0) {
            return true;
        }
        
        int comparison = data.compareTo(node.data);
        if (comparison < 0 && findPath(node.left, data, path)) {
            return true;
        }
        
        if (comparison > 0 && findPath(node.right, data, path)) {
            return true;
        }
        
        path.remove(path.size() - 1);
        return false;
    }
    
    /**
     * Validate if the tree is a valid BST
     */
    public boolean isValidBST() {
        return isValidBSTRecursive(root, null, null);
    }
    
    private boolean isValidBSTRecursive(TreeNode<T> node, T minVal, T maxVal) {
        if (node == null) {
            return true;
        }
        
        if (minVal != null && node.data.compareTo(minVal) <= 0) {
            return false;
        }
        
        if (maxVal != null && node.data.compareTo(maxVal) >= 0) {
            return false;
        }
        
        return isValidBSTRecursive(node.left, minVal, node.data) &&
               isValidBSTRecursive(node.right, node.data, maxVal);
    }
    
    // MARK: - Utility Methods
    
    /**
     * Get all nodes at a specific level
     */
    public List<T> getNodesAtLevel(int level) {
        List<T> result = new ArrayList<>();
        getNodesAtLevelRecursive(root, level, 0, result);
        return result;
    }
    
    private void getNodesAtLevelRecursive(TreeNode<T> node, int targetLevel, 
                                         int currentLevel, List<T> result) {
        if (node == null) {
            return;
        }
        
        if (currentLevel == targetLevel) {
            result.add(node.data);
        } else {
            getNodesAtLevelRecursive(node.left, targetLevel, currentLevel + 1, result);
            getNodesAtLevelRecursive(node.right, targetLevel, currentLevel + 1, result);
        }
    }
    
    /**
     * Pretty print the tree structure
     */
    public void prettyPrint() {
        if (root == null) {
            System.out.println("Empty tree");
            return;
        }
        prettyPrintRecursive(root, "", true);
    }
    
    private void prettyPrintRecursive(TreeNode<T> node, String prefix, boolean isLast) {
        if (node != null) {
            System.out.println(prefix + (isLast ? "└── " : "├── ") + node.data);
            
            List<TreeNode<T>> children = Arrays.asList(node.left, node.right)
                                               .stream()
                                               .filter(Objects::nonNull)
                                               .collect(Collectors.toList());
            
            for (int i = 0; i < children.size(); i++) {
                boolean isLastChild = i == children.size() - 1;
                String extension = isLast ? "    " : "│   ";
                prettyPrintRecursive(children.get(i), prefix + extension, isLastChild);
            }
        }
    }
    
    // MARK: - Stream API Integration
    
    /**
     * Get a stream of all elements (in-order)
     */
    public Stream<T> stream() {
        return inorderTraversal().stream();
    }
    
    /**
     * Filter elements based on a predicate
     */
    public List<T> filter(Predicate<T> predicate) {
        return stream().filter(predicate).collect(Collectors.toList());
    }
    
    /**
     * Map elements to another type
     */
    public <R> List<R> map(Function<T, R> mapper) {
        return stream().map(mapper).collect(Collectors.toList());
    }
    
    // MARK: - Event Listeners
    
    public void addInsertListener(Consumer<T> listener) {
        insertListeners.add(listener);
    }
    
    public void addDeleteListener(Consumer<T> listener) {
        deleteListeners.add(listener);
    }
    
    public void addSearchListener(Consumer<T> listener) {
        searchListeners.add(listener);
    }
    
    // MARK: - Accessors
    
    public int size() { return size; }
    public boolean isEmpty() { return size == 0; }
    public TreeNode<T> getRoot() { return root; }
    
    // MARK: - Iterable Implementation
    
    @Override
    public Iterator<T> iterator() {
        return inorderTraversal().iterator();
    }
    
    // MARK: - Object Methods
    
    @Override
    public String toString() {
        return "BinaryTree" + inorderTraversal();
    }
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        
        BinaryTree<?> that = (BinaryTree<?>) obj;
        return this.inorderTraversal().equals(that.inorderTraversal());
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(inorderTraversal());
    }
    
    // MARK: - Static Factory Methods
    
    public static <T extends Comparable<T>> BinaryTree<T> fromArray(T[] array) {
        return new BinaryTree<>(Arrays.asList(array));
    }
    
    public static <T extends Comparable<T>> BinaryTree<T> fromSortedArray(T[] sortedArray) {
        BinaryTree<T> tree = new BinaryTree<>();
        tree.root = buildBalancedFromSorted(sortedArray, 0, sortedArray.length - 1);
        tree.size = sortedArray.length;
        return tree;
    }
    
    private static <T extends Comparable<T>> TreeNode<T> buildBalancedFromSorted(
            T[] array, int start, int end) {
        if (start > end) {
            return null;
        }
        
        int mid = (start + end) / 2;
        TreeNode<T> node = new TreeNode<>(array[mid]);
        
        node.left = buildBalancedFromSorted(array, start, mid - 1);
        node.right = buildBalancedFromSorted(array, mid + 1, end);
        
        return node;
    }
}

/**
 * Demonstration and testing class
 */
class BinaryTreeDemo {
    
    public static void main(String[] args) {
        System.out.println("🌳 Binary Tree Implementation in Java");
        System.out.println("=".repeat(45));
        
        demonstrateBasicOperations();
        demonstrateAdvancedFeatures();
        testPerformance();
        
        System.out.println("\n✨ Binary Tree demonstration complete!");
    }
    
    private static void demonstrateBasicOperations() {
        System.out.println("\n📋 Basic Operations");
        System.out.println("-".repeat(25));
        
        BinaryTree<Integer> tree = new BinaryTree<>(50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45);
        
        System.out.println("Tree size: " + tree.size());
        System.out.println("Tree height: " + tree.height());
        System.out.println("Is balanced: " + tree.isBalanced());
        System.out.println("Is valid BST: " + tree.isValidBST());
        
        // Visual representation
        System.out.println("\nTree Structure:");
        tree.prettyPrint();
        
        // Traversals
        System.out.println("\nTraversals:");
        System.out.println("In-order:    " + tree.inorderTraversal());
        System.out.println("Pre-order:   " + tree.preorderTraversal());
        System.out.println("Post-order:  " + tree.postorderTraversal());
        System.out.println("Level-order: " + tree.levelOrderTraversal());
        
        // Search operations
        System.out.println("\nSearch Operations:");
        int[] searchValues = {25, 75, 50, 100};
        for (int value : searchValues) {
            boolean found = tree.search(value);
            int depth = found ? tree.depth(value) : -1;
            System.out.printf("Search %d: %s (depth: %d)%n", 
                            value, found ? "Found" : "Not found", depth);
        }
    }
    
    private static void demonstrateAdvancedFeatures() {
        System.out.println("\n🎯 Advanced Features");
        System.out.println("-".repeat(25));
        
        BinaryTree<Integer> tree = new BinaryTree<>(50, 30, 70, 20, 40, 60, 80);
        
        // Advanced operations
        Optional<Integer> lca = tree.lowestCommonAncestor(20, 40);
        lca.ifPresent(value -> System.out.println("LCA of 20 and 40: " + value));
        
        Optional<List<Integer>> path = tree.getPathToNode(40);
        path.ifPresent(p -> System.out.println("Path to 40: " + p));
        
        // Level operations
        System.out.println("\nNodes by level:");
        for (int level = 0; level <= tree.height(); level++) {
            List<Integer> nodes = tree.getNodesAtLevel(level);
            System.out.printf("Level %d: %s%n", level, nodes);
        }
        
        // Stream API operations
        System.out.println("\nStream API operations:");
        List<Integer> evenNumbers = tree.filter(n -> n % 2 == 0);
        System.out.println("Even numbers: " + evenNumbers);
        
        List<String> strings = tree.map(n -> "Item-" + n);
        System.out.println("Mapped to strings: " + strings);
        
        // String tree
        BinaryTree<String> stringTree = new BinaryTree<>("dog", "cat", "fish", "bird", "elephant");
        System.out.println("\nString tree: " + stringTree.inorderTraversal());
        
        // Event listeners
        BinaryTree<Integer> eventTree = new BinaryTree<>();
        eventTree.addInsertListener(value -> System.out.println("Inserted: " + value));
        eventTree.addSearchListener(value -> System.out.println("Searched: " + value));
        
        System.out.println("\nInserting with events:");
        eventTree.insert(10);
        eventTree.insert(5);
        eventTree.search(10);
    }
    
    private static void testPerformance() {
        System.out.println("\n⚡ Performance Testing");
        System.out.println("-".repeat(25));
        
        int[] sizes = {1000, 5000, 10000};
        
        for (int size : sizes) {
            System.out.printf("\nTesting with %,d elements:%n", size);
            
            // Generate test data
            List<Integer> testData = new Random().ints(size, 1, size * 2)
                                                 .boxed()
                                                 .collect(Collectors.toList());
            
            BinaryTree<Integer> tree = new BinaryTree<>();
            
            // Test insertion
            long startTime = System.nanoTime();
            testData.forEach(tree::insert);
            long insertTime = (System.nanoTime() - startTime) / 1_000_000;
            
            // Test search
            List<Integer> searchData = testData.subList(0, Math.min(100, testData.size()));
            startTime = System.nanoTime();
            searchData.forEach(tree::search);
            long searchTime = (System.nanoTime() - startTime) / 1_000_000;
            
            System.out.printf("  Insertion: %d ms%n", insertTime);
            System.out.printf("  Search:    %d ms%n", searchTime);
            System.out.printf("  Height:    %d%n", tree.height());
            System.out.printf("  Balanced:  %s%n", tree.isBalanced());
        }
    }
}
