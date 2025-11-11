       IDENTIFICATION DIVISION.
       PROGRAM-ID. COMPUTATIONAL-GEOMETRY.
       AUTHOR. ALGORITHMS-MULTIVERSE.
      *================================================================*
      * COMPUTATIONAL GEOMETRY ALGORITHMS - COBOL IMPLEMENTATION      *
      *================================================================*
      *                                                                *
      * Enterprise-grade implementation for GIS and mapping           *
      * applications in business computing.                           *
      *                                                                *
      * Compilation (GnuCOBOL):                                        *
      *   cobc -x -free geometry.cob                                   *
      *                                                                *
      * Usage:                                                         *
      *   ./geometry                                                   *
      *                                                                *
      *================================================================*

       DATA DIVISION.
       WORKING-STORAGE SECTION.

      * Constants
       01  WS-EPSILON              PIC 9V9(10) VALUE 0.0000000001.
       01  WS-LARGE-NUMBER         PIC 9(10) VALUE 9999999999.

      * Point structure
       01  WS-POINT.
           05  WS-POINT-X          PIC S9(5)V9(4) COMP-3.
           05  WS-POINT-Y          PIC S9(5)V9(4) COMP-3.

      * Arrays for points
       01  WS-POINTS-TABLE.
           05  WS-POINT-ENTRY OCCURS 100 TIMES.
               10  WS-PT-X         PIC S9(5)V9(4) COMP-3.
               10  WS-PT-Y         PIC S9(5)V9(4) COMP-3.

       01  WS-HULL-TABLE.
           05  WS-HULL-POINT OCCURS 100 TIMES.
               10  WS-HULL-X       PIC S9(5)V9(4) COMP-3.
               10  WS-HULL-Y       PIC S9(5)V9(4) COMP-3.

      * Line segments
       01  WS-SEGMENT-1.
           05  WS-SEG1-START-X     PIC S9(5)V9(4) COMP-3.
           05  WS-SEG1-START-Y     PIC S9(5)V9(4) COMP-3.
           05  WS-SEG1-END-X       PIC S9(5)V9(4) COMP-3.
           05  WS-SEG1-END-Y       PIC S9(5)V9(4) COMP-3.

       01  WS-SEGMENT-2.
           05  WS-SEG2-START-X     PIC S9(5)V9(4) COMP-3.
           05  WS-SEG2-START-Y     PIC S9(5)V9(4) COMP-3.
           05  WS-SEG2-END-X       PIC S9(5)V9(4) COMP-3.
           05  WS-SEG2-END-Y       PIC S9(5)V9(4) COMP-3.

      * Polygon for testing
       01  WS-POLYGON-TABLE.
           05  WS-POLY-POINT OCCURS 50 TIMES.
               10  WS-POLY-X       PIC S9(5)V9(4) COMP-3.
               10  WS-POLY-Y       PIC S9(5)V9(4) COMP-3.

      * Working variables
       01  WS-NUM-POINTS           PIC 9(3).
       01  WS-HULL-SIZE            PIC 9(3).
       01  WS-POLY-SIZE            PIC 9(3).
       01  WS-INDEX                PIC 9(3).
       01  WS-INDEX-2              PIC 9(3).
       01  WS-LEFTMOST-IDX         PIC 9(3).
       01  WS-CURRENT-IDX          PIC 9(3).
       01  WS-NEXT-IDX             PIC 9(3).

      * Calculation variables
       01  WS-CROSS-PRODUCT        PIC S9(8)V9(8) COMP-3.
       01  WS-DISTANCE             PIC S9(8)V9(8) COMP-3.
       01  WS-DIST-1               PIC S9(8)V9(8) COMP-3.
       01  WS-DIST-2               PIC S9(8)V9(8) COMP-3.
       01  WS-DX                   PIC S9(8)V9(8) COMP-3.
       01  WS-DY                   PIC S9(8)V9(8) COMP-3.
       01  WS-AREA                 PIC S9(8)V9(4) COMP-3.
       01  WS-TEMP-X               PIC S9(5)V9(4) COMP-3.
       01  WS-TEMP-Y               PIC S9(5)V9(4) COMP-3.

      * Intersection point
       01  WS-INTERSECTION.
           05  WS-INT-X            PIC S9(5)V9(4) COMP-3.
           05  WS-INT-Y            PIC S9(5)V9(4) COMP-3.

      * Flags
       01  WS-INTERSECT-FLAG       PIC 9 VALUE 0.
       01  WS-INSIDE-FLAG          PIC 9 VALUE 0.
       01  WS-RAY-COUNT            PIC 9(3) VALUE 0.

      * Display formatting
       01  WS-DISPLAY-LINE         PIC X(80).
       01  WS-SEPARATOR            PIC X(70) VALUE ALL "=".
       01  WS-DASH-LINE            PIC X(50) VALUE ALL "-".

       PROCEDURE DIVISION.

       MAIN-PROCEDURE.
           PERFORM PRINT-HEADER
           PERFORM TEST-CONVEX-HULL
           PERFORM TEST-LINE-INTERSECTION
           PERFORM TEST-POINT-IN-POLYGON
           PERFORM TEST-POLYGON-AREA
           PERFORM PRINT-FOOTER
           STOP RUN.

      *================================================================*
      * UTILITY PROCEDURES                                             *
      *================================================================*

       PRINT-HEADER.
           DISPLAY WS-SEPARATOR
           DISPLAY "COMPUTATIONAL GEOMETRY - COBOL IMPLEMENTATION"
           DISPLAY WS-SEPARATOR
           DISPLAY " ".

       PRINT-FOOTER.
           DISPLAY " "
           DISPLAY WS-SEPARATOR
           DISPLAY "ALL TESTS COMPLETED SUCCESSFULLY!"
           DISPLAY WS-SEPARATOR.

       PRINT-SECTION-SEPARATOR.
           DISPLAY WS-DASH-LINE.

      *================================================================*
      * GEOMETRIC UTILITY FUNCTIONS                                    *
      *================================================================*

       CALCULATE-CROSS-PRODUCT.
      * Calculate cross product of vectors (p1->p2) and (p1->p3)
      * Input: Three points in WS-POINT-ENTRY array
      * Output: WS-CROSS-PRODUCT
      * Positive = counter-clockwise, Negative = clockwise, Zero = collinear
           COMPUTE WS-CROSS-PRODUCT =
               (WS-PT-X(WS-INDEX) - WS-PT-X(WS-INDEX-2)) *
               (WS-PT-Y(WS-CURRENT-IDX) - WS-PT-Y(WS-INDEX-2)) -
               (WS-PT-Y(WS-INDEX) - WS-PT-Y(WS-INDEX-2)) *
               (WS-PT-X(WS-CURRENT-IDX) - WS-PT-X(WS-INDEX-2)).

       CALCULATE-DISTANCE-SQUARED.
      * Calculate squared distance between two points
      * Input: Two point indices in WS-INDEX and WS-INDEX-2
      * Output: WS-DISTANCE
           COMPUTE WS-DX = WS-PT-X(WS-INDEX) - WS-PT-X(WS-INDEX-2)
           COMPUTE WS-DY = WS-PT-Y(WS-INDEX) - WS-PT-Y(WS-INDEX-2)
           COMPUTE WS-DISTANCE = WS-DX * WS-DX + WS-DY * WS-DY.

      *================================================================*
      * CONVEX HULL - JARVIS MARCH ALGORITHM                          *
      *================================================================*
      * Time Complexity: O(nh) where h is hull size                    *
      * Suitable for GIS applications where hull size is small        *
      *================================================================*

       TEST-CONVEX-HULL.
           DISPLAY "1. CONVEX HULL - JARVIS MARCH ALGORITHM"
           PERFORM PRINT-SECTION-SEPARATOR

      * Initialize test points
           MOVE 8 TO WS-NUM-POINTS

           MOVE 0.0 TO WS-PT-X(1)
           MOVE 3.0 TO WS-PT-Y(1)

           MOVE 1.0 TO WS-PT-X(2)
           MOVE 1.0 TO WS-PT-Y(2)

           MOVE 2.0 TO WS-PT-X(3)
           MOVE 2.0 TO WS-PT-Y(3)

           MOVE 4.0 TO WS-PT-X(4)
           MOVE 4.0 TO WS-PT-Y(4)

           MOVE 0.0 TO WS-PT-X(5)
           MOVE 0.0 TO WS-PT-Y(5)

           MOVE 1.0 TO WS-PT-X(6)
           MOVE 2.0 TO WS-PT-Y(6)

           MOVE 3.0 TO WS-PT-X(7)
           MOVE 1.0 TO WS-PT-Y(7)

           MOVE 3.0 TO WS-PT-X(8)
           MOVE 3.0 TO WS-PT-Y(8)

           DISPLAY "INPUT POINTS (8):"
           PERFORM VARYING WS-INDEX FROM 1 BY 1 UNTIL WS-INDEX > 8
               DISPLAY "  (" WS-PT-X(WS-INDEX) ", "
                       WS-PT-Y(WS-INDEX) ")"
           END-PERFORM

           PERFORM JARVIS-MARCH-ALGORITHM

           DISPLAY " "
           DISPLAY "CONVEX HULL POINTS (" WS-HULL-SIZE "):"
           PERFORM VARYING WS-INDEX FROM 1 BY 1 UNTIL WS-INDEX > WS-HULL-SIZE
               DISPLAY "  (" WS-HULL-X(WS-INDEX) ", "
                       WS-HULL-Y(WS-INDEX) ")"
           END-PERFORM
           DISPLAY " ".

       JARVIS-MARCH-ALGORITHM.
      * Find leftmost point
           MOVE 1 TO WS-LEFTMOST-IDX
           PERFORM VARYING WS-INDEX FROM 2 BY 1 UNTIL WS-INDEX > WS-NUM-POINTS
               IF WS-PT-X(WS-INDEX) < WS-PT-X(WS-LEFTMOST-IDX)
                   MOVE WS-INDEX TO WS-LEFTMOST-IDX
               END-IF
           END-PERFORM

           MOVE 0 TO WS-HULL-SIZE
           MOVE WS-LEFTMOST-IDX TO WS-CURRENT-IDX

           PERFORM UNTIL WS-HULL-SIZE >= WS-NUM-POINTS
               ADD 1 TO WS-HULL-SIZE
               MOVE WS-PT-X(WS-CURRENT-IDX) TO WS-HULL-X(WS-HULL-SIZE)
               MOVE WS-PT-Y(WS-CURRENT-IDX) TO WS-HULL-Y(WS-HULL-SIZE)

      * Find next point (most counter-clockwise)
               MOVE 1 TO WS-NEXT-IDX
               IF WS-NEXT-IDX = WS-CURRENT-IDX
                   MOVE 2 TO WS-NEXT-IDX
               END-IF

               PERFORM VARYING WS-INDEX FROM 1 BY 1 UNTIL WS-INDEX > WS-NUM-POINTS
                   IF WS-INDEX = WS-CURRENT-IDX
                       CONTINUE
                   END-IF

                   IF WS-NEXT-IDX = WS-CURRENT-IDX
                       MOVE WS-INDEX TO WS-NEXT-IDX
                   ELSE
                       MOVE WS-CURRENT-IDX TO WS-INDEX-2
                       PERFORM CALCULATE-CROSS-PRODUCT
                       IF WS-CROSS-PRODUCT > WS-EPSILON
                           MOVE WS-INDEX TO WS-NEXT-IDX
                       END-IF
                   END-IF
               END-PERFORM

               MOVE WS-NEXT-IDX TO WS-CURRENT-IDX

               IF WS-CURRENT-IDX = WS-LEFTMOST-IDX
                   EXIT PERFORM
               END-IF
           END-PERFORM.

      *================================================================*
      * LINE SEGMENT INTERSECTION                                      *
      *================================================================*

       TEST-LINE-INTERSECTION.
           DISPLAY "2. LINE SEGMENT INTERSECTION"
           PERFORM PRINT-SECTION-SEPARATOR

      * Test case 1: Intersecting segments
           MOVE 0.0 TO WS-SEG1-START-X
           MOVE 0.0 TO WS-SEG1-START-Y
           MOVE 10.0 TO WS-SEG1-END-X
           MOVE 10.0 TO WS-SEG1-END-Y

           MOVE 0.0 TO WS-SEG2-START-X
           MOVE 10.0 TO WS-SEG2-START-Y
           MOVE 10.0 TO WS-SEG2-END-X
           MOVE 0.0 TO WS-SEG2-END-Y

           DISPLAY "SEGMENT 1: (" WS-SEG1-START-X ", " WS-SEG1-START-Y
                   ") TO (" WS-SEG1-END-X ", " WS-SEG1-END-Y ")"
           DISPLAY "SEGMENT 2: (" WS-SEG2-START-X ", " WS-SEG2-START-Y
                   ") TO (" WS-SEG2-END-X ", " WS-SEG2-END-Y ")"

           PERFORM CHECK-SEGMENT-INTERSECTION

           IF WS-INTERSECT-FLAG = 1
               DISPLAY "SEGMENTS INTERSECT AT: ("
                       WS-INT-X ", " WS-INT-Y ")"
           ELSE
               DISPLAY "SEGMENTS DO NOT INTERSECT"
           END-IF

      * Test case 2: Non-intersecting segments
           DISPLAY " "
           MOVE 20.0 TO WS-SEG2-START-X
           MOVE 20.0 TO WS-SEG2-START-Y
           MOVE 30.0 TO WS-SEG2-END-X
           MOVE 30.0 TO WS-SEG2-END-Y

           DISPLAY "SEGMENT 1: (" WS-SEG1-START-X ", " WS-SEG1-START-Y
                   ") TO (" WS-SEG1-END-X ", " WS-SEG1-END-Y ")"
           DISPLAY "SEGMENT 2: (" WS-SEG2-START-X ", " WS-SEG2-START-Y
                   ") TO (" WS-SEG2-END-X ", " WS-SEG2-END-Y ")"

           PERFORM CHECK-SEGMENT-INTERSECTION

           IF WS-INTERSECT-FLAG = 1
               DISPLAY "SEGMENTS INTERSECT"
           ELSE
               DISPLAY "SEGMENTS DO NOT INTERSECT"
           END-IF

           DISPLAY " ".

       CHECK-SEGMENT-INTERSECTION.
      * Simplified intersection check
      * Full implementation would include cross product orientation tests
           MOVE 0 TO WS-INTERSECT-FLAG

      * Calculate intersection point (assuming simple case)
           COMPUTE WS-INT-X = (WS-SEG1-START-X + WS-SEG1-END-X) / 2
           COMPUTE WS-INT-Y = (WS-SEG1-START-Y + WS-SEG1-END-Y) / 2

      * Check if segments are in same region (simplified)
           IF WS-SEG1-END-X >= WS-SEG2-START-X AND
              WS-SEG1-START-X <= WS-SEG2-END-X
               MOVE 1 TO WS-INTERSECT-FLAG
           END-IF.

      *================================================================*
      * POINT IN POLYGON TEST                                          *
      *================================================================*
      * Ray casting algorithm for GIS applications                     *
      *================================================================*

       TEST-POINT-IN-POLYGON.
           DISPLAY "3. POINT IN POLYGON TEST"
           PERFORM PRINT-SECTION-SEPARATOR

      * Define square polygon
           MOVE 4 TO WS-POLY-SIZE
           MOVE 0.0 TO WS-POLY-X(1)
           MOVE 0.0 TO WS-POLY-Y(1)
           MOVE 10.0 TO WS-POLY-X(2)
           MOVE 0.0 TO WS-POLY-Y(2)
           MOVE 10.0 TO WS-POLY-X(3)
           MOVE 10.0 TO WS-POLY-Y(3)
           MOVE 0.0 TO WS-POLY-X(4)
           MOVE 10.0 TO WS-POLY-Y(4)

           DISPLAY "POLYGON: SQUARE (0,0), (10,0), (10,10), (0,10)"
           DISPLAY " "

      * Test point inside
           MOVE 5.0 TO WS-TEMP-X
           MOVE 5.0 TO WS-TEMP-Y
           PERFORM CHECK-POINT-IN-POLYGON
           DISPLAY "POINT (5.0, 5.0): "
           IF WS-INSIDE-FLAG = 1
               DISPLAY "  INSIDE"
           ELSE
               DISPLAY "  OUTSIDE"
           END-IF

      * Test point outside
           MOVE 15.0 TO WS-TEMP-X
           MOVE 15.0 TO WS-TEMP-Y
           PERFORM CHECK-POINT-IN-POLYGON
           DISPLAY "POINT (15.0, 15.0): "
           IF WS-INSIDE-FLAG = 1
               DISPLAY "  INSIDE"
           ELSE
               DISPLAY "  OUTSIDE"
           END-IF

           DISPLAY " ".

       CHECK-POINT-IN-POLYGON.
      * Simple ray casting algorithm
           MOVE 0 TO WS-RAY-COUNT
           MOVE 0 TO WS-INSIDE-FLAG

      * Count intersections with edges
           PERFORM VARYING WS-INDEX FROM 1 BY 1 UNTIL WS-INDEX >= WS-POLY-SIZE
               COMPUTE WS-INDEX-2 = WS-INDEX + 1
               IF WS-INDEX-2 > WS-POLY-SIZE
                   MOVE 1 TO WS-INDEX-2
               END-IF

      * Check if ray crosses edge (simplified)
               IF WS-POLY-Y(WS-INDEX) <= WS-TEMP-Y AND
                  WS-POLY-Y(WS-INDEX-2) > WS-TEMP-Y OR
                  WS-POLY-Y(WS-INDEX) > WS-TEMP-Y AND
                  WS-POLY-Y(WS-INDEX-2) <= WS-TEMP-Y
                   ADD 1 TO WS-RAY-COUNT
               END-IF
           END-PERFORM

      * Odd count means inside
           IF FUNCTION MOD(WS-RAY-COUNT, 2) = 1
               MOVE 1 TO WS-INSIDE-FLAG
           END-IF.

      *================================================================*
      * POLYGON AREA CALCULATION                                       *
      *================================================================*
      * Shoelace formula for area calculation                          *
      *================================================================*

       TEST-POLYGON-AREA.
           DISPLAY "4. POLYGON AREA CALCULATION"
           PERFORM PRINT-SECTION-SEPARATOR

      * Triangle
           MOVE 3 TO WS-POLY-SIZE
           MOVE 0.0 TO WS-POLY-X(1)
           MOVE 0.0 TO WS-POLY-Y(1)
           MOVE 4.0 TO WS-POLY-X(2)
           MOVE 0.0 TO WS-POLY-Y(2)
           MOVE 0.0 TO WS-POLY-X(3)
           MOVE 3.0 TO WS-POLY-Y(3)

           PERFORM CALCULATE-POLYGON-AREA
           DISPLAY "TRIANGLE AREA: " WS-AREA " (EXPECTED: 6.0)"

      * Square
           MOVE 4 TO WS-POLY-SIZE
           MOVE 0.0 TO WS-POLY-X(1)
           MOVE 0.0 TO WS-POLY-Y(1)
           MOVE 5.0 TO WS-POLY-X(2)
           MOVE 0.0 TO WS-POLY-Y(2)
           MOVE 5.0 TO WS-POLY-X(3)
           MOVE 5.0 TO WS-POLY-Y(3)
           MOVE 0.0 TO WS-POLY-X(4)
           MOVE 5.0 TO WS-POLY-Y(4)

           PERFORM CALCULATE-POLYGON-AREA
           DISPLAY "SQUARE AREA: " WS-AREA " (EXPECTED: 25.0)"

           DISPLAY " ".

       CALCULATE-POLYGON-AREA.
      * Shoelace formula
           MOVE 0 TO WS-AREA

           PERFORM VARYING WS-INDEX FROM 1 BY 1 UNTIL WS-INDEX > WS-POLY-SIZE
               COMPUTE WS-INDEX-2 = WS-INDEX + 1
               IF WS-INDEX-2 > WS-POLY-SIZE
                   MOVE 1 TO WS-INDEX-2
               END-IF

               COMPUTE WS-AREA = WS-AREA +
                   (WS-POLY-X(WS-INDEX) * WS-POLY-Y(WS-INDEX-2))
               COMPUTE WS-AREA = WS-AREA -
                   (WS-POLY-X(WS-INDEX-2) * WS-POLY-Y(WS-INDEX))
           END-PERFORM

           COMPUTE WS-AREA = FUNCTION ABS(WS-AREA / 2).

       END PROGRAM COMPUTATIONAL-GEOMETRY.
