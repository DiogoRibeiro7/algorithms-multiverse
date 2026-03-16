# Known Issues - Fortran Data Structures

## Hash Table (hashtable.f90) - RESOLVED

**Status**: Fixed
**Severity**: N/A (resolved)

### Problem

The hash table implementation encountered a segmentation fault during runtime when calling `init()` without an explicit capacity argument.

### Root Cause

Two issues were found:

1. **Parameter name shadowing (primary segfault cause)**: Fortran is case-insensitive, so the optional dummy argument `initial_capacity` in `ht_init` shadowed the module-level parameter `INITIAL_CAPACITY`. When the argument was not passed, the `else` branch read the non-present optional argument instead of the module constant, causing a segfault. Fixed by renaming the dummy argument to `init_cap`.

2. **Pointer array of derived types**: The `buckets` field was declared as `type(hash_node), dimension(:), pointer`, which can lead to unreliable behavior when elements contain pointers. Refactored to use a `bucket_head` wrapper type with an `allocatable` array.

3. **Non-recursive subroutine**: `ht_put` is called recursively from `ht_resize`, but Fortran subroutines are non-recursive by default. Fixed by adding the `recursive` keyword.

### Test Status

```text
All 6/6 tests passing (100%)
```

---

**Last Updated**: 2026-03-16
