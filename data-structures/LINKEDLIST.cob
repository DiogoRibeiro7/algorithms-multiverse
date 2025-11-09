      ******************************************************************
      * LINKED LIST IMPLEMENTATION IN COBOL
      *
      * Features:
      * - Singly linked list using array-based nodes
      * - Fixed-size node pool (COBOL limitation)
      * - Business data processing focus
      * - Insert, delete, search, traverse operations
      *
      * Compilation:
      *   cobc -x LINKEDLIST.cob -o linkedlist
      *   ./linkedlist
      *
      * Note: This uses array-based implementation as COBOL
      * doesn't have dynamic pointers like modern languages.
      ******************************************************************

       IDENTIFICATION DIVISION.
       PROGRAM-ID. LINKEDLIST.
       AUTHOR. ALGORITHMS-MULTIVERSE.

       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.

       DATA DIVISION.
       WORKING-STORAGE SECTION.

      * Configuration
       01 LL-CONFIG.
          05 MAX-NODES              PIC 9(4) VALUE 1000.
          05 FREE-HEAD              PIC 9(4) VALUE 1.
          05 LIST-HEAD              PIC 9(4) VALUE 0.
          05 LIST-SIZE              PIC 9(4) VALUE 0.

      * Node Pool (Array-based linked list)
       01 NODE-POOL.
          05 NODE-ENTRY OCCURS 1000 TIMES
                        INDEXED BY NODE-IDX.
             10 NODE-DATA           PIC 9(6).
             10 NODE-NEXT           PIC 9(4).
             10 NODE-USED           PIC 9 VALUE 0.

      * Working Variables
       01 WS-VARIABLES.
          05 WS-INDEX               PIC 9(4).
          05 WS-PREV-INDEX          PIC 9(4).
          05 WS-CURRENT-INDEX       PIC 9(4).
          05 WS-NEW-NODE-INDEX      PIC 9(4).
          05 WS-DATA                PIC 9(6).
          05 WS-FOUND               PIC 9 VALUE 0.
          05 WS-COUNTER             PIC 9(4).

      * Display Variables
       01 DISPLAY-VARS.
          05 DISPLAY-DATA           PIC Z(5)9.
          05 DISPLAY-SIZE           PIC Z(3)9.

       PROCEDURE DIVISION.

      ******************************************************************
      * MAIN PROGRAM
      ******************************************************************
       MAIN-PROCEDURE.
           PERFORM INITIALIZE-LIST
           PERFORM DEMONSTRATION
           STOP RUN.

      ******************************************************************
      * INITIALIZE LIST
      ******************************************************************
       INITIALIZE-LIST.
           MOVE 1 TO FREE-HEAD
           MOVE 0 TO LIST-HEAD
           MOVE 0 TO LIST-SIZE

           PERFORM VARYING NODE-IDX FROM 1 BY 1
                   UNTIL NODE-IDX > MAX-NODES
               MOVE 0 TO NODE-USED(NODE-IDX)
               COMPUTE NODE-NEXT(NODE-IDX) = NODE-IDX + 1
           END-PERFORM

           MOVE 0 TO NODE-NEXT(MAX-NODES)
           .

      ******************************************************************
      * FIND FREE NODE
      ******************************************************************
       FIND-FREE-NODE.
           MOVE 0 TO WS-NEW-NODE-INDEX

           IF FREE-HEAD > 0 AND FREE-HEAD <= MAX-NODES
               MOVE FREE-HEAD TO WS-NEW-NODE-INDEX
               SET NODE-IDX TO FREE-HEAD
               MOVE NODE-NEXT(NODE-IDX) TO FREE-HEAD
           END-IF
           .

      ******************************************************************
      * INSERT AT HEAD
      ******************************************************************
       INSERT-AT-HEAD.
           PERFORM FIND-FREE-NODE

           IF WS-NEW-NODE-INDEX > 0
               SET NODE-IDX TO WS-NEW-NODE-INDEX
               MOVE WS-DATA TO NODE-DATA(NODE-IDX)
               MOVE LIST-HEAD TO NODE-NEXT(NODE-IDX)
               MOVE 1 TO NODE-USED(NODE-IDX)
               MOVE WS-NEW-NODE-INDEX TO LIST-HEAD
               ADD 1 TO LIST-SIZE

               MOVE WS-DATA TO DISPLAY-DATA
               DISPLAY '  Inserted at head: ' DISPLAY-DATA
           ELSE
               DISPLAY '  ERROR: Node pool full!'
           END-IF
           .

      ******************************************************************
      * INSERT AT TAIL
      ******************************************************************
       INSERT-AT-TAIL.
           PERFORM FIND-FREE-NODE

           IF WS-NEW-NODE-INDEX > 0
               SET NODE-IDX TO WS-NEW-NODE-INDEX
               MOVE WS-DATA TO NODE-DATA(NODE-IDX)
               MOVE 0 TO NODE-NEXT(NODE-IDX)
               MOVE 1 TO NODE-USED(NODE-IDX)

               IF LIST-HEAD = 0
                   MOVE WS-NEW-NODE-INDEX TO LIST-HEAD
               ELSE
                   MOVE LIST-HEAD TO WS-CURRENT-INDEX

                   PERFORM UNTIL WS-CURRENT-INDEX = 0
                       SET NODE-IDX TO WS-CURRENT-INDEX
                       MOVE WS-CURRENT-INDEX TO WS-PREV-INDEX
                       MOVE NODE-NEXT(NODE-IDX) TO WS-CURRENT-INDEX
                   END-PERFORM

                   SET NODE-IDX TO WS-PREV-INDEX
                   MOVE WS-NEW-NODE-INDEX TO NODE-NEXT(NODE-IDX)
               END-IF

               ADD 1 TO LIST-SIZE

               MOVE WS-DATA TO DISPLAY-DATA
               DISPLAY '  Inserted at tail: ' DISPLAY-DATA
           ELSE
               DISPLAY '  ERROR: Node pool full!'
           END-IF
           .

      ******************************************************************
      * DELETE AT HEAD
      ******************************************************************
       DELETE-AT-HEAD.
           MOVE 0 TO WS-FOUND

           IF LIST-HEAD > 0
               SET NODE-IDX TO LIST-HEAD
               MOVE NODE-DATA(NODE-IDX) TO WS-DATA
               MOVE NODE-NEXT(NODE-IDX) TO WS-CURRENT-INDEX

               MOVE 0 TO NODE-USED(NODE-IDX)
               MOVE FREE-HEAD TO NODE-NEXT(NODE-IDX)
               MOVE LIST-HEAD TO FREE-HEAD

               MOVE WS-CURRENT-INDEX TO LIST-HEAD
               SUBTRACT 1 FROM LIST-SIZE
               MOVE 1 TO WS-FOUND

               MOVE WS-DATA TO DISPLAY-DATA
               DISPLAY '  Deleted from head: ' DISPLAY-DATA
           ELSE
               DISPLAY '  ERROR: List is empty!'
           END-IF
           .

      ******************************************************************
      * SEARCH
      ******************************************************************
       SEARCH-LIST.
           MOVE 0 TO WS-FOUND
           MOVE LIST-HEAD TO WS-CURRENT-INDEX

           PERFORM UNTIL WS-CURRENT-INDEX = 0 OR WS-FOUND = 1
               SET NODE-IDX TO WS-CURRENT-INDEX
               IF NODE-DATA(NODE-IDX) = WS-DATA
                   MOVE 1 TO WS-FOUND
               END-IF
               MOVE NODE-NEXT(NODE-IDX) TO WS-CURRENT-INDEX
           END-PERFORM
           .

      ******************************************************************
      * PRINT LIST
      ******************************************************************
       PRINT-LIST.
           DISPLAY '  List: ' WITH NO ADVANCING
           MOVE LIST-HEAD TO WS-CURRENT-INDEX

           PERFORM UNTIL WS-CURRENT-INDEX = 0
               SET NODE-IDX TO WS-CURRENT-INDEX
               MOVE NODE-DATA(NODE-IDX) TO DISPLAY-DATA
               DISPLAY DISPLAY-DATA WITH NO ADVANCING

               MOVE NODE-NEXT(NODE-IDX) TO WS-CURRENT-INDEX
               IF WS-CURRENT-INDEX > 0
                   DISPLAY ' -> ' WITH NO ADVANCING
               END-IF
           END-PERFORM

           DISPLAY ' -> NULL'
           .

      ******************************************************************
      * REVERSE LIST
      ******************************************************************
       REVERSE-LIST.
           MOVE 0 TO WS-PREV-INDEX
           MOVE LIST-HEAD TO WS-CURRENT-INDEX

           PERFORM UNTIL WS-CURRENT-INDEX = 0
               SET NODE-IDX TO WS-CURRENT-INDEX
               MOVE NODE-NEXT(NODE-IDX) TO WS-INDEX
               MOVE WS-PREV-INDEX TO NODE-NEXT(NODE-IDX)
               MOVE WS-CURRENT-INDEX TO WS-PREV-INDEX
               MOVE WS-INDEX TO WS-CURRENT-INDEX
           END-PERFORM

           MOVE WS-PREV-INDEX TO LIST-HEAD
           .

      ******************************************************************
      * DEMONSTRATION
      ******************************************************************
       DEMONSTRATION.
           DISPLAY repeat('=', 80)
           DISPLAY 'LINKED LIST IMPLEMENTATION IN COBOL'
           DISPLAY repeat('=', 80)
           DISPLAY ' '

           DISPLAY '1. SINGLY LINKED LIST OPERATIONS'
           DISPLAY repeat('-', 80)

           DISPLAY 'Inserting: 100, 200, 300 at head'
           MOVE 300 TO WS-DATA
           PERFORM INSERT-AT-HEAD
           MOVE 200 TO WS-DATA
           PERFORM INSERT-AT-HEAD
           MOVE 100 TO WS-DATA
           PERFORM INSERT-AT-HEAD

           DISPLAY ' '
           PERFORM PRINT-LIST

           DISPLAY ' '
           DISPLAY 'Inserting: 400, 500 at tail'
           MOVE 400 TO WS-DATA
           PERFORM INSERT-AT-TAIL
           MOVE 500 TO WS-DATA
           PERFORM INSERT-AT-TAIL

           DISPLAY ' '
           PERFORM PRINT-LIST

           DISPLAY ' '
           MOVE LIST-SIZE TO DISPLAY-SIZE
           DISPLAY 'List size: ' DISPLAY-SIZE

           DISPLAY ' '
           DISPLAY 'Searching for 300...'
           MOVE 300 TO WS-DATA
           PERFORM SEARCH-LIST
           IF WS-FOUND = 1
               DISPLAY '  Found: 300'
           ELSE
               DISPLAY '  Not found'
           END-IF

           DISPLAY ' '
           DISPLAY 'Searching for 999...'
           MOVE 999 TO WS-DATA
           PERFORM SEARCH-LIST
           IF WS-FOUND = 1
               DISPLAY '  Found: 999'
           ELSE
               DISPLAY '  Not found'
           END-IF

           DISPLAY ' '
           DISPLAY 'Reversing list...'
           PERFORM REVERSE-LIST
           PERFORM PRINT-LIST

           DISPLAY ' '
           DISPLAY 'Deleting from head...'
           PERFORM DELETE-AT-HEAD
           PERFORM PRINT-LIST

           DISPLAY ' '
           MOVE LIST-SIZE TO DISPLAY-SIZE
           DISPLAY 'Final size: ' DISPLAY-SIZE

           DISPLAY ' '
           DISPLAY repeat('=', 80)
           DISPLAY '✨ All demonstrations complete!'
           DISPLAY repeat('=', 80)
           .

       END PROGRAM LINKEDLIST.
