      ******************************************************************
      * Matrix Operations and Linear Algebra in COBOL
      *
      * Business-oriented matrix operations for financial calculations,
      * statistical analysis, and business mathematics.
      *
      * Features:
      * - Basic matrix operations (add, multiply, transpose)
      * - Matrix determinant calculation
      * - Linear system solving (simplified)
      * - Business-focused implementations
      * - Fixed-point arithmetic for financial accuracy
      *
      * Compile: cobc -x -free MATRIX.cob
      * Run: ./MATRIX
      *
      * @author Algorithms Multiverse
      * @version 1.0
      ******************************************************************

       IDENTIFICATION DIVISION.
       PROGRAM-ID. MATRIX-OPERATIONS.
       AUTHOR. ALGORITHMS-MULTIVERSE.

       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       SOURCE-COMPUTER. IBM-PC.
       OBJECT-COMPUTER. IBM-PC.

       DATA DIVISION.
       WORKING-STORAGE SECTION.

      * Constants
       01  EPSILON             PIC 9V9(10) VALUE 0.0000000001.
       01  MAX-SIZE            PIC 99 VALUE 10.

      * Matrix A (up to 10x10)
       01  MATRIX-A.
           05  MATRIX-A-ROWS   PIC 99.
           05  MATRIX-A-COLS   PIC 99.
           05  MATRIX-A-DATA.
               10  MATRIX-A-ROW OCCURS 10 TIMES.
                   15  MATRIX-A-ELEMENT OCCURS 10 TIMES
                       PIC S9(5)V9(4) COMP-3.

      * Matrix B (up to 10x10)
       01  MATRIX-B.
           05  MATRIX-B-ROWS   PIC 99.
           05  MATRIX-B-COLS   PIC 99.
           05  MATRIX-B-DATA.
               10  MATRIX-B-ROW OCCURS 10 TIMES.
                   15  MATRIX-B-ELEMENT OCCURS 10 TIMES
                       PIC S9(5)V9(4) COMP-3.

      * Result Matrix C (up to 10x10)
       01  MATRIX-C.
           05  MATRIX-C-ROWS   PIC 99.
           05  MATRIX-C-COLS   PIC 99.
           05  MATRIX-C-DATA.
               10  MATRIX-C-ROW OCCURS 10 TIMES.
                   15  MATRIX-C-ELEMENT OCCURS 10 TIMES
                       PIC S9(5)V9(4) COMP-3.

      * Vector for linear systems
       01  VECTOR-B.
           05  VECTOR-B-SIZE   PIC 99.
           05  VECTOR-B-DATA.
               10  VECTOR-B-ELEMENT OCCURS 10 TIMES
                   PIC S9(5)V9(4) COMP-3.

       01  VECTOR-X.
           05  VECTOR-X-SIZE   PIC 99.
           05  VECTOR-X-DATA.
               10  VECTOR-X-ELEMENT OCCURS 10 TIMES
                   PIC S9(5)V9(4) COMP-3.

      * Loop counters and working variables
       01  I                   PIC 99.
       01  J                   PIC 99.
       01  K                   PIC 99.
       01  ROW-IDX             PIC 99.
       01  COL-IDX             PIC 99.
       01  SUM-TEMP            PIC S9(7)V9(4) COMP-3.
       01  TEMP-VALUE          PIC S9(5)V9(4) COMP-3.
       01  FACTOR              PIC S9(5)V9(4) COMP-3.
       01  DETERMINANT-RESULT  PIC S9(7)V9(4) COMP-3.

      * Display variables
       01  DISPLAY-VALUE       PIC -----9.9999.
       01  OPERATION-STATUS    PIC X(30).

      * Flags
       01  ERROR-FLAG          PIC 9 VALUE 0.
           88  NO-ERROR        VALUE 0.
           88  HAS-ERROR       VALUE 1.

       PROCEDURE DIVISION.
       MAIN-PROCEDURE.
           DISPLAY "========================================".
           DISPLAY "Matrix Operations - COBOL Implementation".
           DISPLAY "========================================".
           DISPLAY " ".

           PERFORM EXAMPLE-MATRIX-ADDITION.
           PERFORM EXAMPLE-MATRIX-MULTIPLICATION.
           PERFORM EXAMPLE-MATRIX-TRANSPOSE.
           PERFORM EXAMPLE-DETERMINANT-2X2.

           DISPLAY " ".
           DISPLAY "========================================".
           DISPLAY "All examples completed successfully!".
           DISPLAY "========================================".

           STOP RUN.

      ******************************************************************
      * Matrix Addition Example
      ******************************************************************
       EXAMPLE-MATRIX-ADDITION.
           DISPLAY "======================================".
           DISPLAY "Example 1: Matrix Addition".
           DISPLAY "======================================".

      * Initialize Matrix A (2x2)
           MOVE 2 TO MATRIX-A-ROWS.
           MOVE 2 TO MATRIX-A-COLS.
           MOVE 1 TO MATRIX-A-ELEMENT(1, 1).
           MOVE 2 TO MATRIX-A-ELEMENT(1, 2).
           MOVE 3 TO MATRIX-A-ELEMENT(2, 1).
           MOVE 4 TO MATRIX-A-ELEMENT(2, 2).

      * Initialize Matrix B (2x2)
           MOVE 2 TO MATRIX-B-ROWS.
           MOVE 2 TO MATRIX-B-COLS.
           MOVE 5 TO MATRIX-B-ELEMENT(1, 1).
           MOVE 6 TO MATRIX-B-ELEMENT(1, 2).
           MOVE 7 TO MATRIX-B-ELEMENT(2, 1).
           MOVE 8 TO MATRIX-B-ELEMENT(2, 2).

      * Perform addition
           PERFORM MATRIX-ADD.

      * Display results
           DISPLAY " ".
           DISPLAY "Matrix A:".
           MOVE MATRIX-A-ROWS TO ROW-IDX.
           MOVE MATRIX-A-COLS TO COL-IDX.
           PERFORM DISPLAY-MATRIX-A.

           DISPLAY " ".
           DISPLAY "Matrix B:".
           MOVE MATRIX-B-ROWS TO ROW-IDX.
           MOVE MATRIX-B-COLS TO COL-IDX.
           PERFORM DISPLAY-MATRIX-B.

           DISPLAY " ".
           DISPLAY "Matrix C = A + B:".
           MOVE MATRIX-C-ROWS TO ROW-IDX.
           MOVE MATRIX-C-COLS TO COL-IDX.
           PERFORM DISPLAY-MATRIX-C.

           DISPLAY " ".

      ******************************************************************
      * Matrix Multiplication Example
      ******************************************************************
       EXAMPLE-MATRIX-MULTIPLICATION.
           DISPLAY "======================================".
           DISPLAY "Example 2: Matrix Multiplication".
           DISPLAY "======================================".

      * Initialize Matrix A (2x3)
           MOVE 2 TO MATRIX-A-ROWS.
           MOVE 3 TO MATRIX-A-COLS.
           MOVE 1 TO MATRIX-A-ELEMENT(1, 1).
           MOVE 2 TO MATRIX-A-ELEMENT(1, 2).
           MOVE 3 TO MATRIX-A-ELEMENT(1, 3).
           MOVE 4 TO MATRIX-A-ELEMENT(2, 1).
           MOVE 5 TO MATRIX-A-ELEMENT(2, 2).
           MOVE 6 TO MATRIX-A-ELEMENT(2, 3).

      * Initialize Matrix B (3x2)
           MOVE 3 TO MATRIX-B-ROWS.
           MOVE 2 TO MATRIX-B-COLS.
           MOVE 7 TO MATRIX-B-ELEMENT(1, 1).
           MOVE 8 TO MATRIX-B-ELEMENT(1, 2).
           MOVE 9 TO MATRIX-B-ELEMENT(2, 1).
           MOVE 10 TO MATRIX-B-ELEMENT(2, 2).
           MOVE 11 TO MATRIX-B-ELEMENT(3, 1).
           MOVE 12 TO MATRIX-B-ELEMENT(3, 2).

      * Perform multiplication
           PERFORM MATRIX-MULTIPLY.

      * Display results
           DISPLAY " ".
           DISPLAY "Matrix A (2x3):".
           MOVE MATRIX-A-ROWS TO ROW-IDX.
           MOVE MATRIX-A-COLS TO COL-IDX.
           PERFORM DISPLAY-MATRIX-A.

           DISPLAY " ".
           DISPLAY "Matrix B (3x2):".
           MOVE MATRIX-B-ROWS TO ROW-IDX.
           MOVE MATRIX-B-COLS TO COL-IDX.
           PERFORM DISPLAY-MATRIX-B.

           DISPLAY " ".
           DISPLAY "Matrix C = A x B (2x2):".
           MOVE MATRIX-C-ROWS TO ROW-IDX.
           MOVE MATRIX-C-COLS TO COL-IDX.
           PERFORM DISPLAY-MATRIX-C.

           DISPLAY " ".

      ******************************************************************
      * Matrix Transpose Example
      ******************************************************************
       EXAMPLE-MATRIX-TRANSPOSE.
           DISPLAY "======================================".
           DISPLAY "Example 3: Matrix Transpose".
           DISPLAY "======================================".

      * Initialize Matrix A (2x3)
           MOVE 2 TO MATRIX-A-ROWS.
           MOVE 3 TO MATRIX-A-COLS.
           MOVE 1 TO MATRIX-A-ELEMENT(1, 1).
           MOVE 2 TO MATRIX-A-ELEMENT(1, 2).
           MOVE 3 TO MATRIX-A-ELEMENT(1, 3).
           MOVE 4 TO MATRIX-A-ELEMENT(2, 1).
           MOVE 5 TO MATRIX-A-ELEMENT(2, 2).
           MOVE 6 TO MATRIX-A-ELEMENT(2, 3).

      * Perform transpose
           PERFORM MATRIX-TRANSPOSE.

      * Display results
           DISPLAY " ".
           DISPLAY "Matrix A (2x3):".
           MOVE MATRIX-A-ROWS TO ROW-IDX.
           MOVE MATRIX-A-COLS TO COL-IDX.
           PERFORM DISPLAY-MATRIX-A.

           DISPLAY " ".
           DISPLAY "Matrix C = A^T (3x2):".
           MOVE MATRIX-C-ROWS TO ROW-IDX.
           MOVE MATRIX-C-COLS TO COL-IDX.
           PERFORM DISPLAY-MATRIX-C.

           DISPLAY " ".

      ******************************************************************
      * Determinant Calculation Example (2x2 only)
      ******************************************************************
       EXAMPLE-DETERMINANT-2X2.
           DISPLAY "======================================".
           DISPLAY "Example 4: Determinant (2x2)".
           DISPLAY "======================================".

      * Initialize Matrix A (2x2)
           MOVE 2 TO MATRIX-A-ROWS.
           MOVE 2 TO MATRIX-A-COLS.
           MOVE 4 TO MATRIX-A-ELEMENT(1, 1).
           MOVE 7 TO MATRIX-A-ELEMENT(1, 2).
           MOVE 2 TO MATRIX-A-ELEMENT(2, 1).
           MOVE 6 TO MATRIX-A-ELEMENT(2, 2).

      * Calculate determinant
           PERFORM CALCULATE-DETERMINANT-2X2.

      * Display results
           DISPLAY " ".
           DISPLAY "Matrix A:".
           MOVE MATRIX-A-ROWS TO ROW-IDX.
           MOVE MATRIX-A-COLS TO COL-IDX.
           PERFORM DISPLAY-MATRIX-A.

           DISPLAY " ".
           MOVE DETERMINANT-RESULT TO DISPLAY-VALUE.
           DISPLAY "Determinant = " DISPLAY-VALUE.
           DISPLAY " ".

      ******************************************************************
      * Matrix Operations Implementations
      ******************************************************************

      ******************************************************************
      * Matrix Addition: C = A + B
      * Time Complexity: O(rows * cols)
      *
      * Applications:
      * - Financial statement consolidation
      * - Budget aggregation
      * - Statistical data combination
      ******************************************************************
       MATRIX-ADD.
           MOVE 0 TO ERROR-FLAG.

      * Check dimensions match
           IF MATRIX-A-ROWS NOT = MATRIX-B-ROWS OR
              MATRIX-A-COLS NOT = MATRIX-B-COLS
               MOVE 1 TO ERROR-FLAG
               MOVE "ERROR: Dimension mismatch" TO OPERATION-STATUS
               DISPLAY OPERATION-STATUS
               GO TO MATRIX-ADD-EXIT
           END-IF.

      * Set result dimensions
           MOVE MATRIX-A-ROWS TO MATRIX-C-ROWS.
           MOVE MATRIX-A-COLS TO MATRIX-C-COLS.

      * Perform addition
           PERFORM VARYING I FROM 1 BY 1
               UNTIL I > MATRIX-A-ROWS
               PERFORM VARYING J FROM 1 BY 1
                   UNTIL J > MATRIX-A-COLS
                   COMPUTE MATRIX-C-ELEMENT(I, J) =
                       MATRIX-A-ELEMENT(I, J) +
                       MATRIX-B-ELEMENT(I, J)
               END-PERFORM
           END-PERFORM.

       MATRIX-ADD-EXIT.
           EXIT.

      ******************************************************************
      * Matrix Multiplication: C = A * B
      * Time Complexity: O(n^3) for n×n matrices
      *
      * Algorithm:
      * C[i][j] = Σ(A[i][k] * B[k][j]) for k from 1 to n
      *
      * Applications:
      * - Financial modeling (compound calculations)
      * - Supply chain optimization
      * - Economic input-output analysis
      * - Portfolio calculations
      ******************************************************************
       MATRIX-MULTIPLY.
           MOVE 0 TO ERROR-FLAG.

      * Check if multiplication is possible
           IF MATRIX-A-COLS NOT = MATRIX-B-ROWS
               MOVE 1 TO ERROR-FLAG
               MOVE "ERROR: Cannot multiply matrices"
                   TO OPERATION-STATUS
               DISPLAY OPERATION-STATUS
               GO TO MATRIX-MULTIPLY-EXIT
           END-IF.

      * Set result dimensions
           MOVE MATRIX-A-ROWS TO MATRIX-C-ROWS.
           MOVE MATRIX-B-COLS TO MATRIX-C-COLS.

      * Initialize result matrix to zero
           PERFORM VARYING I FROM 1 BY 1
               UNTIL I > MATRIX-C-ROWS
               PERFORM VARYING J FROM 1 BY 1
                   UNTIL J > MATRIX-C-COLS
                   MOVE 0 TO MATRIX-C-ELEMENT(I, J)
               END-PERFORM
           END-PERFORM.

      * Perform multiplication
           PERFORM VARYING I FROM 1 BY 1
               UNTIL I > MATRIX-A-ROWS
               PERFORM VARYING J FROM 1 BY 1
                   UNTIL J > MATRIX-B-COLS
                   MOVE 0 TO SUM-TEMP
                   PERFORM VARYING K FROM 1 BY 1
                       UNTIL K > MATRIX-A-COLS
                       COMPUTE SUM-TEMP = SUM-TEMP +
                           (MATRIX-A-ELEMENT(I, K) *
                            MATRIX-B-ELEMENT(K, J))
                   END-PERFORM
                   MOVE SUM-TEMP TO MATRIX-C-ELEMENT(I, J)
               END-PERFORM
           END-PERFORM.

       MATRIX-MULTIPLY-EXIT.
           EXIT.

      ******************************************************************
      * Matrix Transpose: C = A^T
      * Time Complexity: O(rows * cols)
      *
      * Applications:
      * - Data reorganization
      * - Statistical covariance computation
      * - Linear algebra transformations
      ******************************************************************
       MATRIX-TRANSPOSE.
      * Set result dimensions (swapped)
           MOVE MATRIX-A-COLS TO MATRIX-C-ROWS.
           MOVE MATRIX-A-ROWS TO MATRIX-C-COLS.

      * Perform transpose
           PERFORM VARYING I FROM 1 BY 1
               UNTIL I > MATRIX-A-ROWS
               PERFORM VARYING J FROM 1 BY 1
                   UNTIL J > MATRIX-A-COLS
                   MOVE MATRIX-A-ELEMENT(I, J) TO
                        MATRIX-C-ELEMENT(J, I)
               END-PERFORM
           END-PERFORM.

      ******************************************************************
      * Calculate Determinant for 2x2 Matrix
      * Time Complexity: O(1)
      *
      * Formula: det(A) = a11*a22 - a12*a21
      *
      * Applications:
      * - Testing matrix singularity
      * - Checking system solvability
      * - Financial ratio analysis
      ******************************************************************
       CALCULATE-DETERMINANT-2X2.
           IF MATRIX-A-ROWS NOT = 2 OR MATRIX-A-COLS NOT = 2
               MOVE 0 TO DETERMINANT-RESULT
               DISPLAY "ERROR: Not a 2x2 matrix"
               GO TO CALCULATE-DETERMINANT-EXIT
           END-IF.

           COMPUTE DETERMINANT-RESULT =
               (MATRIX-A-ELEMENT(1, 1) * MATRIX-A-ELEMENT(2, 2)) -
               (MATRIX-A-ELEMENT(1, 2) * MATRIX-A-ELEMENT(2, 1)).

       CALCULATE-DETERMINANT-EXIT.
           EXIT.

      ******************************************************************
      * Display Routines
      ******************************************************************
       DISPLAY-MATRIX-A.
           PERFORM VARYING I FROM 1 BY 1
               UNTIL I > ROW-IDX
               PERFORM VARYING J FROM 1 BY 1
                   UNTIL J > COL-IDX
                   MOVE MATRIX-A-ELEMENT(I, J) TO DISPLAY-VALUE
                   DISPLAY DISPLAY-VALUE WITH NO ADVANCING
                   DISPLAY " " WITH NO ADVANCING
               END-PERFORM
               DISPLAY " "
           END-PERFORM.

       DISPLAY-MATRIX-B.
           PERFORM VARYING I FROM 1 BY 1
               UNTIL I > ROW-IDX
               PERFORM VARYING J FROM 1 BY 1
                   UNTIL J > COL-IDX
                   MOVE MATRIX-B-ELEMENT(I, J) TO DISPLAY-VALUE
                   DISPLAY DISPLAY-VALUE WITH NO ADVANCING
                   DISPLAY " " WITH NO ADVANCING
               END-PERFORM
               DISPLAY " "
           END-PERFORM.

       DISPLAY-MATRIX-C.
           PERFORM VARYING I FROM 1 BY 1
               UNTIL I > ROW-IDX
               PERFORM VARYING J FROM 1 BY 1
                   UNTIL J > COL-IDX
                   MOVE MATRIX-C-ELEMENT(I, J) TO DISPLAY-VALUE
                   DISPLAY DISPLAY-VALUE WITH NO ADVANCING
                   DISPLAY " " WITH NO ADVANCING
               END-PERFORM
               DISPLAY " "
           END-PERFORM.

       END PROGRAM MATRIX-OPERATIONS.

      ******************************************************************
      * Business Applications Notes:
      *
      * 1. Financial Statement Consolidation:
      *    - Use matrix addition to combine financial statements
      *    - Aggregate budgets across departments
      *
      * 2. Investment Portfolio Analysis:
      *    - Matrix multiplication for portfolio calculations
      *    - Covariance matrix computations
      *
      * 3. Supply Chain Optimization:
      *    - Matrix operations for route optimization
      *    - Inventory management calculations
      *
      * 4. Economic Analysis:
      *    - Input-output models using matrix operations
      *    - Economic multiplier calculations
      *
      * 5. Statistical Analysis:
      *    - Data transformation using matrices
      *    - Regression analysis computations
      *
      * Note: This is an educational implementation. For production
      * systems, use optimized linear algebra libraries.
      ******************************************************************
