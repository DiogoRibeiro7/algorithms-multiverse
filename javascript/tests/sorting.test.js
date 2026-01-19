/**
 * Test suite for sorting algorithms
 */

import * as sorting from '../src/sorting.js';

// Test utilities
function isSorted(arr, compareFunc = (a, b) => a - b) {
    for (let i = 1; i < arr.length; i++) {
        if (compareFunc(arr[i-1], arr[i]) > 0) {
            return false;
        }
    }
    return true;
}

function runSortTest(sortFunc, name) {
    console.log(`Testing ${name}...`);

    // Test empty array
    let result = sortFunc([]);
    console.assert(result.length === 0, `${name} failed on empty array`);

    // Test single element
    result = sortFunc([1]);
    console.assert(JSON.stringify(result) === '[1]', `${name} failed on single element`);

    // Test already sorted
    result = sortFunc([1, 2, 3, 4, 5]);
    console.assert(isSorted(result), `${name} failed on sorted array`);

    // Test reverse sorted
    result = sortFunc([5, 4, 3, 2, 1]);
    console.assert(isSorted(result), `${name} failed on reverse sorted array`);

    // Test duplicates
    result = sortFunc([3, 1, 4, 1, 5, 9, 2, 6, 5, 3]);
    console.assert(isSorted(result), `${name} failed on array with duplicates`);

    // Test negative numbers
    result = sortFunc([-5, -2, -8, 0, 3, -1]);
    console.assert(isSorted(result), `${name} failed on negative numbers`);

    // Test large array
    const large = Array.from({length: 100}, () => Math.floor(Math.random() * 1000));
    result = sortFunc(large);
    console.assert(isSorted(result), `${name} failed on large random array`);

    // Test custom comparator (descending)
    result = sortFunc([3, 1, 4, 1, 5], (a, b) => b - a);
    console.assert(isSorted(result, (a, b) => b - a), `${name} failed with custom comparator`);

    console.log(`✓ ${name} passed all tests`);
}

// Run tests for all sorting algorithms
console.log('=== SORTING ALGORITHMS TESTS ===\n');

runSortTest(sorting.bubbleSort, 'bubbleSort');
runSortTest(sorting.insertionSort, 'insertionSort');
runSortTest(sorting.selectionSort, 'selectionSort');
runSortTest(sorting.mergeSort, 'mergeSort');
runSortTest(sorting.quickSort, 'quickSort');
runSortTest(sorting.heapSort, 'heapSort');
runSortTest(sorting.shellSort, 'shellSort');
runSortTest(sorting.cocktailSort, 'cocktailSort');
runSortTest(sorting.combSort, 'combSort');
runSortTest(sorting.gnomeSort, 'gnomeSort');
runSortTest(sorting.cycleSort, 'cycleSort');
runSortTest(sorting.oddEvenSort, 'oddEvenSort');
runSortTest(sorting.bitonicSort, 'bitonicSort');

// Special tests for integer-only sorts
console.log('\n=== INTEGER SORTING ALGORITHMS ===\n');

function runIntegerSortTest(sortFunc, name) {
    console.log(`Testing ${name}...`);

    // Test with small range
    let result = sortFunc([3, 1, 4, 1, 5, 9, 2, 6]);
    console.assert(isSorted(result), `${name} failed on small range`);

    // Test with zeros
    result = sortFunc([0, 5, 0, 3, 0, 1]);
    console.assert(isSorted(result), `${name} failed with zeros`);

    console.log(`✓ ${name} passed all tests`);
}

runIntegerSortTest(sorting.countingSort, 'countingSort');
runIntegerSortTest(sorting.radixSort, 'radixSort');
runIntegerSortTest(sorting.bucketSort, 'bucketSort');

console.log('\n=== All sorting tests completed ===');