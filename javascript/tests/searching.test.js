/**
 * Test suite for searching algorithms
 */

import * as searching from '../src/searching.js';

console.log('=== SEARCHING ALGORITHMS TESTS ===\n');

// Test linear search
console.log('Testing linearSearch...');
let arr = [3, 7, 1, 9, 2, 5];
console.assert(searching.linearSearch(arr, 9) === 3, 'linearSearch failed to find element');
console.assert(searching.linearSearch(arr, 10) === -1, 'linearSearch failed on non-existent element');
console.assert(searching.linearSearch([], 5) === -1, 'linearSearch failed on empty array');
console.log('✓ linearSearch passed all tests');

// Test binary search
console.log('Testing binarySearch...');
arr = [1, 2, 3, 4, 5, 6, 7, 8, 9];
console.assert(searching.binarySearch(arr, 5) === 4, 'binarySearch failed to find middle element');
console.assert(searching.binarySearch(arr, 1) === 0, 'binarySearch failed to find first element');
console.assert(searching.binarySearch(arr, 9) === 8, 'binarySearch failed to find last element');
console.assert(searching.binarySearch(arr, 10) === -1, 'binarySearch failed on non-existent element');
console.assert(searching.binarySearch([], 5) === -1, 'binarySearch failed on empty array');
console.log('✓ binarySearch passed all tests');

// Test jump search
console.log('Testing jumpSearch...');
console.assert(searching.jumpSearch(arr, 5) === 4, 'jumpSearch failed to find element');
console.assert(searching.jumpSearch(arr, 10) === -1, 'jumpSearch failed on non-existent element');
console.log('✓ jumpSearch passed all tests');

// Test interpolation search
console.log('Testing interpolationSearch...');
arr = [10, 20, 30, 40, 50, 60, 70, 80, 90];
console.assert(searching.interpolationSearch(arr, 50) === 4, 'interpolationSearch failed to find element');
console.assert(searching.interpolationSearch(arr, 100) === -1, 'interpolationSearch failed on non-existent element');
console.log('✓ interpolationSearch passed all tests');

// Test exponential search
console.log('Testing exponentialSearch...');
console.assert(searching.exponentialSearch(arr, 50) === 4, 'exponentialSearch failed to find element');
console.assert(searching.exponentialSearch(arr, 100) === -1, 'exponentialSearch failed on non-existent element');
console.log('✓ exponentialSearch passed all tests');

// Test ternary search
console.log('Testing ternarySearch...');
console.assert(searching.ternarySearch(arr, 50) === 4, 'ternarySearch failed to find element');
console.assert(searching.ternarySearch(arr, 100) === -1, 'ternarySearch failed on non-existent element');
console.log('✓ ternarySearch passed all tests');

// Test find min/max
console.log('Testing findMin and findMax...');
arr = [3, 7, 1, 9, 2, 5];
console.assert(searching.findMin(arr) === 1, 'findMin failed');
console.assert(searching.findMax(arr) === 9, 'findMax failed');
console.log('✓ findMin and findMax passed all tests');

// Test find kth smallest/largest
console.log('Testing findKthSmallest and findKthLargest...');
console.assert(searching.findKthSmallest(arr, 3) === 3, 'findKthSmallest failed');
console.assert(searching.findKthLargest(arr, 2) === 7, 'findKthLargest failed');
console.log('✓ findKthSmallest and findKthLargest passed all tests');

// Test two sum
console.log('Testing twoSum...');
arr = [2, 7, 11, 15];
let result = searching.twoSum(arr, 9);
console.assert(result[0] === 0 && result[1] === 1, 'twoSum failed');
result = searching.twoSum(arr, 100);
console.assert(result === null, 'twoSum failed on impossible target');
console.log('✓ twoSum passed all tests');

// Test three sum
console.log('Testing threeSum...');
arr = [-1, 0, 1, 2, -1, -4];
result = searching.threeSum(arr);
console.assert(result.length > 0, 'threeSum failed to find triplets');
console.log('✓ threeSum passed all tests');

// Test search in rotated array
console.log('Testing searchRotated...');
arr = [4, 5, 6, 7, 0, 1, 2];
console.assert(searching.searchRotated(arr, 0) === 4, 'searchRotated failed');
console.assert(searching.searchRotated(arr, 3) === -1, 'searchRotated failed on non-existent element');
console.log('✓ searchRotated passed all tests');

// Test peak element
console.log('Testing findPeakElement...');
arr = [1, 3, 5, 4, 2];
result = searching.findPeakElement(arr);
console.assert(result === 2, 'findPeakElement failed');
console.log('✓ findPeakElement passed all tests');

// Test majority element
console.log('Testing majorityElement...');
arr = [2, 2, 1, 1, 1, 2, 2];
console.assert(searching.majorityElement(arr) === 2, 'majorityElement failed');
console.log('✓ majorityElement passed all tests');

// Test search in 2D matrix
console.log('Testing searchMatrix...');
const matrix = [
    [1, 4, 7, 11],
    [2, 5, 8, 12],
    [3, 6, 9, 16]
];
console.assert(searching.searchMatrix(matrix, 5) === true, 'searchMatrix failed to find element');
console.assert(searching.searchMatrix(matrix, 20) === false, 'searchMatrix failed on non-existent element');
console.log('✓ searchMatrix passed all tests');

console.log('\n=== All searching tests completed ===');