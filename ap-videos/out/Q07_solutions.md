# Question 7 — Sums of multiples

## (i) Find the sum of all natural numbers less than 100 which are divisible by 6.

- **Natural numbers below 100 divisible by 6 are 6, 12, 18, and so on, up to 96**
  - `a = 6,   d = 6,   l = 96`
- **Why 96? Because 6 × 16 = 96 and 6 × 17 = 102 is more than 100**
  - `96 = 6 × 16`
- **Find the number of terms with the nth term formula**
  - `aₙ = a + (n − 1)d`
  - `96 = 6 + (n − 1)(6)`
  - `96 − 6 = 6(n − 1)`
  - `90 = 6(n − 1)`
  - `n − 1 = {90|6} = 15`
  - `n = 16`
- **Use the second sum formula**
  - `S₁₆ = {16|2} (6 + 96)`
  - `= 8 × 102`
  - `= 816`

**Answer:** `Sum = 816`

- *Check — Quick check: 6 × (1 + 2 + … + 16)*: `6 × {16 × 17|2} = 6 × 136 = 816`

## (ii) Find the sum of all 3-digit natural numbers which are divisible by 13.

- **The smallest 3-digit multiple of 13: 13 × 7 = 91 has only two digits, 13 × 8 = 104 has three**
  - `a = 104`
- **The biggest 3-digit multiple of 13: 13 × 76 = 988 and 13 × 77 = 1001 has four digits**
  - `l = 988,   d = 13`
- **Find the number of terms**
  - `988 = 104 + (n − 1)(13)`
  - `988 − 104 = 13(n − 1)`
  - `884 = 13(n − 1)`
  - `n − 1 = {884|13} = 68`
  - `n = 69`
- **Use the second sum formula**
  - `S₆₉ = {69|2} (104 + 988)`
  - `= {69|2} × 1092`
- **1092 divided by 2 is 546, then multiply 69 by 546**
  - `= 69 × 546`
  - `= 70 × 546 − 546`
  - `= 38220 − 546`
  - `= 37674`

**Answer:** `Sum = 37674`

- *Check — Quick check: 13 × (8 + 9 + … + 76)*: `13 × 2898 = 37674`

## (iii) Find the sum of all multiples of 9 lying between 300 and 700.

- **Multiples of 9 just above 300: 9 × 33 = 297 is below 300, 9 × 34 = 306 is above**
  - `a = 306`
- **Multiples of 9 just below 700: 9 × 77 = 693 is below 700, 9 × 78 = 702 is above**
  - `l = 693,   d = 9`
- **Find the number of terms**
  - `693 = 306 + (n − 1)(9)`
  - `693 − 306 = 9(n − 1)`
  - `387 = 9(n − 1)`
  - `n − 1 = {387|9} = 43`
  - `n = 44`
- **Use the second sum formula**
  - `S₄₄ = {44|2} (306 + 693)`
  - `= 22 × 999`
- **22 times 999 is 22 times 1000 minus 22**
  - `= 22000 − 22`
  - `= 21978`

**Answer:** `Sum = 21978`

- *Check — Quick check: 9 × (34 + 35 + … + 77)*: `9 × 2442 = 21978`

## (iv) Find the sum of the first hundred even natural numbers which are divisible by 5.

- **Even numbers divisible by 5 are the multiples of 10**
  - `10, 20, 30, 40, …`
- **So the first term is 10, the common difference is 10, and we need 100 terms**
  - `a = 10,   d = 10,   n = 100`
- **Use the sum formula**
  - `S₁₀₀ = {100|2} [2(10) + (100 − 1)(10)]`
- **Work inside the bracket**
  - `= 50 [20 + 990]`
  - `= 50 × 1010`
- **Multiply**
  - `= 50500`

**Answer:** `Sum = 50500`

- *Check — Quick check: the 100th term is 1000*: `S₁₀₀ = 50 (10 + 1000) = 50 × 1010 = 50500`

## (v) Find the sum of all 3-digit natural numbers which are divisible by 11.

- **Smallest 3-digit multiple of 11: 11 × 9 = 99 has two digits, 11 × 10 = 110 has three**
  - `a = 110`
- **Largest 3-digit multiple of 11: 11 × 90 = 990 and 11 × 91 = 1001 has four digits**
  - `l = 990,   d = 11`
- **Find the number of terms**
  - `990 = 110 + (n − 1)(11)`
  - `990 − 110 = 11(n − 1)`
  - `880 = 11(n − 1)`
  - `n − 1 = {880|11} = 80`
  - `n = 81`
- **Use the second sum formula**
  - `S₈₁ = {81|2} (110 + 990)`
  - `= {81|2} × 1100`
  - `= 81 × 550`
- **Multiply 81 by 550**
  - `= 81 × 500 + 81 × 50`
  - `= 40500 + 4050`
  - `= 44550`

**Answer:** `Sum = 44550`

- *Check — Quick check: 11 × (10 + 11 + … + 90)*: `11 × 4050 = 44550`
