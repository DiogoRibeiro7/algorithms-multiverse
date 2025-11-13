# Known Issues - Fortran Data Structures

## Hash Table (hashtable.f90) - Runtime Segmentation Fault

**Status**: Requires refactoring
**Severity**: High (prevents execution)
**Affects**: Pre-existing code (not new implementations)

### Problem

The hash table implementation encounters a segmentation fault during runtime when trying to access the buckets array. The program compiles successfully but crashes on the first `put()` operation.

### Root Cause

The implementation uses a pointer to an array of `hash_node` structures:
```fortran
type(hash_node), dimension(:), pointer :: buckets => null()
```

When allocating this array and accessing elements, Fortran's handling of pointer arrays can lead to undefined behavior, particularly when:
1. The bucket array elements are used as dummy head nodes
2. Each bucket's `next` pointer forms the actual linked list

### Recommended Fix

Refactor to use one of these approaches:

**Option 1**: Array of head pointers (requires Fortran 2003+ allocatable)
```fortran
type :: bucket_head
    type(hash_node), pointer :: head => null()
end type

type(bucket_head), allocatable :: buckets(:)
```

**Option 2**: Single linked list with bucket indexing
```fortran
type(hash_node), pointer :: head => null()
! Store bucket index in each node
```

**Option 3**: Use allocatable array instead of pointer
```fortran
type(hash_node), allocatable :: buckets(:)
```

### Workaround

For now, the hash table test is skipped. All other data structures (BST, Stack, Queue, Trie, Linked List) work correctly.

### Test Status

```
✅ Linked List - Passing
❌ Hash Table - Segfault (known issue)
✅ Binary Search Tree - Passing
✅ Stack - Passing
✅ Queue - Passing
✅ Trie - Passing

Overall: 5/6 tests passing (83.3%)
```

---

**Note**: All newly implemented data structures (BST, Stack, Queue, Trie) are fully functional and tested. This issue only affects pre-existing code.

**Last Updated**: 2025-01-13
