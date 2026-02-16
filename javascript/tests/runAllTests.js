#!/usr/bin/env node

/**
 * Test runner for all algorithm modules
 * Run this file to execute all tests
 */

import { execSync } from 'child_process';
import { readdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

console.log('====================================');
console.log('  ALGORITHMS MULTIVERSE TEST SUITE  ');
console.log('====================================\n');

// Get all test files
const testFiles = readdirSync(__dirname)
    .filter(file => file.endsWith('.test.js'))
    .sort();

let totalTests = 0;
let passedTests = 0;
let failedTests = [];

// Run each test file
for (const testFile of testFiles) {
    console.log(`\n📝 Running ${testFile}...`);
    console.log('─'.repeat(40));

    try {
        execSync(`node ${join(__dirname, testFile)}`, {
            stdio: 'inherit',
            cwd: __dirname
        });
        passedTests++;
        console.log(`✅ ${testFile} completed successfully`);
    } catch (error) {
        failedTests.push(testFile);
        console.error(`❌ ${testFile} failed`);
    }

    totalTests++;
}

// Summary
console.log('\n' + '='.repeat(50));
console.log('                TEST SUMMARY');
console.log('='.repeat(50));
console.log(`Total test files: ${totalTests}`);
console.log(`✅ Passed: ${passedTests}`);
console.log(`❌ Failed: ${failedTests.length}`);

if (failedTests.length > 0) {
    console.log('\nFailed tests:');
    failedTests.forEach(test => console.log(`  - ${test}`));
    process.exit(1);
} else {
    console.log('\n🎉 All tests passed successfully!');
    process.exit(0);
}