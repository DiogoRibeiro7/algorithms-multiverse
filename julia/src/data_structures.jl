"""
    DataStructures

Module containing fundamental data structures implemented in Julia.
"""
module DataStructures

export Stack, Queue, Deque, LinkedList, BinarySearchTree, MinHeap, MaxHeap,
       Trie, UnionFind, push!, pop!, enqueue!, dequeue!, insert!, delete!,
       search, isempty, size

# Stack - LIFO data structure
mutable struct Stack{T}
    items::Vector{T}

    Stack{T}() where T = new(Vector{T}())
end

Base.push!(s::Stack, item) = push!(s.items, item)
Base.pop!(s::Stack) = isempty(s.items) ? nothing : pop!(s.items)
Base.isempty(s::Stack) = isempty(s.items)
Base.size(s::Stack) = length(s.items)
peek(s::Stack) = isempty(s.items) ? nothing : s.items[end]

# Queue - FIFO data structure
mutable struct Queue{T}
    items::Vector{T}

    Queue{T}() where T = new(Vector{T}())
end

enqueue!(q::Queue, item) = push!(q.items, item)
dequeue!(q::Queue) = isempty(q.items) ? nothing : popfirst!(q.items)
Base.isempty(q::Queue) = isempty(q.items)
Base.size(q::Queue) = length(q.items)
front(q::Queue) = isempty(q.items) ? nothing : q.items[1]

# Binary Search Tree Node
mutable struct TreeNode{T}
    data::T
    left::Union{TreeNode{T}, Nothing}
    right::Union{TreeNode{T}, Nothing}

    TreeNode(data::T) where T = new{T}(data, nothing, nothing)
end

# Binary Search Tree
mutable struct BinarySearchTree{T}
    root::Union{TreeNode{T}, Nothing}

    BinarySearchTree{T}() where T = new(nothing)
end

function insert!(bst::BinarySearchTree{T}, data::T) where T
    if bst.root === nothing
        bst.root = TreeNode(data)
    else
        insert_node!(bst.root, data)
    end
end

function insert_node!(node::TreeNode{T}, data::T) where T
    if data < node.data
        if node.left === nothing
            node.left = TreeNode(data)
        else
            insert_node!(node.left, data)
        end
    elseif data > node.data
        if node.right === nothing
            node.right = TreeNode(data)
        else
            insert_node!(node.right, data)
        end
    end
end

function search(bst::BinarySearchTree{T}, data::T) where T
    return search_node(bst.root, data)
end

function search_node(node::Union{TreeNode{T}, Nothing}, data::T) where T
    if node === nothing
        return false
    elseif data == node.data
        return true
    elseif data < node.data
        return search_node(node.left, data)
    else
        return search_node(node.right, data)
    end
end

function inorder(bst::BinarySearchTree)
    result = []
    inorder_traverse(bst.root, result)
    return result
end

function inorder_traverse(node::Union{TreeNode, Nothing}, result)
    if node !== nothing
        inorder_traverse(node.left, result)
        push!(result, node.data)
        inorder_traverse(node.right, result)
    end
end

# Min Heap
mutable struct MinHeap{T}
    items::Vector{T}

    MinHeap{T}() where T = new(Vector{T}())
end

function Base.push!(heap::MinHeap, item)
    push!(heap.items, item)
    bubble_up!(heap, length(heap.items))
end

function Base.pop!(heap::MinHeap)
    if isempty(heap.items)
        return nothing
    elseif length(heap.items) == 1
        return pop!(heap.items)
    else
        min_item = heap.items[1]
        heap.items[1] = pop!(heap.items)
        bubble_down!(heap, 1)
        return min_item
    end
end

function bubble_up!(heap::MinHeap, idx)
    parent_idx = idx ÷ 2
    if idx > 1 && heap.items[idx] < heap.items[parent_idx]
        heap.items[idx], heap.items[parent_idx] = heap.items[parent_idx], heap.items[idx]
        bubble_up!(heap, parent_idx)
    end
end

function bubble_down!(heap::MinHeap, idx)
    n = length(heap.items)
    smallest = idx
    left = 2 * idx
    right = 2 * idx + 1

    if left <= n && heap.items[left] < heap.items[smallest]
        smallest = left
    end

    if right <= n && heap.items[right] < heap.items[smallest]
        smallest = right
    end

    if smallest != idx
        heap.items[idx], heap.items[smallest] = heap.items[smallest], heap.items[idx]
        bubble_down!(heap, smallest)
    end
end

Base.isempty(heap::MinHeap) = isempty(heap.items)
Base.size(heap::MinHeap) = length(heap.items)

# Trie Node
mutable struct TrieNode
    children::Dict{Char, TrieNode}
    is_end::Bool

    TrieNode() = new(Dict{Char, TrieNode}(), false)
end

# Trie
mutable struct Trie
    root::TrieNode

    Trie() = new(TrieNode())
end

function insert!(trie::Trie, word::String)
    node = trie.root
    for char in word
        if !haskey(node.children, char)
            node.children[char] = TrieNode()
        end
        node = node.children[char]
    end
    node.is_end = true
end

function search(trie::Trie, word::String)
    node = trie.root
    for char in word
        if !haskey(node.children, char)
            return false
        end
        node = node.children[char]
    end
    return node.is_end
end

function starts_with(trie::Trie, prefix::String)
    node = trie.root
    for char in prefix
        if !haskey(node.children, char)
            return false
        end
        node = node.children[char]
    end
    return true
end

# Union-Find (Disjoint Set)
mutable struct UnionFind
    parent::Vector{Int}
    rank::Vector{Int}

    function UnionFind(n::Int)
        parent = collect(1:n)
        rank = zeros(Int, n)
        new(parent, rank)
    end
end

function find!(uf::UnionFind, x::Int)
    if uf.parent[x] != x
        uf.parent[x] = find!(uf, uf.parent[x])  # Path compression
    end
    return uf.parent[x]
end

function union!(uf::UnionFind, x::Int, y::Int)
    root_x = find!(uf, x)
    root_y = find!(uf, y)

    if root_x == root_y
        return
    end

    # Union by rank
    if uf.rank[root_x] < uf.rank[root_y]
        uf.parent[root_x] = root_y
    elseif uf.rank[root_x] > uf.rank[root_y]
        uf.parent[root_y] = root_x
    else
        uf.parent[root_y] = root_x
        uf.rank[root_x] += 1
    end
end

function connected(uf::UnionFind, x::Int, y::Int)
    return find!(uf, x) == find!(uf, y)
end

end # module DataStructures