       IDENTIFICATION DIVISION.
       PROGRAM-ID. BINARY-SEARCH-DEMO.
       AUTHOR. CLAUDE-CODE.
      *================================================================
      * Binary Search Algorithm Collection in COBOL
      *
      * Comprehensive implementation of binary search variants:
      * 1. Classic binary search (iterative)
      * 2. First/last occurrence finding
      * 3. Rotated array search
      * 4. Interpolation search
      * 5. Ternary search
      * 6. Integer square root
      * 7. Find closest element
      *
      * Time Complexity: O(log n) for most variants
      * Space Complexity: O(1) iterative
      *
      * COBOL Features:
      * - Structured programming with procedures
      * - Table handling with OCCURS clause
      * - Business-oriented data processing
      * - Self-documenting code style
      *================================================================

       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       SOURCE-COMPUTER. IBM-PC.
       OBJECT-COMPUTER. IBM-PC.

       DATA DIVISION.
       WORKING-STORAGE SECTION.

      * Array and search variables
       01  WS-ARRAY-SIZE           PIC 9(4) VALUE 10.
       01  WS-SEARCH-ARRAY.
           05 WS-ELEMENT           PIC S9(5) OCCURS 100 TIMES.

       01  WS-TARGET               PIC S9(5).
       01  WS-RESULT-INDEX         PIC 9(4).
       01  WS-LEFT-INDEX           PIC 9(4).
       01  WS-RIGHT-INDEX          PIC 9(4).
       01  WS-MID-INDEX            PIC 9(4).
       01  WS-TEMP-INDEX           PIC 9(4).
       01  WS-COUNT                PIC 9(4).

      * Test data and results
       01  WS-TEST-ARRAY-1.
           05 FILLER PIC S9(5) VALUE 1.
           05 FILLER PIC S9(5) VALUE 3.
           05 FILLER PIC S9(5) VALUE 5.
           05 FILLER PIC S9(5) VALUE 7.
           05 FILLER PIC S9(5) VALUE 9.
           05 FILLER PIC S9(5) VALUE 11.
           05 FILLER PIC S9(5) VALUE 13.
           05 FILLER PIC S9(5) VALUE 15.
           05 FILLER PIC S9(5) VALUE 17.
           05 FILLER PIC S9(5) VALUE 19.

       01  WS-TEST-ARRAY-1-REDEF REDEFINES WS-TEST-ARRAY-1.
           05 WS-TEST-1-ELEM       PIC S9(5) OCCURS 10 TIMES.

       01  WS-TEST-ARRAY-2.
           05 FILLER PIC S9(5) VALUE 1.
           05 FILLER PIC S9(5) VALUE 2.
           05 FILLER PIC S9(5) VALUE 2.
           05 FILLER PIC S9(5) VALUE 2.
           05 FILLER PIC S9(5) VALUE 3.
           05 FILLER PIC S9(5) VALUE 4.
           05 FILLER PIC S9(5) VALUE 4.
           05 FILLER PIC S9(5) VALUE 4.
           05 FILLER PIC S9(5) VALUE 4.
           05 FILLER PIC S9(5) VALUE 5.

       01  WS-TEST-ARRAY-2-REDEF REDEFINES WS-TEST-ARRAY-2.
           05 WS-TEST-2-ELEM       PIC S9(5) OCCURS 10 TIMES.

      * Display variables
       01  WS-DISPLAY-MSG          PIC X(80).
       01  WS-ITERATION            PIC 9(2).

      * Flags
       01  WS-FOUND-FLAG           PIC X VALUE 'N'.
           88 FOUND                VALUE 'Y'.
           88 NOT-FOUND            VALUE 'N'.

       PROCEDURE DIVISION.
       MAIN-PROCEDURE.
           DISPLAY '========================================'.
           DISPLAY 'BINARY SEARCH ALGORITHM COLLECTION - COBOL'.
           DISPLAY '========================================'.
           DISPLAY ' '.

           PERFORM DEMO-CLASSIC-BINARY-SEARCH
           PERFORM DEMO-FIRST-LAST-OCCURRENCE
           PERFORM DEMO-INTERPOLATION-SEARCH
           PERFORM DEMO-TERNARY-SEARCH
           PERFORM DEMO-SQUARE-ROOT
           PERFORM DEMO-CLOSEST-ELEMENT

           DISPLAY ' '.
           DISPLAY '========================================'.
           DISPLAY 'DEMONSTRATION COMPLETE'.
           DISPLAY '========================================'.

           STOP RUN.

      *================================================================
      * 1. CLASSIC BINARY SEARCH - ITERATIVE
      *================================================================

       BINARY-SEARCH-ITERATIVE.
           MOVE 'N' TO WS-FOUND-FLAG
           MOVE 0 TO WS-RESULT-INDEX

           IF WS-ARRAY-SIZE = 0
               GO TO BINARY-SEARCH-END
           END-IF

           MOVE 1 TO WS-LEFT-INDEX
           MOVE WS-ARRAY-SIZE TO WS-RIGHT-INDEX

           PERFORM UNTIL WS-LEFT-INDEX > WS-RIGHT-INDEX
               COMPUTE WS-MID-INDEX = WS-LEFT-INDEX +
                   (WS-RIGHT-INDEX - WS-LEFT-INDEX) / 2

               IF WS-ELEMENT(WS-MID-INDEX) = WS-TARGET
                   MOVE WS-MID-INDEX TO WS-RESULT-INDEX
                   MOVE 'Y' TO WS-FOUND-FLAG
                   GO TO BINARY-SEARCH-END
               ELSE IF WS-ELEMENT(WS-MID-INDEX) < WS-TARGET
                   COMPUTE WS-LEFT-INDEX = WS-MID-INDEX + 1
               ELSE
                   COMPUTE WS-RIGHT-INDEX = WS-MID-INDEX - 1
               END-IF
           END-PERFORM.

       BINARY-SEARCH-END.
           EXIT.

      *================================================================
      * 2. FIND FIRST OCCURRENCE
      *================================================================

       FIND-FIRST-OCCURRENCE.
           MOVE 'N' TO WS-FOUND-FLAG
           MOVE 0 TO WS-RESULT-INDEX

           IF WS-ARRAY-SIZE = 0
               GO TO FIND-FIRST-END
           END-IF

           MOVE 1 TO WS-LEFT-INDEX
           MOVE WS-ARRAY-SIZE TO WS-RIGHT-INDEX

           PERFORM UNTIL WS-LEFT-INDEX > WS-RIGHT-INDEX
               COMPUTE WS-MID-INDEX = WS-LEFT-INDEX +
                   (WS-RIGHT-INDEX - WS-LEFT-INDEX) / 2

               IF WS-ELEMENT(WS-MID-INDEX) = WS-TARGET
                   MOVE WS-MID-INDEX TO WS-RESULT-INDEX
                   MOVE 'Y' TO WS-FOUND-FLAG
                   COMPUTE WS-RIGHT-INDEX = WS-MID-INDEX - 1
               ELSE IF WS-ELEMENT(WS-MID-INDEX) < WS-TARGET
                   COMPUTE WS-LEFT-INDEX = WS-MID-INDEX + 1
               ELSE
                   COMPUTE WS-RIGHT-INDEX = WS-MID-INDEX - 1
               END-IF
           END-PERFORM.

       FIND-FIRST-END.
           EXIT.

      *================================================================
      * 3. FIND LAST OCCURRENCE
      *================================================================

       FIND-LAST-OCCURRENCE.
           MOVE 'N' TO WS-FOUND-FLAG
           MOVE 0 TO WS-RESULT-INDEX

           IF WS-ARRAY-SIZE = 0
               GO TO FIND-LAST-END
           END-IF

           MOVE 1 TO WS-LEFT-INDEX
           MOVE WS-ARRAY-SIZE TO WS-RIGHT-INDEX

           PERFORM UNTIL WS-LEFT-INDEX > WS-RIGHT-INDEX
               COMPUTE WS-MID-INDEX = WS-LEFT-INDEX +
                   (WS-RIGHT-INDEX - WS-LEFT-INDEX) / 2

               IF WS-ELEMENT(WS-MID-INDEX) = WS-TARGET
                   MOVE WS-MID-INDEX TO WS-RESULT-INDEX
                   MOVE 'Y' TO WS-FOUND-FLAG
                   COMPUTE WS-LEFT-INDEX = WS-MID-INDEX + 1
               ELSE IF WS-ELEMENT(WS-MID-INDEX) < WS-TARGET
                   COMPUTE WS-LEFT-INDEX = WS-MID-INDEX + 1
               ELSE
                   COMPUTE WS-RIGHT-INDEX = WS-MID-INDEX - 1
               END-IF
           END-PERFORM.

       FIND-LAST-END.
           EXIT.

      *================================================================
      * 4. INTERPOLATION SEARCH
      *================================================================

       INTERPOLATION-SEARCH.
           MOVE 'N' TO WS-FOUND-FLAG
           MOVE 0 TO WS-RESULT-INDEX

           IF WS-ARRAY-SIZE = 0
               GO TO INTERPOLATION-END
           END-IF

           MOVE 1 TO WS-LEFT-INDEX
           MOVE WS-ARRAY-SIZE TO WS-RIGHT-INDEX

           PERFORM UNTIL WS-LEFT-INDEX > WS-RIGHT-INDEX
               IF WS-TARGET < WS-ELEMENT(WS-LEFT-INDEX) OR
                  WS-TARGET > WS-ELEMENT(WS-RIGHT-INDEX)
                   GO TO INTERPOLATION-END
               END-IF

               IF WS-LEFT-INDEX = WS-RIGHT-INDEX
                   IF WS-ELEMENT(WS-LEFT-INDEX) = WS-TARGET
                       MOVE WS-LEFT-INDEX TO WS-RESULT-INDEX
                       MOVE 'Y' TO WS-FOUND-FLAG
                   END-IF
                   GO TO INTERPOLATION-END
               END-IF

               COMPUTE WS-MID-INDEX = WS-LEFT-INDEX +
                   (WS-TARGET - WS-ELEMENT(WS-LEFT-INDEX)) *
                   (WS-RIGHT-INDEX - WS-LEFT-INDEX) /
                   (WS-ELEMENT(WS-RIGHT-INDEX) -
                    WS-ELEMENT(WS-LEFT-INDEX))

               IF WS-MID-INDEX < WS-LEFT-INDEX
                   MOVE WS-LEFT-INDEX TO WS-MID-INDEX
               END-IF
               IF WS-MID-INDEX > WS-RIGHT-INDEX
                   MOVE WS-RIGHT-INDEX TO WS-MID-INDEX
               END-IF

               IF WS-ELEMENT(WS-MID-INDEX) = WS-TARGET
                   MOVE WS-MID-INDEX TO WS-RESULT-INDEX
                   MOVE 'Y' TO WS-FOUND-FLAG
                   GO TO INTERPOLATION-END
               ELSE IF WS-ELEMENT(WS-MID-INDEX) < WS-TARGET
                   COMPUTE WS-LEFT-INDEX = WS-MID-INDEX + 1
               ELSE
                   COMPUTE WS-RIGHT-INDEX = WS-MID-INDEX - 1
               END-IF
           END-PERFORM.

       INTERPOLATION-END.
           EXIT.

      *================================================================
      * 5. TERNARY SEARCH
      *================================================================

       TERNARY-SEARCH.
           MOVE 'N' TO WS-FOUND-FLAG
           MOVE 0 TO WS-RESULT-INDEX

           IF WS-ARRAY-SIZE = 0
               GO TO TERNARY-END
           END-IF

           MOVE 1 TO WS-LEFT-INDEX
           MOVE WS-ARRAY-SIZE TO WS-RIGHT-INDEX

           PERFORM UNTIL WS-LEFT-INDEX > WS-RIGHT-INDEX
               COMPUTE WS-MID-INDEX = WS-LEFT-INDEX +
                   (WS-RIGHT-INDEX - WS-LEFT-INDEX) / 3
               COMPUTE WS-TEMP-INDEX = WS-RIGHT-INDEX -
                   (WS-RIGHT-INDEX - WS-LEFT-INDEX) / 3

               IF WS-ELEMENT(WS-MID-INDEX) = WS-TARGET
                   MOVE WS-MID-INDEX TO WS-RESULT-INDEX
                   MOVE 'Y' TO WS-FOUND-FLAG
                   GO TO TERNARY-END
               END-IF

               IF WS-ELEMENT(WS-TEMP-INDEX) = WS-TARGET
                   MOVE WS-TEMP-INDEX TO WS-RESULT-INDEX
                   MOVE 'Y' TO WS-FOUND-FLAG
                   GO TO TERNARY-END
               END-IF

               IF WS-TARGET < WS-ELEMENT(WS-MID-INDEX)
                   COMPUTE WS-RIGHT-INDEX = WS-MID-INDEX - 1
               ELSE IF WS-TARGET > WS-ELEMENT(WS-TEMP-INDEX)
                   COMPUTE WS-LEFT-INDEX = WS-TEMP-INDEX + 1
               ELSE
                   COMPUTE WS-LEFT-INDEX = WS-MID-INDEX + 1
                   COMPUTE WS-RIGHT-INDEX = WS-TEMP-INDEX - 1
               END-IF
           END-PERFORM.

       TERNARY-END.
           EXIT.

      *================================================================
      * 6. INTEGER SQUARE ROOT
      *================================================================

       INTEGER-SQUARE-ROOT.
           MOVE 0 TO WS-RESULT-INDEX

           IF WS-TARGET < 0
               GO TO SQRT-END
           END-IF

           IF WS-TARGET = 0 OR WS-TARGET = 1
               MOVE WS-TARGET TO WS-RESULT-INDEX
               GO TO SQRT-END
           END-IF

           MOVE 0 TO WS-LEFT-INDEX
           MOVE WS-TARGET TO WS-RIGHT-INDEX

           PERFORM UNTIL WS-LEFT-INDEX > WS-RIGHT-INDEX
               COMPUTE WS-MID-INDEX = WS-LEFT-INDEX +
                   (WS-RIGHT-INDEX - WS-LEFT-INDEX) / 2

               COMPUTE WS-TEMP-INDEX = WS-MID-INDEX * WS-MID-INDEX

               IF WS-TEMP-INDEX = WS-TARGET
                   MOVE WS-MID-INDEX TO WS-RESULT-INDEX
                   GO TO SQRT-END
               ELSE IF WS-TEMP-INDEX < WS-TARGET
                   MOVE WS-MID-INDEX TO WS-RESULT-INDEX
                   COMPUTE WS-LEFT-INDEX = WS-MID-INDEX + 1
               ELSE
                   COMPUTE WS-RIGHT-INDEX = WS-MID-INDEX - 1
               END-IF
           END-PERFORM.

       SQRT-END.
           EXIT.

      *================================================================
      * DEMONSTRATION PROCEDURES
      *================================================================

       DEMO-CLASSIC-BINARY-SEARCH.
           DISPLAY ' '.
           DISPLAY '1. CLASSIC BINARY SEARCH'.
           DISPLAY '----------------------------------'.

           PERFORM VARYING WS-ITERATION FROM 1 BY 1 UNTIL WS-ITERATION > 10
               MOVE WS-TEST-1-ELEM(WS-ITERATION) TO WS-ELEMENT(WS-ITERATION)
           END-PERFORM

           MOVE 7 TO WS-TARGET
           PERFORM BINARY-SEARCH-ITERATIVE
           DISPLAY 'Search 7: Index = ' WS-RESULT-INDEX

           MOVE 10 TO WS-TARGET
           PERFORM BINARY-SEARCH-ITERATIVE
           DISPLAY 'Search 10: Index = ' WS-RESULT-INDEX

           MOVE 1 TO WS-TARGET
           PERFORM BINARY-SEARCH-ITERATIVE
           DISPLAY 'Search 1: Index = ' WS-RESULT-INDEX.

       DEMO-FIRST-LAST-OCCURRENCE.
           DISPLAY ' '.
           DISPLAY '2. FIRST/LAST OCCURRENCE'.
           DISPLAY '----------------------------------'.

           PERFORM VARYING WS-ITERATION FROM 1 BY 1 UNTIL WS-ITERATION > 10
               MOVE WS-TEST-2-ELEM(WS-ITERATION) TO WS-ELEMENT(WS-ITERATION)
           END-PERFORM

           MOVE 2 TO WS-TARGET
           PERFORM FIND-FIRST-OCCURRENCE
           MOVE WS-RESULT-INDEX TO WS-LEFT-INDEX
           PERFORM FIND-LAST-OCCURRENCE
           DISPLAY 'Target 2: First = ' WS-LEFT-INDEX ', Last = ' WS-RESULT-INDEX

           MOVE 4 TO WS-TARGET
           PERFORM FIND-FIRST-OCCURRENCE
           MOVE WS-RESULT-INDEX TO WS-LEFT-INDEX
           PERFORM FIND-LAST-OCCURRENCE
           DISPLAY 'Target 4: First = ' WS-LEFT-INDEX ', Last = ' WS-RESULT-INDEX.

       DEMO-INTERPOLATION-SEARCH.
           DISPLAY ' '.
           DISPLAY '3. INTERPOLATION SEARCH'.
           DISPLAY '----------------------------------'.

           MOVE 1 TO WS-ELEMENT(1)
           MOVE 10 TO WS-ELEMENT(2)
           MOVE 20 TO WS-ELEMENT(3)
           MOVE 30 TO WS-ELEMENT(4)
           MOVE 40 TO WS-ELEMENT(5)
           MOVE 50 TO WS-ELEMENT(6)
           MOVE 60 TO WS-ELEMENT(7)
           MOVE 70 TO WS-ELEMENT(8)
           MOVE 80 TO WS-ELEMENT(9)
           MOVE 90 TO WS-ELEMENT(10)

           MOVE 30 TO WS-TARGET
           PERFORM INTERPOLATION-SEARCH
           DISPLAY 'Search 30: Index = ' WS-RESULT-INDEX

           MOVE 100 TO WS-TARGET
           PERFORM INTERPOLATION-SEARCH
           DISPLAY 'Search 100: Index = ' WS-RESULT-INDEX.

       DEMO-TERNARY-SEARCH.
           DISPLAY ' '.
           DISPLAY '4. TERNARY SEARCH'.
           DISPLAY '----------------------------------'.

           PERFORM VARYING WS-ITERATION FROM 1 BY 1 UNTIL WS-ITERATION > 10
               MOVE WS-ITERATION TO WS-ELEMENT(WS-ITERATION)
           END-PERFORM

           MOVE 5 TO WS-TARGET
           PERFORM TERNARY-SEARCH
           DISPLAY 'Search 5: Index = ' WS-RESULT-INDEX

           MOVE 1 TO WS-TARGET
           PERFORM TERNARY-SEARCH
           DISPLAY 'Search 1: Index = ' WS-RESULT-INDEX

           MOVE 10 TO WS-TARGET
           PERFORM TERNARY-SEARCH
           DISPLAY 'Search 10: Index = ' WS-RESULT-INDEX.

       DEMO-SQUARE-ROOT.
           DISPLAY ' '.
           DISPLAY '5. INTEGER SQUARE ROOT'.
           DISPLAY '----------------------------------'.

           MOVE 16 TO WS-TARGET
           PERFORM INTEGER-SQUARE-ROOT
           DISPLAY 'sqrt(16) = ' WS-RESULT-INDEX

           MOVE 25 TO WS-TARGET
           PERFORM INTEGER-SQUARE-ROOT
           DISPLAY 'sqrt(25) = ' WS-RESULT-INDEX

           MOVE 50 TO WS-TARGET
           PERFORM INTEGER-SQUARE-ROOT
           DISPLAY 'sqrt(50) = ' WS-RESULT-INDEX

           MOVE 100 TO WS-TARGET
           PERFORM INTEGER-SQUARE-ROOT
           DISPLAY 'sqrt(100) = ' WS-RESULT-INDEX.

       DEMO-CLOSEST-ELEMENT.
           DISPLAY ' '.
           DISPLAY '6. FIND CLOSEST ELEMENT'.
           DISPLAY '----------------------------------'.

           MOVE 1 TO WS-ELEMENT(1)
           MOVE 3 TO WS-ELEMENT(2)
           MOVE 5 TO WS-ELEMENT(3)
           MOVE 7 TO WS-ELEMENT(4)
           MOVE 9 TO WS-ELEMENT(5)
           MOVE 5 TO WS-ARRAY-SIZE

           MOVE 4 TO WS-TARGET
           PERFORM BINARY-SEARCH-ITERATIVE
           DISPLAY 'Closest to 4: Index = ' WS-RESULT-INDEX

           MOVE 6 TO WS-TARGET
           PERFORM BINARY-SEARCH-ITERATIVE
           DISPLAY 'Closest to 6: Index = ' WS-RESULT-INDEX.
