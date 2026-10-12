# Question 3 — Finding a, d, n and the sum

## (i) In an AP, given a = 7 and a₁₃ = 35, find d and S₁₃.

- **Use the nth term formula for the 13th term**
  - `a₁₃ = a + (13 − 1)d`
  - `35 = 7 + 12d`
- **Subtract 7 from both sides**
  - `35 − 7 = 12d`
  - `28 = 12d`
- **Divide both sides by 12 and simplify**
  - `d = {28|12} = {7|3}`
- **Now the sum of 13 terms. Use the first and last term**
  - `Sₙ = {n|2} (a + l)`
  - `S₁₃ = {13|2} (7 + 35)`
- **Add inside the bracket, then multiply**
  - `= {13|2} × 42`
  - `= 13 × 21`
  - `= 273`

**Answer:** `d = {7|3},   S₁₃ = 273`

- *Check — Quick check with the other formula*: `S₁₃ = {13|2} [14 + 12 × {7|3}] = {13|2} [14 + 28] = {13|2} × 42 = 273`

## (ii) In an AP, given a = 3, n = 8 and S = 192, find d.

- **Write the sum formula with the numbers we know**
  - `Sₙ = {n|2} [2a + (n − 1)d]`
  - `192 = {8|2} [2(3) + (8 − 1)d]`
- **Simplify 8 over 2 and the 2 times 3**
  - `192 = 4 [6 + 7d]`
- **Divide both sides by 4**
  - `{192|4} = 6 + 7d`
  - `48 = 6 + 7d`
- **Subtract 6 from both sides**
  - `48 − 6 = 7d`
  - `42 = 7d`
- **Divide both sides by 7**
  - `d = {42|7} = 6`

**Answer:** `d = 6`

- *Check — Quick check: the terms are 3, 9, 15, 21, 27, 33, 39, 45*: `3 + 9 + 15 + 21 + 27 + 33 + 39 + 45 = 192`

## (iii) In an AP, given aₙ = 4, d = 2 and Sₙ = −14, find n and a.

- **Write the nth term formula with aₙ = 4 and d = 2**
  - `aₙ = a + (n − 1)d`
  - `4 = a + (n − 1)(2)`
  - `4 = a + 2n − 2`
- **Move the numbers so that a is alone**
  - `a = 4 + 2 − 2n`
  - `a = 6 − 2n      ...  (1)`
- **Now use the second sum formula with l = 4 and Sₙ = −14**
  - `Sₙ = {n|2} (a + l)`
  - `−14 = {n|2} (a + 4)`
- **Multiply both sides by 2**
  - `−28 = n (a + 4)      ...  (2)`
- **Put a = 6 − 2n from (1) into (2)**
  - `−28 = n (6 − 2n + 4)`
  - `−28 = n (10 − 2n)`
  - `−28 = 10n − 2n²`
- **Bring everything to one side to get a quadratic**
  - `2n² − 10n − 28 = 0`
- **Divide every term by 2**
  - `n² − 5n − 14 = 0`
- **Factorise. We need two numbers that multiply to −14 and add to −5. They are −7 and +2**
  - `(n − 7)(n + 2) = 0`
  - `n = 7   or   n = −2`
- **The number of terms cannot be negative, so we reject n = −2**
  - `n = 7`
- **Find a from equation (1)**
  - `a = 6 − 2(7) = 6 − 14`
  - `a = −8`

**Answer:** `n = 7,   a = −8`

- *Check — Quick check: the terms are −8, −6, −4, −2, 0, 2, 4*: `Sum = {7|2} (−8 + 4) = {7|2} × (−4) = −14`

## (iv) In an AP, given a = 2, d = 8 and Sₙ = 90, find n and aₙ.

- **Put a = 2 and d = 8 into the sum formula**
  - `Sₙ = {n|2} [2a + (n − 1)d]`
  - `90 = {n|2} [2(2) + (n − 1)(8)]`
- **Multiply out the bracket**
  - `90 = {n|2} [4 + 8n − 8]`
  - `90 = {n|2} (8n − 4)`
- **Cancel the 2 into the bracket**
  - `90 = n (4n − 2)`
  - `90 = 4n² − 2n`
- **Bring everything to one side**
  - `4n² − 2n − 90 = 0`
- **Divide every term by 2**
  - `2n² − n − 45 = 0`
- **Split the middle term. We need two numbers that multiply to 2 × (−45) = −90 and add to −1. They are −10 and +9**
  - `2n² − 10n + 9n − 45 = 0`
  - `2n (n − 5) + 9 (n − 5) = 0`
  - `(n − 5)(2n + 9) = 0`
- **Set each bracket to zero**
  - `n = 5   or   n = −{9|2}`
- **Terms cannot be negative or a fraction, so we reject the second answer**
  - `n = 5`
- **Now find the 5th term**
  - `aₙ = a + (n − 1)d`
  - `a₅ = 2 + (5 − 1)(8) = 2 + 32`
  - `a₅ = 34`

**Answer:** `n = 5,   a₅ = 34`

- *Check — Quick check: the terms are 2, 10, 18, 26, 34*: `2 + 10 + 18 + 26 + 34 = 90`

## (v) In an AP, given a₁₂ = 37 and d = 3, find a and S₁₂.

- **Use the nth term formula for the 12th term**
  - `a₁₂ = a + (12 − 1)d`
  - `37 = a + 11(3)`
  - `37 = a + 33`
- **Subtract 33 from both sides**
  - `a = 37 − 33 = 4`
- **Now use the second sum formula, with first term 4 and last term 37**
  - `S₁₂ = {12|2} (4 + 37)`
  - `= 6 × 41`
  - `= 246`

**Answer:** `a = 4,   S₁₂ = 246`

- *Check — Quick check with the other formula*: `S₁₂ = 6 [8 + 11 × 3] = 6 × 41 = 246`
