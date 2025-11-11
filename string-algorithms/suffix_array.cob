       IDENTIFICATION DIVISION.
       PROGRAM-ID. SUFFIX-ARRAY.
       AUTHOR. Algorithms Multiverse.
      *================================================================*
      * SUFFIX ARRAY AND LCP ARRAY CONSTRUCTION IN COBOL              *
      *================================================================*
      * Implements:                                                    *
      * - Naive suffix array construction O(n² log n)                 *
      * - Kasai's algorithm for LCP array O(n)                        *
      *                                                                *
      * Applications:                                                  *
      * - Pattern matching                                             *
      * - Finding repeated substrings                                  *
      * - Counting distinct substrings                                 *
      *                                                                *
      * Compilation:                                                   *
      * cobc -x -free suffix_array.cob -o suffix_array                *
      *================================================================*

       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       SOURCE-COMPUTER. IBM-PC.
       OBJECT-COMPUTER. IBM-PC.

       DATA DIVISION.
       WORKING-STORAGE SECTION.

       01  WS-CONSTANTS.
           05  MAX-TEXT-LENGTH     PIC 9(4) VALUE 100.
           05  SEPARATOR-CHAR      PIC X VALUE '#'.

       01  WS-TEXT.
           05  TEXT-STRING         PIC X(100).
           05  TEXT-LENGTH         PIC 9(4).

       01  WS-PATTERN.
           05  PATTERN-STRING      PIC X(50).
           05  PATTERN-LENGTH      PIC 9(4).

       01  WS-SUFFIX-ARRAY.
           05  SA-ENTRY OCCURS 100 TIMES.
               10  SA-INDEX        PIC 9(4).
               10  SA-SUFFIX       PIC X(100).

       01  WS-LCP-ARRAY.
           05  LCP-ENTRY OCCURS 100 TIMES.
               10  LCP-VALUE       PIC 9(4).

       01  WS-RANK-ARRAY.
           05  RANK-ENTRY OCCURS 100 TIMES.
               10  RANK-VALUE      PIC 9(4).

       01  WS-COUNTERS.
           05  I                   PIC 9(4).
           05  J                   PIC 9(4).
           05  K                   PIC 9(4).
           05  H                   PIC 9(4).
           05  TEMP-IDX            PIC 9(4).
           05  MATCH-COUNT         PIC 9(4).

       01  WS-RESULTS.
           05  MAX-LCP             PIC 9(4).
           05  MAX-LCP-IDX         PIC 9(4).
           05  DISTINCT-COUNT      PIC 9(8).
           05  TOTAL-SUBSTRINGS    PIC 9(8).
           05  DUPLICATE-SUM       PIC 9(8).

       01  WS-TEMP-VALUES.
           05  TEMP-SA-INDEX       PIC 9(4).
           05  TEMP-SA-SUFFIX      PIC X(100).
           05  TEMP-CHAR           PIC X.
           05  MATCH-FLAG          PIC 9 VALUE 0.

       01  WS-DISPLAY.
           05  DISPLAY-LINE        PIC X(80).
           05  DISPLAY-SUFFIX      PIC X(40).

       PROCEDURE DIVISION.
       MAIN-PROCEDURE.
           DISPLAY "======================================"
           DISPLAY "SUFFIX ARRAY IN COBOL"
           DISPLAY "======================================"
           DISPLAY " "

           PERFORM EXAMPLE-BASIC-CONSTRUCTION
           PERFORM EXAMPLE-PATTERN-SEARCH
           PERFORM EXAMPLE-LONGEST-REPEATED
           PERFORM EXAMPLE-COUNT-DISTINCT

           DISPLAY "======================================"
           DISPLAY "All examples completed!"
           DISPLAY "======================================"

           STOP RUN.

      *================================================================*
      * BUILD SUFFIX ARRAY (NAIVE ALGORITHM)                          *
      *================================================================*
       BUILD-SUFFIX-ARRAY.
           PERFORM VARYING I FROM 1 BY 1 UNTIL I > TEXT-LENGTH
               MOVE I TO SA-INDEX(I)
               MOVE TEXT-STRING(I:TEXT-LENGTH - I + 1)
                   TO SA-SUFFIX(I)
           END-PERFORM

      * Sort suffixes using bubble sort
           PERFORM BUBBLE-SORT-SUFFIXES

           EXIT.

      *================================================================*
      * BUBBLE SORT FOR SUFFIXES                                       *
      *================================================================*
       BUBBLE-SORT-SUFFIXES.
           PERFORM VARYING I FROM 1 BY 1
               UNTIL I >= TEXT-LENGTH
               PERFORM VARYING J FROM 1 BY 1
                   UNTIL J > TEXT-LENGTH - I
                   IF SA-SUFFIX(J) > SA-SUFFIX(J + 1)
                       MOVE SA-INDEX(J) TO TEMP-SA-INDEX
                       MOVE SA-SUFFIX(J) TO TEMP-SA-SUFFIX

                       MOVE SA-INDEX(J + 1) TO SA-INDEX(J)
                       MOVE SA-SUFFIX(J + 1) TO SA-SUFFIX(J)

                       MOVE TEMP-SA-INDEX TO SA-INDEX(J + 1)
                       MOVE TEMP-SA-SUFFIX TO SA-SUFFIX(J + 1)
                   END-IF
               END-PERFORM
           END-PERFORM
           EXIT.

      *================================================================*
      * BUILD LCP ARRAY (KASAI'S ALGORITHM)                           *
      *================================================================*
       BUILD-LCP-ARRAY.
      * Initialize LCP array
           PERFORM VARYING I FROM 1 BY 1 UNTIL I > TEXT-LENGTH
               MOVE 0 TO LCP-VALUE(I)
           END-PERFORM

      * Build rank array (inverse of suffix array)
           PERFORM VARYING I FROM 1 BY 1 UNTIL I > TEXT-LENGTH
               MOVE I TO RANK-VALUE(SA-INDEX(I))
           END-PERFORM

      * Compute LCP values
           MOVE 0 TO H
           PERFORM VARYING I FROM 1 BY 1 UNTIL I > TEXT-LENGTH
               IF RANK-VALUE(I) > 1
                   COMPUTE J = SA-INDEX(RANK-VALUE(I) - 1)

      * Compute LCP between suffix at I and suffix at J
                   PERFORM COMPUTE-LCP-VALUE

                   MOVE H TO LCP-VALUE(RANK-VALUE(I))

      * Decrease H for next iteration
                   IF H > 0
                       SUBTRACT 1 FROM H
                   END-IF
               END-IF
           END-PERFORM

           EXIT.

      *================================================================*
      * COMPUTE LCP VALUE BETWEEN TWO SUFFIXES                        *
      *================================================================*
       COMPUTE-LCP-VALUE.
           MOVE 0 TO H
           PERFORM VARYING K FROM 1 BY 1
               UNTIL K > TEXT-LENGTH
                   OR I + H > TEXT-LENGTH
                   OR J + H > TEXT-LENGTH
               IF TEXT-STRING(I + H:1) = TEXT-STRING(J + H:1)
                   ADD 1 TO H
               ELSE
                   EXIT PERFORM
               END-IF
           END-PERFORM
           EXIT.

      *================================================================*
      * PATTERN SEARCH USING SUFFIX ARRAY                             *
      *================================================================*
       PATTERN-SEARCH.
           MOVE 0 TO MATCH-COUNT

           PERFORM VARYING I FROM 1 BY 1 UNTIL I > TEXT-LENGTH
               MOVE 1 TO MATCH-FLAG

      * Check if pattern matches at this suffix
               IF PATTERN-LENGTH <=
                   (TEXT-LENGTH - SA-INDEX(I) + 1)
                   PERFORM VARYING J FROM 1 BY 1
                       UNTIL J > PATTERN-LENGTH
                       COMPUTE TEMP-IDX = SA-INDEX(I) + J - 1
                       IF TEXT-STRING(TEMP-IDX:1) NOT =
                           PATTERN-STRING(J:1)
                           MOVE 0 TO MATCH-FLAG
                           EXIT PERFORM
                       END-IF
                   END-PERFORM

                   IF MATCH-FLAG = 1
                       ADD 1 TO MATCH-COUNT
                       DISPLAY "  Match at position " SA-INDEX(I)
                   END-IF
               END-IF
           END-PERFORM

           EXIT.

      *================================================================*
      * FIND LONGEST REPEATED SUBSTRING                               *
      *================================================================*
       LONGEST-REPEATED-SUBSTRING.
           MOVE 0 TO MAX-LCP
           MOVE 0 TO MAX-LCP-IDX

      * Find maximum LCP value
           PERFORM VARYING I FROM 2 BY 1 UNTIL I > TEXT-LENGTH
               IF LCP-VALUE(I) > MAX-LCP
                   MOVE LCP-VALUE(I) TO MAX-LCP
                   MOVE I TO MAX-LCP-IDX
               END-IF
           END-PERFORM

           IF MAX-LCP = 0
               DISPLAY "No repeated substring found"
           ELSE
               MOVE TEXT-STRING(SA-INDEX(MAX-LCP-IDX):MAX-LCP)
                   TO DISPLAY-SUFFIX
               DISPLAY "Longest repeated substring: '"
                   DISPLAY-SUFFIX(1:MAX-LCP) "'"
           END-IF

           EXIT.

      *================================================================*
      * COUNT DISTINCT SUBSTRINGS                                     *
      *================================================================*
       COUNT-DISTINCT-SUBSTRINGS.
      * Total substrings = n * (n + 1) / 2
           COMPUTE TOTAL-SUBSTRINGS =
               TEXT-LENGTH * (TEXT-LENGTH + 1) / 2

      * Sum of LCP array
           MOVE 0 TO DUPLICATE-SUM
           PERFORM VARYING I FROM 2 BY 1 UNTIL I > TEXT-LENGTH
               ADD LCP-VALUE(I) TO DUPLICATE-SUM
           END-PERFORM

      * Distinct substrings = total - duplicates
           COMPUTE DISTINCT-COUNT =
               TOTAL-SUBSTRINGS - DUPLICATE-SUM

           DISPLAY "Total substrings: " TOTAL-SUBSTRINGS
           DISPLAY "Duplicate substrings: " DUPLICATE-SUM
           DISPLAY "Distinct substrings: " DISTINCT-COUNT

           EXIT.

      *================================================================*
      * VISUALIZE SUFFIX ARRAY                                        *
      *================================================================*
       VISUALIZE-SUFFIX-ARRAY.
           DISPLAY " "
           DISPLAY "Suffix Array Visualization:"
           DISPLAY "Text: '" TEXT-STRING(1:TEXT-LENGTH) "'"
           DISPLAY "Length: " TEXT-LENGTH
           DISPLAY " "
           DISPLAY "  i | SA[i] | LCP[i] | Suffix"
           DISPLAY "----+-------+--------+----------------"

           PERFORM VARYING I FROM 1 BY 1 UNTIL I > TEXT-LENGTH
               MOVE SA-SUFFIX(I) TO DISPLAY-SUFFIX
               IF SA-SUFFIX(I) > SPACES
                   DISPLAY I " | " SA-INDEX(I) " | "
                       LCP-VALUE(I) " | " DISPLAY-SUFFIX(1:40)
               END-IF
           END-PERFORM

           DISPLAY " "
           EXIT.

      *================================================================*
      * EXAMPLE 1: BASIC CONSTRUCTION                                 *
      *================================================================*
       EXAMPLE-BASIC-CONSTRUCTION.
           DISPLAY "======================================"
           DISPLAY "EXAMPLE 1: Basic Construction"
           DISPLAY "======================================"

           MOVE "banana" TO TEXT-STRING
           MOVE 6 TO TEXT-LENGTH

           PERFORM BUILD-SUFFIX-ARRAY
           PERFORM BUILD-LCP-ARRAY
           PERFORM VISUALIZE-SUFFIX-ARRAY

           EXIT.

      *================================================================*
      * EXAMPLE 2: PATTERN SEARCHING                                  *
      *================================================================*
       EXAMPLE-PATTERN-SEARCH.
           DISPLAY "======================================"
           DISPLAY "EXAMPLE 2: Pattern Searching"
           DISPLAY "======================================"

           MOVE "banana republic" TO TEXT-STRING
           MOVE 15 TO TEXT-LENGTH
           MOVE "ana" TO PATTERN-STRING
           MOVE 3 TO PATTERN-LENGTH

           PERFORM BUILD-SUFFIX-ARRAY

           DISPLAY "Text: '" TEXT-STRING(1:TEXT-LENGTH) "'"
           DISPLAY "Pattern: '" PATTERN-STRING(1:PATTERN-LENGTH)
               "'"
           DISPLAY "Matches:"

           PERFORM PATTERN-SEARCH

           IF MATCH-COUNT = 0
               DISPLAY "  No matches found"
           ELSE
               DISPLAY "Total matches: " MATCH-COUNT
           END-IF

           DISPLAY " "
           EXIT.

      *================================================================*
      * EXAMPLE 3: LONGEST REPEATED SUBSTRING                         *
      *================================================================*
       EXAMPLE-LONGEST-REPEATED.
           DISPLAY "======================================"
           DISPLAY "EXAMPLE 3: Longest Repeated Substring"
           DISPLAY "======================================"

           MOVE "abracadabra" TO TEXT-STRING
           MOVE 11 TO TEXT-LENGTH

           PERFORM BUILD-SUFFIX-ARRAY
           PERFORM BUILD-LCP-ARRAY

           DISPLAY "Text: '" TEXT-STRING(1:TEXT-LENGTH) "'"
           PERFORM LONGEST-REPEATED-SUBSTRING

           DISPLAY " "
           EXIT.

      *================================================================*
      * EXAMPLE 4: COUNT DISTINCT SUBSTRINGS                          *
      *================================================================*
       EXAMPLE-COUNT-DISTINCT.
           DISPLAY "======================================"
           DISPLAY "EXAMPLE 4: Count Distinct Substrings"
           DISPLAY "======================================"

           MOVE "abab" TO TEXT-STRING
           MOVE 4 TO TEXT-LENGTH

           PERFORM BUILD-SUFFIX-ARRAY
           PERFORM BUILD-LCP-ARRAY

           DISPLAY "Text: '" TEXT-STRING(1:TEXT-LENGTH) "'"
           PERFORM COUNT-DISTINCT-SUBSTRINGS

           DISPLAY " "
           EXIT.

       END PROGRAM SUFFIX-ARRAY.
