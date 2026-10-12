# Question 21 — Sum of n terms from two sums

##  If the sum of the first 7 terms of an AP is 49 and that of 17 terms is 289, find the sum of the first n terms.

- **Use the sum formula for 7 terms**
  - `S₇ = {7|2} [2a + 6d] = 49`
  - `7 (a + 3d) = 49`
- **Divide by 7**
  - `a + 3d = 7      ...  (1)`
- **Use the sum formula for 17 terms**
  - `S₁₇ = {17|2} [2a + 16d] = 289`
  - `17 (a + 8d) = 289`
- **Divide by 17**
  - `a + 8d = 17      ...  (2)`
- **Subtract equation (1) from equation (2)**
  - `(a + 8d) − (a + 3d) = 17 − 7`
  - `5d = 10`
  - `d = 2`
- **Put d = 2 into equation (1)**
  - `a + 3(2) = 7`
  - `a + 6 = 7`
  - `a = 1`
- **Now the sum of n terms**
  - `Sₙ = {n|2} [2a + (n − 1)d]`
  - `= {n|2} [2(1) + (n − 1)(2)]`
- **Simplify inside the bracket**
  - `= {n|2} [2 + 2n − 2]`
  - `= {n|2} × 2n`
- **The 2s cancel**
  - `= n²`

**Answer:** `Sₙ = n²`

- *Check — Quick check: the AP is 1, 3, 5, 7, …*: `S₇ = 49 = 7² ✓,   S₁₇ = 289 = 17² ✓`
