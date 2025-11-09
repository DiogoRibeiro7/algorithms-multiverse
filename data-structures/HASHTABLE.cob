      ******************************************************************
      * HASH TABLE IMPLEMENTATION IN COBOL
      *
      * Features:
      * - Separate chaining for collision resolution (simplified)
      * - Fixed-size buckets (no dynamic resizing in standard COBOL)
      * - String keys and numeric values
      * - Basic hash function
      * - Insert, search, and delete operations
      * - Performance statistics
      *
      * Time Complexity:
      * - Average: O(1) for insert, delete, search
      * - Worst:   O(n) for chaining with poor hash function
      *
      * Space Complexity: O(n) where n is the number of elements
      *
      * Compilation and Usage:
      *   cobc -x HASHTABLE.cob -o hashtable
      *   ./hashtable
      *
      * Or with GnuCOBOL:
      *   cobc -free -x HASHTABLE.cob
      *   ./HASHTABLE
      *
      * Note: This is a simplified implementation due to COBOL's
      * limitations. Modern COBOL (COBOL 2002+) would support
      * more advanced features, but this uses COBOL-85 standard.
      ******************************************************************

       IDENTIFICATION DIVISION.
       PROGRAM-ID. HASHTABLE.
       AUTHOR. ALGORITHMS-MULTIVERSE.

       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.

       DATA DIVISION.
       WORKING-STORAGE SECTION.

      * Hash Table Configuration
       01 HT-CONFIG.
          05 HT-CAPACITY            PIC 9(4) VALUE 100.
          05 HT-MAX-CHAIN-LENGTH    PIC 9(3) VALUE 10.
          05 HT-SIZE                PIC 9(4) VALUE 0.

      * Hash Table Entry (Chain Node)
       01 HT-ENTRY.
          05 HT-KEY                 PIC X(20).
          05 HT-VALUE               PIC 9(6).
          05 HT-NEXT-INDEX          PIC 9(4).
          05 HT-IS-USED             PIC 9 VALUE 0.

      * Hash Table Buckets (Array of head indices)
       01 HT-BUCKETS.
          05 HT-BUCKET OCCURS 100 TIMES
                       INDEXED BY BUCKET-IDX.
             10 HT-HEAD-INDEX       PIC 9(4) VALUE 0.

      * Entry Storage (Pool of entries for chains)
       01 HT-ENTRIES.
          05 HT-ENTRY-REC OCCURS 1000 TIMES
                          INDEXED BY ENTRY-IDX.
             10 ENTRY-KEY           PIC X(20).
             10 ENTRY-VALUE         PIC 9(6).
             10 ENTRY-NEXT          PIC 9(4) VALUE 0.
             10 ENTRY-USED          PIC 9 VALUE 0.

      * Statistics
       01 HT-STATS.
          05 HT-COLLISIONS          PIC 9(6) VALUE 0.
          05 HT-SEARCHES            PIC 9(6) VALUE 0.
          05 HT-INSERTS             PIC 9(6) VALUE 0.
          05 HT-DELETES             PIC 9(6) VALUE 0.

      * Working Variables
       01 WS-VARIABLES.
          05 WS-HASH-VALUE          PIC 9(9).
          05 WS-INDEX               PIC 9(4).
          05 WS-TEMP-INDEX          PIC 9(4).
          05 WS-PREV-INDEX          PIC 9(4).
          05 WS-KEY                 PIC X(20).
          05 WS-VALUE               PIC 9(6).
          05 WS-FOUND               PIC 9 VALUE 0.
          05 WS-COUNTER             PIC 9(4).
          05 WS-CHAR                PIC X.
          05 WS-CHAR-VALUE          PIC 9(3).
          05 WS-I                   PIC 9(4).

      * Display Variables
       01 DISPLAY-VARS.
          05 DISPLAY-KEY            PIC X(20).
          05 DISPLAY-VALUE          PIC Z(5)9.
          05 DISPLAY-SIZE           PIC Z(3)9.
          05 DISPLAY-STATS          PIC Z(5)9.

       PROCEDURE DIVISION.

      ******************************************************************
      * MAIN PROGRAM
      ******************************************************************
       MAIN-PROCEDURE.
           PERFORM INITIALIZE-HASH-TABLE
           PERFORM DEMONSTRATION
           STOP RUN.

      ******************************************************************
      * DEMONSTRATION ROUTINE
      ******************************************************************
       DEMONSTRATION.
           DISPLAY "==========================================="
           DISPLAY "Hash Table Implementation in COBOL"
           DISPLAY "==========================================="
           DISPLAY " "

           DISPLAY "1. Inserting elements..."
           DISPLAY "-----------------------------------------"
           PERFORM INSERT-TEST-DATA

           DISPLAY " "
           MOVE HT-SIZE TO DISPLAY-SIZE
           DISPLAY "Size: " DISPLAY-SIZE
           DISPLAY " "

           DISPLAY "2. Retrieving elements..."
           DISPLAY "-----------------------------------------"
           PERFORM RETRIEVE-TEST-DATA

           DISPLAY " "
           DISPLAY "3. Testing containment..."
           DISPLAY "-----------------------------------------"
           PERFORM TEST-CONTAINMENT

           DISPLAY " "
           DISPLAY "4. Updating values..."
           DISPLAY "-----------------------------------------"
           PERFORM UPDATE-TEST-DATA

           DISPLAY " "
           DISPLAY "5. Removing elements..."
           DISPLAY "-----------------------------------------"
           PERFORM DELETE-TEST-DATA

           DISPLAY " "
           DISPLAY "6. Performance Statistics"
           DISPLAY "-----------------------------------------"
           PERFORM PRINT-STATISTICS

           DISPLAY " "
           DISPLAY "==========================================="
           DISPLAY "Hash table demonstration complete!"
           DISPLAY "==========================================="
           .

      ******************************************************************
      * INITIALIZE HASH TABLE
      ******************************************************************
       INITIALIZE-HASH-TABLE.
           MOVE 0 TO HT-SIZE
           MOVE 0 TO HT-COLLISIONS
           MOVE 0 TO HT-SEARCHES
           MOVE 0 TO HT-INSERTS
           MOVE 0 TO HT-DELETES

           PERFORM VARYING BUCKET-IDX FROM 1 BY 1
                   UNTIL BUCKET-IDX > HT-CAPACITY
               MOVE 0 TO HT-HEAD-INDEX(BUCKET-IDX)
           END-PERFORM

           PERFORM VARYING ENTRY-IDX FROM 1 BY 1
                   UNTIL ENTRY-IDX > 1000
               MOVE 0 TO ENTRY-USED(ENTRY-IDX)
               MOVE 0 TO ENTRY-NEXT(ENTRY-IDX)
           END-PERFORM
           .

      ******************************************************************
      * HASH FUNCTION (Simple String Hash)
      ******************************************************************
       COMPUTE-HASH.
           MOVE 0 TO WS-HASH-VALUE
           PERFORM VARYING WS-I FROM 1 BY 1
                   UNTIL WS-I > FUNCTION LENGTH(
                                FUNCTION TRIM(WS-KEY))
               MOVE WS-KEY(WS-I:1) TO WS-CHAR
               COMPUTE WS-CHAR-VALUE =
                       FUNCTION ORD(WS-CHAR)
               COMPUTE WS-HASH-VALUE =
                       WS-HASH-VALUE * 31 + WS-CHAR-VALUE
           END-PERFORM

           COMPUTE WS-INDEX =
                   FUNCTION MOD(WS-HASH-VALUE, HT-CAPACITY) + 1
           .

      ******************************************************************
      * FIND FREE ENTRY SLOT
      ******************************************************************
       FIND-FREE-ENTRY.
           MOVE 0 TO WS-TEMP-INDEX
           PERFORM VARYING ENTRY-IDX FROM 1 BY 1
                   UNTIL ENTRY-IDX > 1000
                     OR ENTRY-USED(ENTRY-IDX) = 0
               CONTINUE
           END-PERFORM

           IF ENTRY-IDX <= 1000
               MOVE ENTRY-IDX TO WS-TEMP-INDEX
           END-IF
           .

      ******************************************************************
      * INSERT KEY-VALUE PAIR
      ******************************************************************
       HT-INSERT.
           ADD 1 TO HT-INSERTS
           MOVE WS-KEY TO DISPLAY-KEY
           MOVE WS-VALUE TO DISPLAY-VALUE

           PERFORM COMPUTE-HASH

           SET BUCKET-IDX TO WS-INDEX

      *    Check if key already exists (update)
           MOVE HT-HEAD-INDEX(BUCKET-IDX) TO WS-TEMP-INDEX
           PERFORM UNTIL WS-TEMP-INDEX = 0
               SET ENTRY-IDX TO WS-TEMP-INDEX
               IF ENTRY-KEY(ENTRY-IDX) = WS-KEY
                   MOVE WS-VALUE TO ENTRY-VALUE(ENTRY-IDX)
                   DISPLAY "  Updated: " DISPLAY-KEY
                           " -> " DISPLAY-VALUE
                   EXIT PARAGRAPH
               END-IF
               MOVE ENTRY-NEXT(ENTRY-IDX) TO WS-TEMP-INDEX
           END-PERFORM

      *    Key not found, insert new entry
           PERFORM FIND-FREE-ENTRY

           IF WS-TEMP-INDEX > 0
               SET ENTRY-IDX TO WS-TEMP-INDEX
               MOVE WS-KEY TO ENTRY-KEY(ENTRY-IDX)
               MOVE WS-VALUE TO ENTRY-VALUE(ENTRY-IDX)
               MOVE 1 TO ENTRY-USED(ENTRY-IDX)

               IF HT-HEAD-INDEX(BUCKET-IDX) = 0
                   MOVE WS-TEMP-INDEX TO HT-HEAD-INDEX(BUCKET-IDX)
               ELSE
                   ADD 1 TO HT-COLLISIONS
                   MOVE HT-HEAD-INDEX(BUCKET-IDX) TO
                        ENTRY-NEXT(ENTRY-IDX)
                   MOVE WS-TEMP-INDEX TO HT-HEAD-INDEX(BUCKET-IDX)
               END-IF

               ADD 1 TO HT-SIZE
               DISPLAY "  Inserted: " DISPLAY-KEY
                       " -> " DISPLAY-VALUE
           ELSE
               DISPLAY "  ERROR: Hash table full!"
           END-IF
           .

      ******************************************************************
      * SEARCH FOR KEY
      ******************************************************************
       HT-SEARCH.
           ADD 1 TO HT-SEARCHES
           MOVE 0 TO WS-FOUND
           MOVE 0 TO WS-VALUE

           PERFORM COMPUTE-HASH
           SET BUCKET-IDX TO WS-INDEX

           MOVE HT-HEAD-INDEX(BUCKET-IDX) TO WS-TEMP-INDEX

           PERFORM UNTIL WS-TEMP-INDEX = 0 OR WS-FOUND = 1
               SET ENTRY-IDX TO WS-TEMP-INDEX
               IF ENTRY-KEY(ENTRY-IDX) = WS-KEY
                   MOVE ENTRY-VALUE(ENTRY-IDX) TO WS-VALUE
                   MOVE 1 TO WS-FOUND
               END-IF
               MOVE ENTRY-NEXT(ENTRY-IDX) TO WS-TEMP-INDEX
           END-PERFORM
           .

      ******************************************************************
      * DELETE KEY
      ******************************************************************
       HT-DELETE.
           ADD 1 TO HT-DELETES

           PERFORM COMPUTE-HASH
           SET BUCKET-IDX TO WS-INDEX

           MOVE HT-HEAD-INDEX(BUCKET-IDX) TO WS-TEMP-INDEX
           MOVE 0 TO WS-PREV-INDEX
           MOVE 0 TO WS-FOUND

           PERFORM UNTIL WS-TEMP-INDEX = 0 OR WS-FOUND = 1
               SET ENTRY-IDX TO WS-TEMP-INDEX
               IF ENTRY-KEY(ENTRY-IDX) = WS-KEY
                   IF WS-PREV-INDEX = 0
                       MOVE ENTRY-NEXT(ENTRY-IDX) TO
                            HT-HEAD-INDEX(BUCKET-IDX)
                   ELSE
                       SET ENTRY-IDX TO WS-PREV-INDEX
                       MOVE WS-TEMP-INDEX TO WS-INDEX
                       SET ENTRY-IDX TO WS-INDEX
                       MOVE ENTRY-NEXT(ENTRY-IDX) TO WS-INDEX
                       SET ENTRY-IDX TO WS-PREV-INDEX
                       MOVE WS-INDEX TO ENTRY-NEXT(ENTRY-IDX)
                   END-IF

                   SET ENTRY-IDX TO WS-TEMP-INDEX
                   MOVE 0 TO ENTRY-USED(ENTRY-IDX)
                   SUBTRACT 1 FROM HT-SIZE
                   MOVE 1 TO WS-FOUND
               END-IF

               MOVE WS-TEMP-INDEX TO WS-PREV-INDEX
               SET ENTRY-IDX TO WS-TEMP-INDEX
               MOVE ENTRY-NEXT(ENTRY-IDX) TO WS-TEMP-INDEX
           END-PERFORM
           .

      ******************************************************************
      * TEST DATA OPERATIONS
      ******************************************************************
       INSERT-TEST-DATA.
           PERFORM VARYING WS-COUNTER FROM 0 BY 1
                   UNTIL WS-COUNTER >= 10
               STRING "KEY" WS-COUNTER DELIMITED BY SIZE
                      INTO WS-KEY
               COMPUTE WS-VALUE = WS-COUNTER * 10
               PERFORM HT-INSERT
           END-PERFORM
           .

       RETRIEVE-TEST-DATA.
           MOVE "KEY0" TO WS-KEY
           PERFORM HT-SEARCH
           MOVE WS-KEY TO DISPLAY-KEY
           IF WS-FOUND = 1
               MOVE WS-VALUE TO DISPLAY-VALUE
               DISPLAY "  Get '" DISPLAY-KEY "': " DISPLAY-VALUE
           ELSE
               DISPLAY "  Get '" DISPLAY-KEY "': Not found"
           END-IF

           MOVE "KEY5" TO WS-KEY
           PERFORM HT-SEARCH
           MOVE WS-KEY TO DISPLAY-KEY
           IF WS-FOUND = 1
               MOVE WS-VALUE TO DISPLAY-VALUE
               DISPLAY "  Get '" DISPLAY-KEY "': " DISPLAY-VALUE
           ELSE
               DISPLAY "  Get '" DISPLAY-KEY "': Not found"
           END-IF

           MOVE "NONEXISTENT" TO WS-KEY
           PERFORM HT-SEARCH
           MOVE WS-KEY TO DISPLAY-KEY
           IF WS-FOUND = 1
               MOVE WS-VALUE TO DISPLAY-VALUE
               DISPLAY "  Get '" DISPLAY-KEY "': " DISPLAY-VALUE
           ELSE
               DISPLAY "  Get '" DISPLAY-KEY "': Not found"
           END-IF
           .

       TEST-CONTAINMENT.
           MOVE "KEY3" TO WS-KEY
           PERFORM HT-SEARCH
           MOVE WS-KEY TO DISPLAY-KEY
           IF WS-FOUND = 1
               DISPLAY "  Contains '" DISPLAY-KEY "': TRUE"
           ELSE
               DISPLAY "  Contains '" DISPLAY-KEY "': FALSE"
           END-IF

           MOVE "MISSING" TO WS-KEY
           PERFORM HT-SEARCH
           MOVE WS-KEY TO DISPLAY-KEY
           IF WS-FOUND = 1
               DISPLAY "  Contains '" DISPLAY-KEY "': TRUE"
           ELSE
               DISPLAY "  Contains '" DISPLAY-KEY "': FALSE"
           END-IF
           .

       UPDATE-TEST-DATA.
           MOVE "KEY5" TO WS-KEY
           MOVE 999 TO WS-VALUE
           PERFORM HT-INSERT
           .

       DELETE-TEST-DATA.
           MOVE "KEY7" TO WS-KEY
           PERFORM HT-DELETE
           MOVE WS-KEY TO DISPLAY-KEY
           IF WS-FOUND = 1
               DISPLAY "  Removed '" DISPLAY-KEY "': Success"
           ELSE
               DISPLAY "  Removed '" DISPLAY-KEY "': Not found"
           END-IF

           MOVE HT-SIZE TO DISPLAY-SIZE
           DISPLAY "  Size after removal: " DISPLAY-SIZE
           .

      ******************************************************************
      * PRINT STATISTICS
      ******************************************************************
       PRINT-STATISTICS.
           DISPLAY "Hash Table Statistics:"

           MOVE HT-SIZE TO DISPLAY-STATS
           DISPLAY "  Size:        " DISPLAY-STATS

           MOVE HT-CAPACITY TO DISPLAY-STATS
           DISPLAY "  Capacity:    " DISPLAY-STATS

           MOVE HT-COLLISIONS TO DISPLAY-STATS
           DISPLAY "  Collisions:  " DISPLAY-STATS

           MOVE HT-INSERTS TO DISPLAY-STATS
           DISPLAY "  Inserts:     " DISPLAY-STATS

           MOVE HT-SEARCHES TO DISPLAY-STATS
           DISPLAY "  Searches:    " DISPLAY-STATS

           MOVE HT-DELETES TO DISPLAY-STATS
           DISPLAY "  Deletes:     " DISPLAY-STATS
           .

       END PROGRAM HASHTABLE.
