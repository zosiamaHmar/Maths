# Question 18 — Prove S₃ = 3(S₂ − S₁)

##  The sums of n, 2n and 3n terms of an AP are S₁, S₂ and S₃. Prove that S₃ = 3(S₂ − S₁).

- **Write each sum with the formula Sₙ equals n over 2 times the bracket**
  - `Sₙ = {n|2} [2a + (n − 1)d]`
- **S one is the sum of n terms**
  - `S₁ = {n|2} [2a + (n − 1)d]`
- **S two is the sum of 2n terms. Replace n by 2n**
  - `S₂ = {2n|2} [2a + (2n − 1)d]`
  - `= n [2a + (2n − 1)d]`
- **S three is the sum of 3n terms. Replace n by 3n**
  - `S₃ = {3n|2} [2a + (3n − 1)d]`
- **Now work out S two minus S one. Take n over 2 out as a common factor**
  - `S₂ − S₁ = {n|2} [2(2a + (2n − 1)d) − (2a + (n − 1)d)]`
- **Open the brackets inside**
  - `= {n|2} [4a + (4n − 2)d − 2a − (n − 1)d]`
- **Combine the a terms and the d terms**
  - `= {n|2} [2a + (4n − 2 − n + 1)d]`
  - `= {n|2} [2a + (3n − 1)d]`
- **Multiply by 3**
  - `3 (S₂ − S₁) = {3n|2} [2a + (3n − 1)d]`
- **This is exactly S three**
  - `3 (S₂ − S₁) = S₃`

**Answer:** `S₃ = 3(S₂ − S₁)   — proved ✓`

- *Check — Quick check with a = 1, d = 1, n = 1: S₁ = 1, S₂ = 3, S₃ = 6*: `3 (3 − 1) = 6 = S₃ ✓`
