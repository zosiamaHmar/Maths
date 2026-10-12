# Question 11 — nth term from the sum

## (i) The sum of the first n terms of an AP is Sₙ = 2n² + 5n. Find the nth term.

- **We use: aₙ = Sₙ − Sₙ₋₁**
  - `aₙ = Sₙ − Sₙ₋₁`
- **Write Sₙ₋₁ by replacing n with n − 1**
  - `Sₙ₋₁ = 2(n − 1)² + 5(n − 1)`
- **Expand (n − 1) squared as n² − 2n + 1**
  - `= 2(n² − 2n + 1) + 5n − 5`
  - `= 2n² − 4n + 2 + 5n − 5`
  - `= 2n² + n − 3`
- **Subtract Sₙ₋₁ from Sₙ. Be careful with the minus signs**
  - `aₙ = (2n² + 5n) − (2n² + n − 3)`
  - `= 2n² + 5n − 2n² − n + 3`
- **2n² cancels. Combine the n terms**
  - `aₙ = 4n + 3`

**Answer:** `aₙ = 4n + 3`

- *Check — Quick check: the first term a₁ should equal S₁*: `a₁ = 4(1) + 3 = 7,   S₁ = 2 + 5 = 7`

## (ii) If the nth term of an AP is 2n + 1, find the sum of the first n terms.

- **Find the first term: put n = 1**
  - `a = a₁ = 2(1) + 1 = 3`
- **The last term is the nth term**
  - `l = 2n + 1`
- **Use the second sum formula**
  - `Sₙ = {n|2} (a + l)`
  - `= {n|2} (3 + 2n + 1)`
- **Add inside the bracket**
  - `= {n|2} (2n + 4)`
- **Cancel the 2, then multiply out**
  - `= n (n + 2)`
  - `= n² + 2n`

**Answer:** `Sₙ = n² + 2n`

- *Check — Quick check with n = 3: the terms are 3, 5, 7*: `S₃ = 9 + 6 = 15 = 3 + 5 + 7`
