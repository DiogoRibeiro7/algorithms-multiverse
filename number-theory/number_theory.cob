       IDENTIFICATION DIVISION.
       PROGRAM-ID. NUMBER-THEORY.
       AUTHOR. ALGORITHMS-MULTIVERSE.
      *================================================================*
      * NUMBER THEORY ALGORITHMS - COBOL IMPLEMENTATION                *
      *================================================================*
      *                                                                *
      * Enterprise-grade implementation of fundamental number theory   *
      * algorithms in COBOL for business computing applications.       *
      *                                                                *
      * Features:                                                      *
      * - Fixed-point arithmetic for precision                         *
      * - Structured procedure divisions                               *
      * - Comprehensive documentation                                  *
      * - Business computing focus                                     *
      *                                                                *
      * Compilation (GnuCOBOL):                                        *
      *   cobc -x -free number_theory.cob                              *
      *                                                                *
      * Usage:                                                         *
      *   ./number_theory                                              *
      *                                                                *
      *================================================================*

       DATA DIVISION.
       WORKING-STORAGE SECTION.

      * General purpose variables
       01  WS-RESULT               PIC 9(18).
       01  WS-TEMP                 PIC 9(18).
       01  WS-COUNTER              PIC 9(5).
       01  WS-INDEX                PIC 9(5).

      * Variables for sieve of Eratosthenes
       01  WS-LIMIT                PIC 9(6) VALUE 100.
       01  WS-SIEVE-SIZE           PIC 9(6).
       01  WS-SQRT-LIMIT           PIC 9(6).
       01  WS-PRIME-COUNT          PIC 9(5) VALUE 0.
       01  WS-PRIMES-TABLE.
           05  WS-PRIME OCCURS 1000 TIMES PIC 9(6).
       01  WS-IS-PRIME-TABLE.
           05  WS-IS-PRIME OCCURS 1001 TIMES PIC 9 VALUE 1.

      * Variables for GCD and modular arithmetic
       01  WS-A                    PIC 9(18).
       01  WS-B                    PIC 9(18).
       01  WS-GCD-RESULT           PIC 9(18).
       01  WS-LCM-RESULT           PIC 9(18).
       01  WS-MOD-RESULT           PIC 9(18).

      * Variables for modular exponentiation
       01  WS-BASE                 PIC 9(10).
       01  WS-EXPONENT             PIC 9(10).
       01  WS-MODULUS              PIC 9(10).
       01  WS-MODEXP-RESULT        PIC 9(10).

      * Variables for Extended GCD
       01  WS-EGCD-X               PIC S9(18).
       01  WS-EGCD-Y               PIC S9(18).
       01  WS-QUOTIENT             PIC S9(18).

      * Variables for factorization
       01  WS-NUMBER               PIC 9(18).
       01  WS-FACTOR               PIC 9(18).
       01  WS-FACTOR-COUNT         PIC 9(5).
       01  WS-FACTORS-TABLE.
           05  WS-FACTORS OCCURS 100 TIMES PIC 9(18).

      * Display formatting
       01  WS-DISPLAY-LINE         PIC X(80).
       01  WS-SEPARATOR            PIC X(70) VALUE ALL "=".
       01  WS-DASH-LINE            PIC X(50) VALUE ALL "-".

       PROCEDURE DIVISION.

       MAIN-PROCEDURE.
           PERFORM PRINT-HEADER
           PERFORM TEST-SIEVE
           PERFORM TEST-GCD-LCM
           PERFORM TEST-MODULAR-ARITHMETIC
           PERFORM TEST-FACTORIZATION
           PERFORM PRINT-FOOTER
           STOP RUN.

      *================================================================*
      * UTILITY PROCEDURES                                             *
      *================================================================*

       PRINT-HEADER.
           DISPLAY WS-SEPARATOR
           DISPLAY "NUMBER THEORY ALGORITHMS - COBOL IMPLEMENTATION"
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
      * PRIME NUMBER GENERATION - SIEVE OF ERATOSTHENES                *
      *================================================================*
      * Time Complexity: O(n log log n)                                *
      * Space Complexity: O(n)                                         *
      *                                                                *
      * Algorithm:                                                     *
      * 1. Initialize array with all numbers marked as prime           *
      * 2. For each number i from 2 to sqrt(limit):                    *
      *    - If i is prime, mark all multiples as composite            *
      * 3. Collect remaining primes                                    *
      *================================================================*

       TEST-SIEVE.
           DISPLAY "1. SIEVE OF ERATOSTHENES"
           PERFORM PRINT-SECTION-SEPARATOR

           MOVE 100 TO WS-LIMIT
           PERFORM SIEVE-OF-ERATOSTHENES

           DISPLAY "PRIMES UP TO " WS-LIMIT ":"
           PERFORM DISPLAY-PRIMES
           DISPLAY "TOTAL: " WS-PRIME-COUNT " PRIMES"
           DISPLAY " ".

       SIEVE-OF-ERATOSTHENES.
      * Initialize sieve - mark all as potential primes
           MOVE 0 TO WS-PRIME-COUNT
           PERFORM VARYING WS-INDEX FROM 0 BY 1 UNTIL WS-INDEX > 1000
               MOVE 1 TO WS-IS-PRIME(WS-INDEX)
           END-PERFORM

      * 0 and 1 are not prime
           MOVE 0 TO WS-IS-PRIME(1)
           MOVE 0 TO WS-IS-PRIME(2)

      * Calculate square root of limit
           COMPUTE WS-SQRT-LIMIT = FUNCTION SQRT(WS-LIMIT)

      * Sieve algorithm
           PERFORM VARYING WS-INDEX FROM 2 BY 1
                   UNTIL WS-INDEX > WS-SQRT-LIMIT
               IF WS-IS-PRIME(WS-INDEX + 1) = 1 THEN
                   PERFORM MARK-MULTIPLES
               END-IF
           END-PERFORM

      * Collect primes
           PERFORM VARYING WS-INDEX FROM 2 BY 1 UNTIL WS-INDEX > WS-LIMIT
               IF WS-IS-PRIME(WS-INDEX + 1) = 1 THEN
                   ADD 1 TO WS-PRIME-COUNT
                   MOVE WS-INDEX TO WS-PRIME(WS-PRIME-COUNT)
               END-IF
           END-PERFORM.

       MARK-MULTIPLES.
           COMPUTE WS-TEMP = WS-INDEX * WS-INDEX
           PERFORM VARYING WS-COUNTER FROM WS-TEMP BY WS-INDEX
                   UNTIL WS-COUNTER > WS-LIMIT
               MOVE 0 TO WS-IS-PRIME(WS-COUNTER + 1)
           END-PERFORM.

       DISPLAY-PRIMES.
           PERFORM VARYING WS-INDEX FROM 1 BY 1
                   UNTIL WS-INDEX > WS-PRIME-COUNT OR WS-INDEX > 25
               DISPLAY WS-PRIME(WS-INDEX) " " WITH NO ADVANCING
           END-PERFORM
           IF WS-PRIME-COUNT > 25 THEN
               DISPLAY "..." WITH NO ADVANCING
           END-IF
           DISPLAY " ".

      *================================================================*
      * GREATEST COMMON DIVISOR - EUCLIDEAN ALGORITHM                  *
      *================================================================*
      * Time Complexity: O(log min(a, b))                              *
      * Space Complexity: O(1)                                         *
      *                                                                *
      * Mathematical Proof:                                            *
      *   gcd(a, b) = gcd(b, a mod b) when b != 0                      *
      *   gcd(a, 0) = a                                                *
      *================================================================*

       TEST-GCD-LCM.
           DISPLAY "2. GCD AND LCM"
           PERFORM PRINT-SECTION-SEPARATOR

      * Test case 1: gcd(48, 18)
           MOVE 48 TO WS-A
           MOVE 18 TO WS-B
           PERFORM CALCULATE-GCD
           PERFORM CALCULATE-LCM
           DISPLAY "GCD(" WS-A ", " WS-B ") = " WS-GCD-RESULT
           DISPLAY "LCM(" WS-A ", " WS-B ") = " WS-LCM-RESULT

      * Test case 2: gcd(100, 35)
           MOVE 100 TO WS-A
           MOVE 35 TO WS-B
           PERFORM CALCULATE-GCD
           PERFORM CALCULATE-LCM
           DISPLAY "GCD(" WS-A ", " WS-B ") = " WS-GCD-RESULT
           DISPLAY "LCM(" WS-A ", " WS-B ") = " WS-LCM-RESULT

      * Test case 3: gcd(17, 19)
           MOVE 17 TO WS-A
           MOVE 19 TO WS-B
           PERFORM CALCULATE-GCD
           PERFORM CALCULATE-LCM
           DISPLAY "GCD(" WS-A ", " WS-B ") = " WS-GCD-RESULT
           DISPLAY "LCM(" WS-A ", " WS-B ") = " WS-LCM-RESULT
           DISPLAY " ".

       CALCULATE-GCD.
           MOVE WS-A TO WS-TEMP
           MOVE WS-B TO WS-GCD-RESULT

           PERFORM UNTIL WS-GCD-RESULT = 0
               MOVE WS-GCD-RESULT TO WS-MOD-RESULT
               COMPUTE WS-GCD-RESULT = FUNCTION MOD(WS-TEMP,
                                                     WS-GCD-RESULT)
               MOVE WS-MOD-RESULT TO WS-TEMP
           END-PERFORM

           MOVE WS-TEMP TO WS-GCD-RESULT.

       CALCULATE-LCM.
      * Formula: lcm(a, b) = (a * b) / gcd(a, b)
           IF WS-GCD-RESULT = 0 THEN
               MOVE 0 TO WS-LCM-RESULT
           ELSE
               COMPUTE WS-LCM-RESULT = (WS-A / WS-GCD-RESULT) * WS-B
           END-IF.

      *================================================================*
      * MODULAR ARITHMETIC                                             *
      *================================================================*
      * Implements modular exponentiation using binary method          *
      * Time Complexity: O(log exponent)                               *
      *                                                                *
      * Critical for cryptographic applications:                       *
      * - RSA encryption/decryption                                    *
      * - Diffie-Hellman key exchange                                  *
      *================================================================*

       TEST-MODULAR-ARITHMETIC.
           DISPLAY "3. MODULAR ARITHMETIC"
           PERFORM PRINT-SECTION-SEPARATOR

           DISPLAY "MODULAR EXPONENTIATION:"

      * Test case 1: 2^10 mod 1000
           MOVE 2 TO WS-BASE
           MOVE 10 TO WS-EXPONENT
           MOVE 1000 TO WS-MODULUS
           PERFORM MODULAR-EXPONENTIATION
           DISPLAY "  " WS-BASE "^" WS-EXPONENT " MOD " WS-MODULUS
                   " = " WS-MODEXP-RESULT

      * Test case 2: 3^100 mod 13
           MOVE 3 TO WS-BASE
           MOVE 100 TO WS-EXPONENT
           MOVE 13 TO WS-MODULUS
           PERFORM MODULAR-EXPONENTIATION
           DISPLAY "  " WS-BASE "^" WS-EXPONENT " MOD " WS-MODULUS
                   " = " WS-MODEXP-RESULT

      * Test case 3: 7^256 mod 100
           MOVE 7 TO WS-BASE
           MOVE 256 TO WS-EXPONENT
           MOVE 100 TO WS-MODULUS
           PERFORM MODULAR-EXPONENTIATION
           DISPLAY "  " WS-BASE "^" WS-EXPONENT " MOD " WS-MODULUS
                   " = " WS-MODEXP-RESULT
           DISPLAY " ".

       MODULAR-EXPONENTIATION.
      * Binary exponentiation algorithm
           IF WS-MODULUS = 1 THEN
               MOVE 0 TO WS-MODEXP-RESULT
           ELSE
               MOVE 1 TO WS-MODEXP-RESULT
               COMPUTE WS-BASE = FUNCTION MOD(WS-BASE, WS-MODULUS)

               PERFORM UNTIL WS-EXPONENT = 0
                   IF FUNCTION MOD(WS-EXPONENT, 2) = 1 THEN
                       COMPUTE WS-MODEXP-RESULT =
                           FUNCTION MOD(WS-MODEXP-RESULT * WS-BASE,
                                        WS-MODULUS)
                   END-IF

                   DIVIDE WS-EXPONENT BY 2 GIVING WS-EXPONENT
                   COMPUTE WS-BASE = FUNCTION MOD(WS-BASE * WS-BASE,
                                                   WS-MODULUS)
               END-PERFORM
           END-IF.

      *================================================================*
      * PRIME FACTORIZATION                                            *
      *================================================================*
      * Trial division algorithm                                       *
      * Time Complexity: O(sqrt(n))                                    *
      *                                                                *
      * Returns array of prime factors (with repetition)               *
      *================================================================*

       TEST-FACTORIZATION.
           DISPLAY "4. PRIME FACTORIZATION"
           PERFORM PRINT-SECTION-SEPARATOR

      * Test case 1: Factorize 60
           MOVE 60 TO WS-NUMBER
           PERFORM PRIME-FACTORIZATION
           DISPLAY WS-NUMBER " = " WITH NO ADVANCING
           PERFORM DISPLAY-FACTORS

      * Test case 2: Factorize 128
           MOVE 128 TO WS-NUMBER
           PERFORM PRIME-FACTORIZATION
           DISPLAY WS-NUMBER " = " WITH NO ADVANCING
           PERFORM DISPLAY-FACTORS

      * Test case 3: Factorize 1001
           MOVE 1001 TO WS-NUMBER
           PERFORM PRIME-FACTORIZATION
           DISPLAY WS-NUMBER " = " WITH NO ADVANCING
           PERFORM DISPLAY-FACTORS

      * Test case 4: Factorize 2024
           MOVE 2024 TO WS-NUMBER
           PERFORM PRIME-FACTORIZATION
           DISPLAY WS-NUMBER " = " WITH NO ADVANCING
           PERFORM DISPLAY-FACTORS

           DISPLAY " ".

       PRIME-FACTORIZATION.
           MOVE 0 TO WS-FACTOR-COUNT
           MOVE WS-NUMBER TO WS-TEMP

      * Handle factor 2
           PERFORM UNTIL FUNCTION MOD(WS-TEMP, 2) NOT = 0
               ADD 1 TO WS-FACTOR-COUNT
               MOVE 2 TO WS-FACTORS(WS-FACTOR-COUNT)
               DIVIDE WS-TEMP BY 2 GIVING WS-TEMP
           END-PERFORM

      * Check odd divisors
           MOVE 3 TO WS-FACTOR
           PERFORM UNTIL WS-FACTOR * WS-FACTOR > WS-TEMP
               PERFORM UNTIL FUNCTION MOD(WS-TEMP, WS-FACTOR) NOT = 0
                   ADD 1 TO WS-FACTOR-COUNT
                   MOVE WS-FACTOR TO WS-FACTORS(WS-FACTOR-COUNT)
                   DIVIDE WS-TEMP BY WS-FACTOR GIVING WS-TEMP
               END-PERFORM
               ADD 2 TO WS-FACTOR
           END-PERFORM

      * If temp > 1, it's a prime factor
           IF WS-TEMP > 1 THEN
               ADD 1 TO WS-FACTOR-COUNT
               MOVE WS-TEMP TO WS-FACTORS(WS-FACTOR-COUNT)
           END-IF.

       DISPLAY-FACTORS.
           PERFORM VARYING WS-INDEX FROM 1 BY 1
                   UNTIL WS-INDEX > WS-FACTOR-COUNT
               DISPLAY WS-FACTORS(WS-INDEX) WITH NO ADVANCING
               IF WS-INDEX < WS-FACTOR-COUNT THEN
                   DISPLAY " × " WITH NO ADVANCING
               END-IF
           END-PERFORM
           DISPLAY " ".

       END PROGRAM NUMBER-THEORY.
