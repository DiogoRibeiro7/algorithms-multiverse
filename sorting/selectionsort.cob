       IDENTIFICATION DIVISION.
       PROGRAM-ID. SELECTION-SORT-DEMO.
      *================================================================
      * Selection Sort Algorithm - Educational Implementation (COBOL)
      *
      * ALGORITHM OVERVIEW:
      * ==================
      * Selection Sort works by repeatedly finding the minimum element
      * from the unsorted portion of the array and placing it at the
      * beginning. It divides the array into two parts: a sorted
      * portion (left) and an unsorted portion (right).
      *
      * Time Complexity:
      * - Best Case: O(n²) - Even if array is already sorted
      * - Average Case: O(n²)
      * - Worst Case: O(n²)
      * - IMPORTANT: Unlike bubble sort and insertion sort, selection
      *   sort ALWAYS performs O(n²) comparisons, regardless of input
      *
      * Space Complexity: O(1) - Sorts in-place with constant space
      *
      * Stability: NOT stable by default
      * In-place: YES
      *
      * KEY ADVANTAGE: Makes MINIMUM number of swaps - only O(n) swaps!
      * This is critical when writing to memory is expensive.
      *================================================================

       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       SOURCE-COMPUTER. IBM-PC.
       OBJECT-COMPUTER. IBM-PC.

       DATA DIVISION.
       WORKING-STORAGE SECTION.
      *----------------------------------------------------------------
      * Array Definitions
      *----------------------------------------------------------------
       01  ARRAY-SIZE             PIC 99 VALUE 10.
       01  TEST-ARRAY.
           05  ARR-ELEMENT        PIC S9(4) OCCURS 10 TIMES.

       01  TEMP-ARRAY.
           05  TEMP-ELEMENT       PIC S9(4) OCCURS 10 TIMES.

      *----------------------------------------------------------------
      * Loop Control Variables
      *----------------------------------------------------------------
       01  OUTER-INDEX            PIC 99.
       01  INNER-INDEX            PIC 99.
       01  MIN-INDEX              PIC 99.
       01  TEMP-VALUE             PIC S9(4).
       01  DISPLAY-INDEX          PIC 99.

      *----------------------------------------------------------------
      * Display and Control Variables
      *----------------------------------------------------------------
       01  IS-SORTED-FLAG         PIC 9 VALUE 0.
           88  IS-SORTED                VALUE 1.
           88  NOT-SORTED               VALUE 0.

       01  PASS-COUNTER           PIC 99.
       01  MIN-VALUE              PIC S9(4).

       01  DISPLAY-LINE           PIC X(70).

      *----------------------------------------------------------------
      * Test Data Definitions
      *----------------------------------------------------------------
       01  TEST-DATA-1.
           05  FILLER             PIC S9(4) VALUE +0064.
           05  FILLER             PIC S9(4) VALUE +0025.
           05  FILLER             PIC S9(4) VALUE +0012.
           05  FILLER             PIC S9(4) VALUE +0022.
           05  FILLER             PIC S9(4) VALUE +0011.
           05  FILLER             PIC S9(4) VALUE +0090.
           05  FILLER             PIC S9(4) VALUE +0033.
           05  FILLER             PIC S9(4) VALUE +0015.
           05  FILLER             PIC S9(4) VALUE +0008.
           05  FILLER             PIC S9(4) VALUE +0045.

       01  FILLER REDEFINES TEST-DATA-1.
           05  TD1-ELEMENT        PIC S9(4) OCCURS 10 TIMES.

      *================================================================
      * MAIN PROCEDURE
      *================================================================
       PROCEDURE DIVISION.
       MAIN-PROCEDURE.
           PERFORM DISPLAY-HEADER.
           PERFORM TEST-BASIC-SORT.
           PERFORM DISPLAY-VISUALIZATION.
           PERFORM DISPLAY-MEMORY-ANALYSIS.
           PERFORM DISPLAY-USE-CASES.
           STOP RUN.

      *----------------------------------------------------------------
      * Display program header
      *----------------------------------------------------------------
       DISPLAY-HEADER.
           DISPLAY "========================================"
                   "====================================".
           DISPLAY "SELECTION SORT - EDUCATIONAL DEMONSTR"
                   "ATION (COBOL)".
           DISPLAY "========================================"
                   "====================================".
           DISPLAY SPACE.

      *----------------------------------------------------------------
      * Test basic sorting functionality
      *----------------------------------------------------------------
       TEST-BASIC-SORT.
           DISPLAY "BASIC FUNCTIONALITY TEST:".
           DISPLAY "----------------------------------------"
                   "------------------------------------".
           DISPLAY SPACE.

      *    Copy test data to array
           PERFORM VARYING DISPLAY-INDEX FROM 1 BY 1
                   UNTIL DISPLAY-INDEX > 10
               MOVE TD1-ELEMENT(DISPLAY-INDEX)
                    TO ARR-ELEMENT(DISPLAY-INDEX)
           END-PERFORM.

      *    Display original array
           DISPLAY "Original Array:".
           PERFORM DISPLAY-ARRAY.
           DISPLAY SPACE.

      *    Perform selection sort
           PERFORM SELECTION-SORT.

      *    Display sorted array
           DISPLAY "Sorted Array:".
           PERFORM DISPLAY-ARRAY.

      *    Verify array is sorted
           PERFORM CHECK-IF-SORTED.
           IF IS-SORTED
               DISPLAY "Status: PASS ✓"
           ELSE
               DISPLAY "Status: FAIL ✗"
           END-IF.
           DISPLAY SPACE.
           DISPLAY SPACE.

      *================================================================
      * STANDARD SELECTION SORT
      *================================================================
      * ALGORITHM STEPS:
      * ===============
      * 1. Find the minimum element in the unsorted portion
      * 2. Swap it with the first element of the unsorted portion
      * 3. Move the boundary of sorted/unsorted portions one element
      *    to the right
      * 4. Repeat until the entire array is sorted
      *
      * Visual Example:
      * ==============
      * Initial: [64, 25, 12, 22, 11]
      *
      * Pass 1: Find min in [64, 25, 12, 22, 11] → 11
      *         Swap 64 ↔ 11
      *         Result: [11, 25, 12, 22, 64]
      *                  ^^^ sorted portion
      *
      * Pass 2: Find min in [25, 12, 22, 64] → 12
      *         Swap 25 ↔ 12
      *         Result: [11, 12, 25, 22, 64]
      *                  ^^^^^^^ sorted portion
      *
      * Time: O(n²), Space: O(1)
      *================================================================
       SELECTION-SORT.
      *    Outer loop: Move boundary of unsorted subarray one by one
           PERFORM VARYING OUTER-INDEX FROM 1 BY 1
                   UNTIL OUTER-INDEX >= ARRAY-SIZE

      *        Find the minimum element in the remaining unsorted array
      *        Start by assuming the first unsorted element is minimum
               MOVE OUTER-INDEX TO MIN-INDEX

      *        Inner loop: Search for the minimum in remaining elements
               PERFORM VARYING INNER-INDEX FROM OUTER-INDEX + 1 BY 1
                       UNTIL INNER-INDEX > ARRAY-SIZE

      *            If we find a smaller element, update MIN-INDEX
                   IF ARR-ELEMENT(INNER-INDEX) <
                      ARR-ELEMENT(MIN-INDEX)
                       MOVE INNER-INDEX TO MIN-INDEX
                   END-IF
               END-PERFORM

      *        Swap the found minimum element with the first element
      *        of the unsorted portion (only if different)
               IF MIN-INDEX NOT = OUTER-INDEX
                   MOVE ARR-ELEMENT(OUTER-INDEX) TO TEMP-VALUE
                   MOVE ARR-ELEMENT(MIN-INDEX)
                        TO ARR-ELEMENT(OUTER-INDEX)
                   MOVE TEMP-VALUE TO ARR-ELEMENT(MIN-INDEX)
               END-IF
           END-PERFORM.

      *----------------------------------------------------------------
      * Display array contents
      *----------------------------------------------------------------
       DISPLAY-ARRAY.
           DISPLAY "  [" WITH NO ADVANCING.
           PERFORM VARYING DISPLAY-INDEX FROM 1 BY 1
                   UNTIL DISPLAY-INDEX > ARRAY-SIZE
               IF DISPLAY-INDEX < ARRAY-SIZE
                   DISPLAY ARR-ELEMENT(DISPLAY-INDEX) WITH NO ADVANCING
                   DISPLAY ", " WITH NO ADVANCING
               ELSE
                   DISPLAY ARR-ELEMENT(DISPLAY-INDEX) WITH NO ADVANCING
               END-IF
           END-PERFORM.
           DISPLAY "]".

      *----------------------------------------------------------------
      * Check if array is sorted in ascending order
      *----------------------------------------------------------------
       CHECK-IF-SORTED.
           MOVE 1 TO IS-SORTED-FLAG.
           PERFORM VARYING DISPLAY-INDEX FROM 1 BY 1
                   UNTIL DISPLAY-INDEX >= ARRAY-SIZE
               IF ARR-ELEMENT(DISPLAY-INDEX) >
                  ARR-ELEMENT(DISPLAY-INDEX + 1)
                   MOVE 0 TO IS-SORTED-FLAG
                   EXIT PERFORM
               END-IF
           END-PERFORM.

      *----------------------------------------------------------------
      * Display step-by-step visualization
      *----------------------------------------------------------------
       DISPLAY-VISUALIZATION.
           DISPLAY "========================================"
                   "====================================".
           DISPLAY "STEP-BY-STEP VISUALIZATION".
           DISPLAY "========================================"
                   "====================================".
           DISPLAY SPACE.

      *    Initialize array with demo data
           MOVE +0064 TO ARR-ELEMENT(1).
           MOVE +0025 TO ARR-ELEMENT(2).
           MOVE +0012 TO ARR-ELEMENT(3).
           MOVE +0022 TO ARR-ELEMENT(4).
           MOVE +0011 TO ARR-ELEMENT(5).
           MOVE 5 TO ARRAY-SIZE.

           DISPLAY "Initial array:".
           PERFORM DISPLAY-ARRAY.
           DISPLAY SPACE.

      *    Perform sort with visualization
           MOVE 0 TO PASS-COUNTER.
           PERFORM VARYING OUTER-INDEX FROM 1 BY 1
                   UNTIL OUTER-INDEX >= ARRAY-SIZE

               ADD 1 TO PASS-COUNTER
               DISPLAY "Pass " PASS-COUNTER ":"

      *        Display unsorted portion
               DISPLAY "  Looking for minimum in unsorted portion:"
                       WITH NO ADVANCING
               DISPLAY "  [" WITH NO ADVANCING
               PERFORM VARYING DISPLAY-INDEX FROM OUTER-INDEX BY 1
                       UNTIL DISPLAY-INDEX > ARRAY-SIZE
                   IF DISPLAY-INDEX < ARRAY-SIZE
                       DISPLAY ARR-ELEMENT(DISPLAY-INDEX)
                               WITH NO ADVANCING
                       DISPLAY ", " WITH NO ADVANCING
                   ELSE
                       DISPLAY ARR-ELEMENT(DISPLAY-INDEX)
                               WITH NO ADVANCING
                   END-IF
               END-PERFORM
               DISPLAY "]"

      *        Find minimum
               MOVE OUTER-INDEX TO MIN-INDEX
               MOVE ARR-ELEMENT(MIN-INDEX) TO MIN-VALUE
               PERFORM VARYING INNER-INDEX FROM OUTER-INDEX + 1 BY 1
                       UNTIL INNER-INDEX > ARRAY-SIZE
                   IF ARR-ELEMENT(INNER-INDEX) < MIN-VALUE
                       MOVE INNER-INDEX TO MIN-INDEX
                       MOVE ARR-ELEMENT(MIN-INDEX) TO MIN-VALUE
                       DISPLAY "    Found new minimum: " MIN-VALUE
                               " at index " MIN-INDEX
                   END-IF
               END-PERFORM

      *        Perform swap if needed
               IF MIN-INDEX NOT = OUTER-INDEX
                   DISPLAY "  Swapping " ARR-ELEMENT(OUTER-INDEX)
                           " ↔ " ARR-ELEMENT(MIN-INDEX)
                   MOVE ARR-ELEMENT(OUTER-INDEX) TO TEMP-VALUE
                   MOVE ARR-ELEMENT(MIN-INDEX)
                        TO ARR-ELEMENT(OUTER-INDEX)
                   MOVE TEMP-VALUE TO ARR-ELEMENT(MIN-INDEX)
               ELSE
                   DISPLAY "  No swap needed "
                           "(minimum already in place)"
               END-IF

      *        Display current state
               DISPLAY "  Sorted: [" WITH NO ADVANCING
               PERFORM VARYING DISPLAY-INDEX FROM 1 BY 1
                       UNTIL DISPLAY-INDEX > OUTER-INDEX
                   IF DISPLAY-INDEX < OUTER-INDEX
                       DISPLAY ARR-ELEMENT(DISPLAY-INDEX)
                               WITH NO ADVANCING
                       DISPLAY ", " WITH NO ADVANCING
                   ELSE
                       DISPLAY ARR-ELEMENT(DISPLAY-INDEX)
                               WITH NO ADVANCING
                   END-IF
               END-PERFORM
               DISPLAY "] | Unsorted: [" WITH NO ADVANCING
               IF OUTER-INDEX < ARRAY-SIZE
                   PERFORM VARYING DISPLAY-INDEX FROM OUTER-INDEX + 1 BY 1
                           UNTIL DISPLAY-INDEX > ARRAY-SIZE
                       IF DISPLAY-INDEX < ARRAY-SIZE
                           DISPLAY ARR-ELEMENT(DISPLAY-INDEX)
                                   WITH NO ADVANCING
                           DISPLAY ", " WITH NO ADVANCING
                       ELSE
                           DISPLAY ARR-ELEMENT(DISPLAY-INDEX)
                                   WITH NO ADVANCING
                       END-IF
                   END-PERFORM
               END-IF
               DISPLAY "]"
               DISPLAY SPACE
           END-PERFORM.

           DISPLAY "Final sorted array:".
           PERFORM DISPLAY-ARRAY.
           DISPLAY SPACE.
           DISPLAY SPACE.

      *    Restore array size
           MOVE 10 TO ARRAY-SIZE.

      *----------------------------------------------------------------
      * Display memory usage analysis
      *----------------------------------------------------------------
       DISPLAY-MEMORY-ANALYSIS.
           DISPLAY "========================================"
                   "====================================".
           DISPLAY "MEMORY USAGE ANALYSIS".
           DISPLAY "========================================"
                   "====================================".
           DISPLAY SPACE.
           DISPLAY "Selection Sort Memory Characteristics:".
           DISPLAY SPACE.
           DISPLAY "1. In-Place Sorting:".
           DISPLAY "   - Space Complexity: O(1) auxiliary space".
           DISPLAY "   - Only uses constant extra memory".
           DISPLAY "   - Original array is modified in-place".
           DISPLAY SPACE.
           DISPLAY "2. Memory Writes:".
           DISPLAY "   - Selection Sort: O(n) swaps (minimum)".
           DISPLAY "   - Bubble Sort: O(n²) swaps worst case".
           DISPLAY "   - Insertion Sort: O(n²) shifts worst case".
           DISPLAY SPACE.
           DISPLAY "   ⭐ This makes Selection Sort ideal when".
           DISPLAY "      writing to memory is expensive!".
           DISPLAY "      Examples: Flash memory, EEPROM, or".
           DISPLAY "      distributed systems".
           DISPLAY SPACE.
           DISPLAY "3. COBOL-Specific:".
           DISPLAY "   - Fixed-size arrays (OCCURS clause)".
           DISPLAY "   - No dynamic allocation".
           DISPLAY "   - Efficient for business data processing".
           DISPLAY SPACE.
           DISPLAY SPACE.

      *----------------------------------------------------------------
      * Display use cases
      *----------------------------------------------------------------
       DISPLAY-USE-CASES.
           DISPLAY "========================================"
                   "====================================".
           DISPLAY "WHEN TO USE SELECTION SORT".
           DISPLAY "========================================"
                   "====================================".
           DISPLAY SPACE.
           DISPLAY "✅ GOOD USE CASES:".
           DISPLAY SPACE.
           DISPLAY "1. Minimal Memory Writes:".
           DISPLAY "   - Flash memory or EEPROM (limited write"
                   " cycles)".
           DISPLAY "   - Distributed systems where network".
           DISPLAY "     writes are expensive".
           DISPLAY SPACE.
           DISPLAY "2. Small Datasets:".
           DISPLAY "   - When simplicity matters more than".
           DISPLAY "     efficiency".
           DISPLAY "   - Business applications with small".
           DISPLAY "     record sets".
           DISPLAY SPACE.
           DISPLAY "3. Known Small Data:".
           DISPLAY "   - COBOL batch processing with small".
           DISPLAY "     arrays".
           DISPLAY "   - When n is guaranteed to be small".
           DISPLAY "     (< 20 elements)".
           DISPLAY SPACE.
           DISPLAY "❌ POOR USE CASES:".
           DISPLAY SPACE.
           DISPLAY "1. Large Datasets:".
           DISPLAY "   - Always O(n²) time, never adapts to input".
           DISPLAY "   - Much slower than O(n log n) algorithms".
           DISPLAY SPACE.
           DISPLAY "2. Nearly Sorted Data:".
           DISPLAY "   - Unlike insertion sort, doesn't benefit".
           DISPLAY "     from sorted input".
           DISPLAY "   - Still performs all O(n²) comparisons".
           DISPLAY SPACE.
           DISPLAY "3. Real-time Systems:".
           DISPLAY "   - Non-adaptive nature means worst-case".
           DISPLAY "     is always hit".
           DISPLAY SPACE.
           DISPLAY SPACE.
           DISPLAY "✨ Selection Sort demonstration complete!".

       END PROGRAM SELECTION-SORT-DEMO.
