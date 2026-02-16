! Test suite for data structures module
program test_data_structures_module
    use iso_fortran_env, only: int32, real64
    use data_structures_module
    implicit none

    integer :: total_tests = 0, passed_tests = 0

    print '(A)', "========================================"
    print '(A)', "    Data Structures Module Test Suite"
    print '(A)', "========================================"

    call test_stack()
    call test_queue()
    call test_priority_queue()
    call test_linked_lists()
    call test_trees()
    call test_hash_table()
    call test_advanced_structures()

    print '(A)', ""
    print '(A)', "========================================"
    print '(A,I0,A,I0)', "Tests passed: ", passed_tests, "/", total_tests
    if (passed_tests == total_tests) then
        print '(A)', "STATUS: ALL TESTS PASSED ✓"
    else
        print '(A)', "STATUS: SOME TESTS FAILED ✗"
    end if
    print '(A)', "========================================"

contains

    subroutine test_stack()
        type(stack_type) :: stack
        integer :: value
        logical :: is_empty, success

        print '(A)', ""
        print '(A)', "Testing Stack Operations..."

        ! Initialize stack
        call stack_init(stack, 10)

        ! Test empty stack
        is_empty = stack_is_empty(stack)
        success = is_empty
        call report_test("Stack initially empty", success)

        ! Test push
        call stack_push(stack, 5)
        call stack_push(stack, 10)
        call stack_push(stack, 15)
        success = stack_size(stack) == 3
        call report_test("Stack push operation", success)

        ! Test peek
        value = stack_peek(stack)
        success = value == 15
        call report_test("Stack peek operation", success)

        ! Test pop
        value = stack_pop(stack)
        success = value == 15 .and. stack_size(stack) == 2
        call report_test("Stack pop operation", success)

        ! Test multiple operations
        value = stack_pop(stack)
        value = stack_pop(stack)
        is_empty = stack_is_empty(stack)
        success = is_empty
        call report_test("Stack empty after pops", success)

        call stack_destroy(stack)

    end subroutine test_stack

    subroutine test_queue()
        type(queue_type) :: queue
        integer :: value
        logical :: is_empty, success

        print '(A)', ""
        print '(A)', "Testing Queue Operations..."

        ! Initialize queue
        call queue_init(queue, 10)

        ! Test empty queue
        is_empty = queue_is_empty(queue)
        success = is_empty
        call report_test("Queue initially empty", success)

        ! Test enqueue
        call queue_enqueue(queue, 5)
        call queue_enqueue(queue, 10)
        call queue_enqueue(queue, 15)
        success = queue_size(queue) == 3
        call report_test("Queue enqueue operation", success)

        ! Test dequeue (FIFO)
        value = queue_dequeue(queue)
        success = value == 5
        call report_test("Queue dequeue (FIFO)", success)

        value = queue_dequeue(queue)
        success = value == 10 .and. queue_size(queue) == 1
        call report_test("Queue size after dequeue", success)

        call queue_destroy(queue)

    end subroutine test_queue

    subroutine test_priority_queue()
        type(priority_queue_type) :: pq
        integer :: value
        logical :: success

        print '(A)', ""
        print '(A)', "Testing Priority Queue Operations..."

        ! Initialize priority queue (min-heap)
        call pq_init(pq, 10, .true.)

        ! Test insertion
        call pq_insert(pq, 10, 10.0_real64)
        call pq_insert(pq, 5, 5.0_real64)
        call pq_insert(pq, 20, 20.0_real64)
        call pq_insert(pq, 3, 3.0_real64)

        success = pq_size(pq) == 4
        call report_test("Priority queue insertion", success)

        ! Test extraction (min-heap should return smallest)
        value = pq_extract(pq)
        success = value == 3
        call report_test("Priority queue extract min", success)

        value = pq_extract(pq)
        success = value == 5
        call report_test("Priority queue ordered extraction", success)

        call pq_destroy(pq)

        ! Test max-heap
        call pq_init(pq, 10, .false.)
        call pq_insert(pq, 10, 10.0_real64)
        call pq_insert(pq, 5, 5.0_real64)
        call pq_insert(pq, 20, 20.0_real64)

        value = pq_extract(pq)
        success = value == 20
        call report_test("Priority queue extract max", success)

        call pq_destroy(pq)

    end subroutine test_priority_queue

    subroutine test_linked_lists()
        type(linked_list_type) :: list
        type(doubly_linked_list_type) :: dlist
        integer :: value
        logical :: found, success

        print '(A)', ""
        print '(A)', "Testing Linked List Operations..."

        ! Test singly linked list
        call list_init(list)
        call list_insert(list, 10)
        call list_insert(list, 20)
        call list_insert(list, 30)

        success = list_size(list) == 3
        call report_test("Linked list insertion", success)

        found = list_search(list, 20)
        success = found
        call report_test("Linked list search (found)", success)

        found = list_search(list, 40)
        success = .not. found
        call report_test("Linked list search (not found)", success)

        call list_delete(list, 20)
        success = list_size(list) == 2
        call report_test("Linked list deletion", success)

        call list_destroy(list)

        ! Test doubly linked list
        call dlist_init(dlist)
        call dlist_insert_front(dlist, 10)
        call dlist_insert_back(dlist, 30)
        call dlist_insert_front(dlist, 5)

        value = dlist_front(dlist)
        success = value == 5
        call report_test("Doubly linked list front", success)

        value = dlist_back(dlist)
        success = value == 30
        call report_test("Doubly linked list back", success)

        call dlist_destroy(dlist)

    end subroutine test_linked_lists

    subroutine test_trees()
        type(bst_type) :: bst
        type(avl_tree_type) :: avl
        integer :: height
        logical :: found, success

        print '(A)', ""
        print '(A)', "Testing Tree Operations..."

        ! Test Binary Search Tree
        call bst_init(bst)
        call bst_insert(bst, 50)
        call bst_insert(bst, 30)
        call bst_insert(bst, 70)
        call bst_insert(bst, 20)
        call bst_insert(bst, 40)

        found = bst_search(bst, 40)
        success = found
        call report_test("BST search (found)", success)

        found = bst_search(bst, 25)
        success = .not. found
        call report_test("BST search (not found)", success)

        call bst_delete(bst, 30)
        found = bst_search(bst, 30)
        success = .not. found
        call report_test("BST deletion", success)

        call bst_destroy(bst)

        ! Test AVL Tree
        call avl_init(avl)
        call avl_insert(avl, 10)
        call avl_insert(avl, 20)
        call avl_insert(avl, 30)
        call avl_insert(avl, 40)
        call avl_insert(avl, 50)

        height = avl_height(avl)
        success = height <= 3  ! AVL tree should be balanced
        call report_test("AVL tree balancing", success)

        found = avl_search(avl, 30)
        success = found
        call report_test("AVL tree search", success)

        call avl_destroy(avl)

    end subroutine test_trees

    subroutine test_hash_table()
        type(hash_table_type) :: ht
        integer :: value
        logical :: found, success

        print '(A)', ""
        print '(A)', "Testing Hash Table Operations..."

        ! Initialize hash table
        call hash_table_init(ht, 100)

        ! Test insertion
        call hash_table_insert(ht, "key1", 100)
        call hash_table_insert(ht, "key2", 200)
        call hash_table_insert(ht, "key3", 300)

        success = hash_table_size(ht) == 3
        call report_test("Hash table insertion", success)

        ! Test retrieval
        value = hash_table_get(ht, "key2", found)
        success = found .and. value == 200
        call report_test("Hash table get (found)", success)

        value = hash_table_get(ht, "key4", found)
        success = .not. found
        call report_test("Hash table get (not found)", success)

        ! Test deletion
        call hash_table_delete(ht, "key2")
        value = hash_table_get(ht, "key2", found)
        success = .not. found
        call report_test("Hash table deletion", success)

        ! Test collision handling
        call hash_table_insert(ht, "abc", 111)
        call hash_table_insert(ht, "bca", 222)  ! Might collide depending on hash
        value = hash_table_get(ht, "abc", found)
        success = found .and. value == 111
        call report_test("Hash table collision handling", success)

        call hash_table_destroy(ht)

    end subroutine test_hash_table

    subroutine test_advanced_structures()
        type(trie_type) :: trie
        type(disjoint_set_type) :: dset
        type(segment_tree_type) :: segtree
        type(fenwick_tree_type) :: fenwick
        integer :: arr(8), value
        logical :: found, success

        print '(A)', ""
        print '(A)', "Testing Advanced Data Structures..."

        ! Test Trie
        call trie_init(trie)
        call trie_insert(trie, "hello")
        call trie_insert(trie, "help")
        call trie_insert(trie, "world")

        found = trie_search(trie, "help")
        success = found
        call report_test("Trie search (found)", success)

        found = trie_search(trie, "hell")
        success = .not. found  ! "hell" is not a complete word
        call report_test("Trie search (prefix not word)", success)

        call trie_destroy(trie)

        ! Test Disjoint Set (Union-Find)
        call disjoint_set_init(dset, 10)
        call disjoint_set_union(dset, 1, 2)
        call disjoint_set_union(dset, 2, 3)
        call disjoint_set_union(dset, 4, 5)

        success = disjoint_set_find(dset, 1) == disjoint_set_find(dset, 3)
        call report_test("Disjoint set union-find", success)

        success = disjoint_set_find(dset, 1) /= disjoint_set_find(dset, 4)
        call report_test("Disjoint set separate sets", success)

        call disjoint_set_destroy(dset)

        ! Test Segment Tree
        arr = [1, 3, 5, 7, 9, 11, 13, 15]
        call segment_tree_build(segtree, arr, 8)

        value = segment_tree_query(segtree, 2, 5)  ! Sum of arr[2:5]
        success = value == (5 + 7 + 9 + 11)  ! = 32
        call report_test("Segment tree range query", success)

        call segment_tree_update(segtree, 3, 10)  ! Change arr[3] from 7 to 10
        value = segment_tree_query(segtree, 2, 5)
        success = value == (5 + 10 + 9 + 11)  ! = 35
        call report_test("Segment tree update", success)

        call segment_tree_destroy(segtree)

        ! Test Fenwick Tree (Binary Indexed Tree)
        call fenwick_tree_build(fenwick, arr, 8)

        value = fenwick_tree_query(fenwick, 4)  ! Sum of first 4 elements
        success = value == (1 + 3 + 5 + 10)  ! Note: arr[3] was updated above
        call report_test("Fenwick tree prefix sum", success)

        call fenwick_tree_update(fenwick, 2, 2)  ! Add 2 to position 2
        value = fenwick_tree_query(fenwick, 4)
        success = value == (1 + 5 + 5 + 10)  ! = 21
        call report_test("Fenwick tree update", success)

        call fenwick_tree_destroy(fenwick)

    end subroutine test_advanced_structures

    subroutine report_test(test_name, success)
        character(len=*), intent(in) :: test_name
        logical, intent(in) :: success

        total_tests = total_tests + 1
        if (success) then
            passed_tests = passed_tests + 1
            print '(A,A,A)', "  ✓ ", test_name, " ... PASSED"
        else
            print '(A,A,A)', "  ✗ ", test_name, " ... FAILED"
        end if
    end subroutine report_test

end program test_data_structures_module