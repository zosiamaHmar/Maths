# Question 13 — A sum with n terms

##  Find the sum  (1 − 1/n) + (1 − 2/n) + (1 − 3/n) + … up to n terms.

- **Find the first term**
  - `a = 1 − {1|n} = {n − 1|n}`
- **Find the common difference: second term minus first**
  - `d = (1 − {2|n}) − (1 − {1|n})`
  - `= 1 − {2|n} − 1 + {1|n}`
  - `= −{1|n}`
- **Find the last term, the nth term, by putting n in the pattern**
  - `l = 1 − {n|n} = 1 − 1 = 0`
- **Use the second sum formula**
  - `Sₙ = {n|2} (a + l)`
  - `= {n|2} ({n − 1|n} + 0)`
- **The n on the top cancels the n on the bottom**
  - `= {n − 1|2}`

**Answer:** `Sₙ = {n − 1|2}`

- *Check — Quick check with n = 4: the terms are 3/4, 1/2, 1/4, 0*: `Sum = {3|4} + {2|4} + {1|4} + 0 = {6|4} = {3|2} = {4 − 1|2} ✓`
