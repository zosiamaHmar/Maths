# Question 19 — Prove the sum of (m + n) terms is 0

##  If the sum of m terms of an AP is the same as the sum of its n terms, show that the sum of its (m + n) terms is zero.

- **Write down what is given: the two sums are equal**
  - `Sₘ = Sₙ`
- **Use the sum formula on both sides**
  - `{m|2} [2a + (m − 1)d] = {n|2} [2a + (n − 1)d]`
- **Multiply both sides by 2**
  - `m [2a + (m − 1)d] = n [2a + (n − 1)d]`
- **Open the brackets**
  - `2am + m(m − 1)d = 2an + n(n − 1)d`
  - `2am + (m² − m)d = 2an + (n² − n)d`
- **Collect everything on the left side**
  - `2am − 2an + (m² − m − n² + n)d = 0`
- **Factor: 2a times (m − n), and m² − n² is (m − n)(m + n)**
  - `2a (m − n) + [(m² − n²) − (m − n)] d = 0`
  - `2a (m − n) + [(m − n)(m + n) − (m − n)] d = 0`
- **Take (m − n) out as a common factor**
  - `(m − n) [2a + (m + n − 1) d] = 0`
- **m and n are different, so m − n is not zero. So the other factor must be zero**
  - `2a + (m + n − 1) d = 0      ...  (★)`
- **Now write the sum of (m + n) terms**
  - `Sₘ₊ₙ = {m + n|2} [2a + (m + n − 1) d]`
- **The bracket is zero by (★)**
  - `= {m + n|2} × 0`
  - `= 0`

**Answer:** `Sₘ₊ₙ = 0   — shown ✓`

- *Check — Quick check with the AP 3, 2, 1, 0, −1, −2, …: S₂ = 5 and S₃ = 6 are not equal, but S₃ = S₄ = 6 is*: `Here m = 3, n = 4, and S₇ = 3 + 2 + 1 + 0 − 1 − 2 − 3 = 0 ✓`
