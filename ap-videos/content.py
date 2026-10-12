"""Content for the 25 AP-sum videos: every step, every operation, with narration.

Math-line mini syntax (rendered by scene.py, spoken by speak()):
  {a|b}   stacked fraction a over b
  !text   highlighted line (gold)
Each step is (say, [math lines]); `say` is shown as the caption and spoken first,
then each math line is written on the board and read aloud.
"""
from fractions import Fraction as F
from decimal import Decimal

SUBS = str.maketrans("0123456789nm+-", "₀₁₂₃₄₅₆₇₈₉ₙₘ₊₋")


def sub(x):
    return str(x).translate(SUBS)


def num(x, frac=False):
    """Format int/Fraction with a real minus sign; decimals unless frac=True."""
    x = F(x)
    neg = x < 0
    x = abs(x)
    if x.denominator == 1:
        s = str(x.numerator)
    elif frac:
        s = "{%d|%d}" % (x.numerator, x.denominator)
    else:
        d = x.denominator
        for p in (2, 5):
            while d % p == 0:
                d //= p
        if d == 1:
            s = format(Decimal(x.numerator) / Decimal(x.denominator), "f").rstrip("0").rstrip(".")
        else:
            s = "{%d|%d}" % (x.numerator, x.denominator)
    return ("−" if neg else "") + s


def par(x, frac=False):
    s = num(x, frac)
    return "(" + s + ")" if s.startswith("−") else s


def half(n):
    return str(n // 2) if n % 2 == 0 else "{%d|2}" % n


# ---------------------------------------------------------------- formulas
K = {
    "an": ("aₙ = a + (n − 1)d", "The n th term is a plus n minus 1 times d"),
    "s1": ("Sₙ = {n|2} [2a + (n − 1)d]", "Sum of n terms, when we know a and d"),
    "s2": ("Sₙ = {n|2} (a + l)", "Sum of n terms, when we know the last term l"),
    "d": ("d = a₂ − a₁", "Common difference is any term minus the one before it"),
    "diff": ("aₙ = Sₙ − Sₙ₋₁", "The n th term is the sum of n terms minus the sum of n minus 1 terms"),
}


# ---------------------------------------------------------------- helpers
def sum_steps(a, d, n, frac=False, extra_say=""):
    """Sₙ = n/2 [2a + (n−1)d] with every operation shown."""
    a, d = F(a), F(d)
    inside1 = 2 * a
    inside2 = (n - 1) * d
    tot = inside1 + inside2
    res = F(n, 2) * tot
    h = half(n)
    S = "S" + sub(n)
    nf = lambda x: num(x, frac)
    pf = lambda x: par(x, frac)
    return [
        ("Write down what we know", [f"a = {nf(a)},   d = {nf(d)},   n = {n}"]),
        ("Use the sum formula", ["Sₙ = {n|2} [2a + (n − 1)d]"]),
        ("Put the numbers in", [f"{S} = {{{n}|2}} [2({nf(a)}) + ({n} − 1)({nf(d)})]"]),
        ("First do the brackets and the multiplications inside",
         [f"= {h} [{nf(inside1)} + ({n - 1})({nf(d)})]",
          f"= {h} [{nf(inside1)} + ({nf(inside2)})]"]),
        ("Now add inside the big bracket", [f"= {h} × {pf(tot)}"]),
        ("Finally multiply", [f"!= {nf(res)}"]),
    ], res


def n_from_last(a, d, l, frac=False):
    a, d, l = F(a), F(d), F(l)
    nf = lambda x: num(x, frac)
    n = (l - a) / d + 1
    return [
        ("To find how many terms, use the nth term formula", ["aₙ = a + (n − 1)d"]),
        ("The last term is the nth term, so put it in",
         [f"{nf(l)} = {nf(a)} + (n − 1)({nf(d)})"]),
        ("Move a to the other side by subtracting", [f"{nf(l)} − {par(a, frac)} = (n − 1)({nf(d)})",
                                                     f"{nf(l - a)} = (n − 1)({nf(d)})"]),
        ("Divide both sides by d", [f"n − 1 = {{{nf(l - a)}|{nf(d)}}} = {nf((l - a) / d)}"]),
        ("Add 1 to both sides", [f"!n = {nf((l - a) / d)} + 1 = {int(n)}"]),
    ], int(n)


def sum_ends(a, l, n, frac=False):
    a, l = F(a), F(l)
    nf = lambda x: num(x, frac)
    res = F(n, 2) * (a + l)
    h = half(n)
    return [
        ("Now we know the first and last term, so use the second sum formula", ["Sₙ = {n|2} (a + l)"]),
        ("Put the numbers in", [f"S{sub(n)} = {{{n}|2}} ({nf(a)} + {par(l, frac)})"]),
        ("Add the two terms", [f"= {h} × {par(a + l, frac)}"]),
        ("Multiply", [f"!= {nf(res)}"]),
    ], res


def quad_solve(a, b, c, name="n"):
    """Return roots of ax²+bx+c as ints (assumes integer roots)."""
    disc = b * b - 4 * a * c
    r = int(round(disc ** 0.5))
    assert r * r == disc, disc
    return F(-b + r, 2 * a), F(-b - r, 2 * a)


PROBLEMS = []


def problem(q, title, know, hook, parts):
    PROBLEMS.append(dict(q=q, title=title, know=know, hook=hook, parts=parts))


def part(label, stmt, steps, ans, check=None, short=None):
    return dict(label=label, stmt=stmt, steps=steps, ans=ans, check=check or [], short=short or stmt)


# ======================================================================= Q1
def q1():
    ps = []
    # (i)
    st, r = sum_steps(8, -5, 22)
    assert r == -979
    st = [("Find the common difference: second term minus first term", ["d = 3 − 8 = −5"])] + st
    ps.append(part("(i)", "Find the sum of the AP 8, 3, −2, … to 22 terms.", st, "S₂₂ = −979",
                   [("Quick check: the terms are going down by 5 each time, so the sum is negative",
                     ["a₂₂ = 8 + 21(−5) = −97", "S₂₂ = 11 × (8 − 97) = 11 × (−89) = −979"])]))
    # (ii)
    st, r = sum_steps(2, 5, 10)
    assert r == 245
    st = [("Find the common difference", ["d = 7 − 2 = 5"])] + st
    ps.append(part("(ii)", "Find the sum of the AP 2, 7, 12, … to 10 terms.", st, "S₁₀ = 245",
                   [("Quick check with the last term", ["a₁₀ = 2 + 9(5) = 47", "S₁₀ = 5 × (2 + 47) = 5 × 49 = 245"])]))
    # (iii)
    st, r = sum_steps(-37, 4, 12)
    assert r == -180
    st = [("Find the common difference", ["d = −33 − (−37) = −33 + 37 = 4"])] + st
    ps.append(part("(iii)", "Find the sum of the AP −37, −33, −29, … to 12 terms.", st, "S₁₂ = −180",
                   [("Quick check with the last term", ["a₁₂ = −37 + 11(4) = 7", "S₁₂ = 6 × (−37 + 7) = 6 × (−30) = −180"])]))
    # (iv) fractions
    st = [
        ("Find the common difference. We need a common denominator, the LCM of 12 and 15, which is 60",
         ["d = {1|12} − {1|15}", "= {5|60} − {4|60} = {1|60}"]),
        ("Write down what we know", ["a = {1|15},   d = {1|60},   n = 11"]),
        ("Use the sum formula", ["Sₙ = {n|2} [2a + (n − 1)d]"]),
        ("Put the numbers in", ["S₁₁ = {11|2} [2({1|15}) + (11 − 1)({1|60})]"]),
        ("Multiply inside the bracket", ["= {11|2} [{2|15} + 10 × {1|60}]", "= {11|2} [{2|15} + {10|60}]", "= {11|2} [{2|15} + {1|6}]"]),
        ("Add the fractions. The LCM of 15 and 6 is 30", ["= {11|2} [{4|30} + {5|30}]", "= {11|2} × {9|30}", "= {11|2} × {3|10}"]),
        ("Multiply the tops together and the bottoms together", ["!= {33|20}"]),
    ]
    ps.append(part("(iv)", "Find the sum of the AP 1/15, 1/12, 1/10, … to 11 terms.", st, "S₁₁ = {33|20}  (= 1.65)",
                   [("Quick check as a decimal", ["33 ÷ 20 = 1.65"])]))
    # (v) decimals
    st, r = sum_steps(F(3, 5), F(11, 10), 100)
    assert r == 5505
    st = [("Find the common difference", ["d = 1.7 − 0.6 = 1.1"])] + st
    ps.append(part("(v)", "Find the sum of the AP 0.6, 1.7, 2.8, … to 100 terms.", st, "S₁₀₀ = 5505",
                   [("Quick check with the last term", ["a₁₀₀ = 0.6 + 99(1.1) = 109.5", "S₁₀₀ = 50 × (0.6 + 109.5) = 50 × 110.1 = 5505"])]))
    problem(1, "Sum of an AP", ["d", "s1"], [8, 3, -2, -7, -12, -17], ps)


q1()


# ======================================================================= Q2
def q2():
    ps = []
    # (i)
    s1, n = n_from_last(-5, -3, -230)
    assert n == 76
    s2, r = sum_ends(-5, -230, 76)
    assert r == -8930
    st = [("First find the common difference", ["d = −8 − (−5) = −8 + 5 = −3"]),
          ("Write down what we know", ["a = −5,   d = −3,   l = −230"])] + s1 + s2
    ps.append(part("(i)", "Find the sum  −5 + (−8) + (−11) + … + (−230).", st, "Sum = −8930",
                   [("Quick check using the other formula", ["S₇₆ = 38 × (−5 − 230) = 38 × (−235) = −8930"])]))
    # (ii)
    st = [("The second term 10½ is the same as 10.5. First find the common difference", ["d = 10.5 − 7 = 3.5"]),
          ("Write down what we know", ["a = 7,   d = 3.5,   l = 84"]),
          ("To find how many terms, use the nth term formula", ["aₙ = a + (n − 1)d"]),
          ("The last term is the nth term, so put it in", ["84 = 7 + (n − 1)(3.5)"]),
          ("Subtract 7 from 84", ["84 − 7 = 3.5 (n − 1)", "77 = 3.5 (n − 1)"]),
          ("Divide both sides by 3.5", ["n − 1 = {77|3.5} = 22"]),
          ("Add 1 to both sides", ["!n = 23"]),
          ("Now use the second sum formula", ["Sₙ = {n|2} (a + l)"]),
          ("Put the numbers in", ["S₂₃ = {23|2} (7 + 84)"]),
          ("Add the two terms", ["= {23|2} × 91"]),
          ("Multiply 23 by 91, then halve it", ["= {2093|2}", "!= 1046.5"])]
    ps.append(part("(ii)", "Find the sum  7 + 10½ + 14 + … + 84.", st, "Sum = 1046.5  (= {2093|2})",
                   [("Quick check: 23 × 91", ["23 × 91 = 23 × 90 + 23 = 2070 + 23 = 2093", "2093 ÷ 2 = 1046.5"])]))
    # (iii)
    s1, n = n_from_last(25, 3, 100)
    assert n == 26
    s2, r = sum_ends(25, 100, 26)
    assert r == 1625
    st = [("Find the common difference", ["d = 28 − 25 = 3"]),
          ("Write down what we know", ["a = 25,   d = 3,   l = 100"])] + s1 + s2
    ps.append(part("(iii)", "Find the sum  25 + 28 + 31 + … + 100.", st, "Sum = 1625",
                   [("Quick check", ["13 × 125 = 13 × 100 + 13 × 25 = 1300 + 325 = 1625"])]))
    problem(2, "Sum when the last term is known", ["d", "an", "s2"], [-5, -8, -11, -14, -17, -20], ps)


q2()


# ======================================================================= Q3
def q3():
    ps = []
    # (i)
    st = [
        ("Use the nth term formula for the 13th term", ["a₁₃ = a + (13 − 1)d", "35 = 7 + 12d"]),
        ("Subtract 7 from both sides", ["35 − 7 = 12d", "28 = 12d"]),
        ("Divide both sides by 12 and simplify", ["d = {28|12} = {7|3}"]),
        ("Now the sum of 13 terms. Use the first and last term", ["Sₙ = {n|2} (a + l)", "S₁₃ = {13|2} (7 + 35)"]),
        ("Add inside the bracket, then multiply", ["= {13|2} × 42", "= 13 × 21", "!= 273"]),
    ]
    ps.append(part("(i)", "In an AP, given a = 7 and a₁₃ = 35, find d and S₁₃.", st, "d = {7|3},   S₁₃ = 273",
                   [("Quick check with the other formula", ["S₁₃ = {13|2} [14 + 12 × {7|3}] = {13|2} [14 + 28] = {13|2} × 42 = 273"])]))
    # (ii)
    st = [
        ("Write the sum formula with the numbers we know", ["Sₙ = {n|2} [2a + (n − 1)d]", "192 = {8|2} [2(3) + (8 − 1)d]"]),
        ("Simplify 8 over 2 and the 2 times 3", ["192 = 4 [6 + 7d]"]),
        ("Divide both sides by 4", ["{192|4} = 6 + 7d", "48 = 6 + 7d"]),
        ("Subtract 6 from both sides", ["48 − 6 = 7d", "42 = 7d"]),
        ("Divide both sides by 7", ["!d = {42|7} = 6"]),
    ]
    ps.append(part("(ii)", "In an AP, given a = 3, n = 8 and S = 192, find d.", st, "d = 6",
                   [("Quick check: the terms are 3, 9, 15, 21, 27, 33, 39, 45", ["3 + 9 + 15 + 21 + 27 + 33 + 39 + 45 = 192"])]))
    # (iii)
    st = [
        ("Write the nth term formula with aₙ = 4 and d = 2", ["aₙ = a + (n − 1)d", "4 = a + (n − 1)(2)", "4 = a + 2n − 2"]),
        ("Move the numbers so that a is alone", ["a = 4 + 2 − 2n", "a = 6 − 2n      ...  (1)"]),
        ("Now use the second sum formula with l = 4 and Sₙ = −14", ["Sₙ = {n|2} (a + l)", "−14 = {n|2} (a + 4)"]),
        ("Multiply both sides by 2", ["−28 = n (a + 4)      ...  (2)"]),
        ("Put a = 6 − 2n from (1) into (2)", ["−28 = n (6 − 2n + 4)", "−28 = n (10 − 2n)", "−28 = 10n − 2n²"]),
        ("Bring everything to one side to get a quadratic", ["2n² − 10n − 28 = 0"]),
        ("Divide every term by 2", ["n² − 5n − 14 = 0"]),
        ("Factorise. We need two numbers that multiply to −14 and add to −5. They are −7 and +2",
         ["(n − 7)(n + 2) = 0", "n = 7   or   n = −2"]),
        ("The number of terms cannot be negative, so we reject n = −2", ["!n = 7"]),
        ("Find a from equation (1)", ["a = 6 − 2(7) = 6 − 14", "!a = −8"]),
    ]
    ps.append(part("(iii)", "In an AP, given aₙ = 4, d = 2 and Sₙ = −14, find n and a.", st, "n = 7,   a = −8",
                   [("Quick check: the terms are −8, −6, −4, −2, 0, 2, 4", ["Sum = {7|2} (−8 + 4) = {7|2} × (−4) = −14"])]))
    # (iv)
    st = [
        ("Put a = 2 and d = 8 into the sum formula", ["Sₙ = {n|2} [2a + (n − 1)d]", "90 = {n|2} [2(2) + (n − 1)(8)]"]),
        ("Multiply out the bracket", ["90 = {n|2} [4 + 8n − 8]", "90 = {n|2} (8n − 4)"]),
        ("Cancel the 2 into the bracket", ["90 = n (4n − 2)", "90 = 4n² − 2n"]),
        ("Bring everything to one side", ["4n² − 2n − 90 = 0"]),
        ("Divide every term by 2", ["2n² − n − 45 = 0"]),
        ("Split the middle term. We need two numbers that multiply to 2 × (−45) = −90 and add to −1. They are −10 and +9",
         ["2n² − 10n + 9n − 45 = 0", "2n (n − 5) + 9 (n − 5) = 0", "(n − 5)(2n + 9) = 0"]),
        ("Set each bracket to zero", ["n = 5   or   n = −{9|2}"]),
        ("Terms cannot be negative or a fraction, so we reject the second answer", ["!n = 5"]),
        ("Now find the 5th term", ["aₙ = a + (n − 1)d", "a₅ = 2 + (5 − 1)(8) = 2 + 32", "!a₅ = 34"]),
    ]
    ps.append(part("(iv)", "In an AP, given a = 2, d = 8 and Sₙ = 90, find n and aₙ.", st, "n = 5,   a₅ = 34",
                   [("Quick check: the terms are 2, 10, 18, 26, 34", ["2 + 10 + 18 + 26 + 34 = 90"])]))
    # (v)
    st = [
        ("Use the nth term formula for the 12th term", ["a₁₂ = a + (12 − 1)d", "37 = a + 11(3)", "37 = a + 33"]),
        ("Subtract 33 from both sides", ["!a = 37 − 33 = 4"]),
        ("Now use the second sum formula, with first term 4 and last term 37", ["S₁₂ = {12|2} (4 + 37)", "= 6 × 41", "!= 246"]),
    ]
    ps.append(part("(v)", "In an AP, given a₁₂ = 37 and d = 3, find a and S₁₂.", st, "a = 4,   S₁₂ = 246",
                   [("Quick check with the other formula", ["S₁₂ = 6 [8 + 11 × 3] = 6 × 41 = 246"])]))
    problem(3, "Finding a, d, n and the sum", ["an", "s1", "s2"], [7, 14, 21, 28, 35], ps)


q3()


# ======================================================================= Q4
def q4():
    ps = []
    st = [
        ("Write down what we know", ["a = 3,   d = 5 − 3 = 2,   Sₙ = 120"]),
        ("Use the sum formula", ["Sₙ = {n|2} [2a + (n − 1)d]", "120 = {n|2} [2(3) + (n − 1)(2)]"]),
        ("Simplify inside the bracket", ["120 = {n|2} [6 + 2n − 2]", "120 = {n|2} (2n + 4)"]),
        ("Cancel the 2", ["120 = n (n + 2)", "120 = n² + 2n"]),
        ("Make one side zero", ["n² + 2n − 120 = 0"]),
        ("Factorise. Two numbers that multiply to −120 and add to +2 are +12 and −10", ["n² + 12n − 10n − 120 = 0", "n (n + 12) − 10 (n + 12) = 0", "(n + 12)(n − 10) = 0"]),
        ("Set each bracket to zero", ["n = −12   or   n = 10"]),
        ("A number of terms cannot be negative, so reject −12", ["!n = 10"]),
    ]
    ps.append(part("(i)", "How many terms of the AP 3, 5, 7, 9, … must be added to get the sum 120?", st, "10 terms",
                   [("Quick check", ["a₁₀ = 3 + 9(2) = 21", "S₁₀ = 5 × (3 + 21) = 5 × 24 = 120"])]))
    st = [
        ("Write down what we know", ["a = 63,   d = 60 − 63 = −3,   Sₙ = 693"]),
        ("Use the sum formula", ["693 = {n|2} [2(63) + (n − 1)(−3)]"]),
        ("Simplify inside the bracket", ["693 = {n|2} [126 − 3n + 3]", "693 = {n|2} (129 − 3n)"]),
        ("Multiply both sides by 2", ["1386 = n (129 − 3n)", "1386 = 129n − 3n²"]),
        ("Make one side zero", ["3n² − 129n + 1386 = 0"]),
        ("Divide every term by 3", ["n² − 43n + 462 = 0"]),
        ("Factorise. Two numbers that multiply to 462 and add to −43 are −21 and −22", ["n² − 21n − 22n + 462 = 0", "n (n − 21) − 22 (n − 21) = 0", "(n − 21)(n − 22) = 0"]),
        ("Both answers are positive whole numbers, so both are valid", ["!n = 21   or   n = 22"]),
        ("Why two answers? Find the 22nd term", ["a₂₂ = 63 + 21(−3) = 63 − 63", "!a₂₂ = 0"]),
        ("The 22nd term is zero, and adding zero changes nothing. So the sum of 21 terms and the sum of 22 terms are the same",
         ["S₂₁ = S₂₂ + 0 = 693"]),
    ]
    ps.append(part("(ii)", "How many terms of the AP 63, 60, 57, … must be added so that their sum is 693? Explain the double answer.",
                   st, "n = 21 or n = 22",
                   [("Quick check of 21 terms", ["a₂₁ = 63 + 20(−3) = 3", "S₂₁ = {21|2} (63 + 3) = {21|2} × 66 = 693"])]))
    st = [
        ("Write down what we know", ["a = 54,   d = 51 − 54 = −3,   Sₙ = 513"]),
        ("Use the sum formula", ["513 = {n|2} [2(54) + (n − 1)(−3)]"]),
        ("Simplify inside the bracket", ["513 = {n|2} [108 − 3n + 3]", "513 = {n|2} (111 − 3n)"]),
        ("Multiply both sides by 2", ["1026 = n (111 − 3n)", "1026 = 111n − 3n²"]),
        ("Make one side zero", ["3n² − 111n + 1026 = 0"]),
        ("Divide every term by 3", ["n² − 37n + 342 = 0"]),
        ("Factorise. Two numbers that multiply to 342 and add to −37 are −18 and −19", ["n² − 18n − 19n + 342 = 0", "n (n − 18) − 19 (n − 18) = 0", "(n − 18)(n − 19) = 0"]),
        ("Both are valid whole numbers", ["!n = 18   or   n = 19"]),
        ("Why two answers? Find the 19th term", ["a₁₉ = 54 + 18(−3) = 54 − 54", "!a₁₉ = 0"]),
        ("The 19th term is zero, so adding it does not change the sum. 18 terms and 19 terms give the same total",
         ["S₁₈ = S₁₉ = 513"]),
    ]
    ps.append(part("(iii)", "How many terms of the series 54, 51, 48, … be taken so that their sum is 513? Explain the double answer.",
                   st, "n = 18 or n = 19",
                   [("Quick check of 18 terms", ["a₁₈ = 54 + 17(−3) = 3", "S₁₈ = 9 × (54 + 3) = 9 × 57 = 513"])]))
    problem(4, "How many terms?", ["s1", "an"], [3, 5, 7, 9, 11, 13], ps)


q4()


# ======================================================================= Q5
def q5():
    ps = []
    st = [
        ("Put n = 1 to get the first term", ["a₁ = 7 − 3(1) = 7 − 3 = 4"]),
        ("Put n = 2 to get the second term", ["a₂ = 7 − 3(2) = 7 − 6 = 1"]),
        ("The common difference is second minus first", ["d = 1 − 4 = −3"]),
        ("Put n = 25 to get the 25th term", ["a₂₅ = 7 − 3(25) = 7 − 75 = −68"]),
        ("Use the second sum formula", ["Sₙ = {n|2} (a + l)", "S₂₅ = {25|2} (4 + (−68))"]),
        ("Add inside the bracket, then multiply", ["= {25|2} × (−64)", "= 25 × (−32)", "!= −800"]),
    ]
    ps.append(part("(i)", "Find the sum of the first 25 terms of an AP whose nth term is aₙ = 7 − 3n.", st, "S₂₅ = −800",
                   [("Quick check with the other formula", ["S₂₅ = {25|2} [8 + 24(−3)] = {25|2} × (−64) = −800"])]))
    st = [
        ("Put n = 1 to get the first term", ["a₁ = 2 − 3(1) = −1"]),
        ("Put n = 2 to get the second term", ["a₂ = 2 − 3(2) = −4"]),
        ("The common difference", ["d = −4 − (−1) = −3"]),
        ("Put n = 20 to get the 20th term", ["a₂₀ = 2 − 3(20) = 2 − 60 = −58"]),
        ("Use the second sum formula", ["S₂₀ = {20|2} (−1 + (−58))"]),
        ("Add inside the bracket, then multiply", ["= 10 × (−59)", "!= −590"]),
    ]
    ps.append(part("(ii)", "Find the sum of the first 20 terms of an AP whose nth term is aₙ = 2 − 3n.", st, "S₂₀ = −590",
                   [("Quick check with the other formula", ["S₂₀ = 10 [−2 + 19(−3)] = 10 × (−59) = −590"])]))
    problem(5, "Sum from the nth term", ["an", "s2", "s1"], [4, 1, -2, -5, -8, -11], ps)


q5()


# ======================================================================= Q6
def q6():
    ps = []
    st = [
        ("Write the 2nd and 4th terms using aₙ = a + (n − 1)d", ["a₂ = a + d = 8      ...  (1)", "a₄ = a + 3d = 14      ...  (2)"]),
        ("Subtract equation (1) from equation (2). The a cancels", ["(a + 3d) − (a + d) = 14 − 8", "2d = 6"]),
        ("Divide by 2", ["d = 3"]),
        ("Put d = 3 into equation (1)", ["a + 3 = 8", "a = 8 − 3 = 5"]),
        ("Now the sum of 21 terms", ["S₂₁ = {21|2} [2(5) + (21 − 1)(3)]"]),
        ("Work inside the bracket", ["= {21|2} [10 + 60]", "= {21|2} × 70"]),
        ("70 divided by 2 is 35, then multiply", ["= 21 × 35", "!= 735"]),
    ]
    ps.append(part("(i)", "Find the sum of the first 21 terms of the AP whose 2nd term is 8 and 4th term is 14.", st, "S₂₁ = 735",
                   [("Quick check: the 21st term is 5 + 20 × 3 = 65", ["S₂₁ = {21|2} (5 + 65) = {21|2} × 70 = 735"])]))
    st = [
        ("Write the 2nd and 4th terms", ["a + d = 2      ...  (1)", "a + 3d = 8      ...  (2)"]),
        ("Subtract equation (1) from equation (2)", ["2d = 6", "d = 3"]),
        ("Put d = 3 into equation (1)", ["a + 3 = 2", "a = 2 − 3 = −1"]),
        ("Now the sum of 51 terms", ["S₅₁ = {51|2} [2(−1) + (51 − 1)(3)]"]),
        ("Work inside the bracket", ["= {51|2} [−2 + 150]", "= {51|2} × 148"]),
        ("148 divided by 2 is 74, then multiply 51 by 74", ["= 51 × 74", "= 51 × 70 + 51 × 4", "= 3570 + 204", "!= 3774"]),
    ]
    ps.append(part("(ii)", "Find the sum of the first 51 terms of the AP whose 2nd term is 2 and 4th term is 8.", st, "S₅₁ = 3774",
                   [("Quick check: the 51st term is −1 + 50 × 3 = 149", ["S₅₁ = {51|2} (−1 + 149) = {51|2} × 148 = 3774"])]))
    st = [
        ("Write the 5th and 12th terms", ["a₅ = a + 4d = −4      ...  (1)", "a₁₂ = a + 11d = −18      ...  (2)"]),
        ("Subtract equation (1) from equation (2)", ["(a + 11d) − (a + 4d) = −18 − (−4)", "7d = −18 + 4", "7d = −14"]),
        ("Divide by 7", ["d = −2"]),
        ("Put d = −2 into equation (1)", ["a + 4(−2) = −4", "a − 8 = −4", "a = −4 + 8 = 4"]),
        ("Now the sum of 20 terms", ["S₂₀ = {20|2} [2(4) + (20 − 1)(−2)]"]),
        ("Work inside the bracket", ["= 10 [8 + 19(−2)]", "= 10 [8 − 38]", "= 10 × (−30)", "!= −300"]),
    ]
    ps.append(part("(iii)", "If the 5th and 12th terms of an AP are −4 and −18, find the sum of the first 20 terms.", st, "S₂₀ = −300",
                   [("Quick check: the 20th term is 4 + 19(−2) = −34", ["S₂₀ = 10 (4 − 34) = 10 × (−30) = −300"])]))
    problem(6, "Finding a and d from two terms", ["an", "s1"], [5, 8, 11, 14, 17, 20], ps)


q6()


# ======================================================================= Q7
def q7():
    ps = []
    # (i)
    st = [
        ("Natural numbers below 100 divisible by 6 are 6, 12, 18, and so on, up to 96", ["a = 6,   d = 6,   l = 96"]),
        ("Why 96? Because 6 × 16 = 96 and 6 × 17 = 102 is more than 100", ["96 = 6 × 16"]),
        ("Find the number of terms with the nth term formula", ["aₙ = a + (n − 1)d", "96 = 6 + (n − 1)(6)", "96 − 6 = 6(n − 1)", "90 = 6(n − 1)", "n − 1 = {90|6} = 15", "!n = 16"]),
        ("Use the second sum formula", ["S₁₆ = {16|2} (6 + 96)", "= 8 × 102", "!= 816"]),
    ]
    ps.append(part("(i)", "Find the sum of all natural numbers less than 100 which are divisible by 6.", st, "Sum = 816",
                   [("Quick check: 6 × (1 + 2 + … + 16)", ["6 × {16 × 17|2} = 6 × 136 = 816"])]))
    # (ii)
    st = [
        ("The smallest 3-digit multiple of 13: 13 × 7 = 91 has only two digits, 13 × 8 = 104 has three", ["a = 104"]),
        ("The biggest 3-digit multiple of 13: 13 × 76 = 988 and 13 × 77 = 1001 has four digits", ["l = 988,   d = 13"]),
        ("Find the number of terms", ["988 = 104 + (n − 1)(13)", "988 − 104 = 13(n − 1)", "884 = 13(n − 1)", "n − 1 = {884|13} = 68", "!n = 69"]),
        ("Use the second sum formula", ["S₆₉ = {69|2} (104 + 988)", "= {69|2} × 1092"]),
        ("1092 divided by 2 is 546, then multiply 69 by 546", ["= 69 × 546", "= 70 × 546 − 546", "= 38220 − 546", "!= 37674"]),
    ]
    ps.append(part("(ii)", "Find the sum of all 3-digit natural numbers which are divisible by 13.", st, "Sum = 37674",
                   [("Quick check: 13 × (8 + 9 + … + 76)", ["13 × 2898 = 37674"])]))
    # (iii)
    st = [
        ("Multiples of 9 just above 300: 9 × 33 = 297 is below 300, 9 × 34 = 306 is above", ["a = 306"]),
        ("Multiples of 9 just below 700: 9 × 77 = 693 is below 700, 9 × 78 = 702 is above", ["l = 693,   d = 9"]),
        ("Find the number of terms", ["693 = 306 + (n − 1)(9)", "693 − 306 = 9(n − 1)", "387 = 9(n − 1)", "n − 1 = {387|9} = 43", "!n = 44"]),
        ("Use the second sum formula", ["S₄₄ = {44|2} (306 + 693)", "= 22 × 999"]),
        ("22 times 999 is 22 times 1000 minus 22", ["= 22000 − 22", "!= 21978"]),
    ]
    ps.append(part("(iii)", "Find the sum of all multiples of 9 lying between 300 and 700.", st, "Sum = 21978",
                   [("Quick check: 9 × (34 + 35 + … + 77)", ["9 × 2442 = 21978"])]))
    # (iv)
    st = [
        ("Even numbers divisible by 5 are the multiples of 10", ["10, 20, 30, 40, …"]),
        ("So the first term is 10, the common difference is 10, and we need 100 terms", ["a = 10,   d = 10,   n = 100"]),
        ("Use the sum formula", ["S₁₀₀ = {100|2} [2(10) + (100 − 1)(10)]"]),
        ("Work inside the bracket", ["= 50 [20 + 990]", "= 50 × 1010"]),
        ("Multiply", ["!= 50500"]),
    ]
    ps.append(part("(iv)", "Find the sum of the first hundred even natural numbers which are divisible by 5.", st, "Sum = 50500",
                   [("Quick check: the 100th term is 1000", ["S₁₀₀ = 50 (10 + 1000) = 50 × 1010 = 50500"])]))
    # (v)
    st = [
        ("Smallest 3-digit multiple of 11: 11 × 9 = 99 has two digits, 11 × 10 = 110 has three", ["a = 110"]),
        ("Largest 3-digit multiple of 11: 11 × 90 = 990 and 11 × 91 = 1001 has four digits", ["l = 990,   d = 11"]),
        ("Find the number of terms", ["990 = 110 + (n − 1)(11)", "990 − 110 = 11(n − 1)", "880 = 11(n − 1)", "n − 1 = {880|11} = 80", "!n = 81"]),
        ("Use the second sum formula", ["S₈₁ = {81|2} (110 + 990)", "= {81|2} × 1100", "= 81 × 550"]),
        ("Multiply 81 by 550", ["= 81 × 500 + 81 × 50", "= 40500 + 4050", "!= 44550"]),
    ]
    ps.append(part("(v)", "Find the sum of all 3-digit natural numbers which are divisible by 11.", st, "Sum = 44550",
                   [("Quick check: 11 × (10 + 11 + … + 90)", ["11 × 4050 = 44550"])]))
    problem(7, "Sums of multiples", ["an", "s2"], [6, 12, 18, 24, 30, 36], ps)


q7()


# ======================================================================= Q8, Q9
problem(8, "Finding a term from Sₙ", ["diff"], [3 + 5 + 8, 11, 14, 17, 20, 23], [part(
    "", "In an AP the sum of first n terms is  {3n²|2} + {13n|2}.  Find its 25th term.",
    [
        ("We use: the 25th term is S₂₅ minus S₂₄", ["a₂₅ = S₂₅ − S₂₄"]),
        ("First find S₂₅. Put n = 25", ["S₂₅ = {3(25)²|2} + {13(25)|2}", "= {3(625)|2} + {325|2}", "= {1875|2} + {325|2}", "= {2200|2} = 1100"]),
        ("Now find S₂₄. Put n = 24", ["S₂₄ = {3(24)²|2} + {13(24)|2}", "= {3(576)|2} + {312|2}", "= {1728|2} + {156 × 2|2}", "= 864 + 156 = 1020"]),
        ("Subtract", ["a₂₅ = 1100 − 1020", "!a₂₅ = 80"]),
    ],
    "a₂₅ = 80",
    [("Quick check using a general formula: aₙ = Sₙ − Sₙ₋₁ = 3n + 5", ["a₂₅ = 3(25) + 5 = 75 + 5 = 80"])],
    short="Sum of n terms is 3n²/2 + 13n/2. Find the 25th term.")])

problem(9, "Finding a term from Sₙ", ["diff"], [4, 9, 14, 19, 24, 29], [part(
    "", "The sum of n terms of an AP is  {5n²|2} + {3n|2}.  Find its 20th term.",
    [
        ("We use: the 20th term is S₂₀ minus S₁₉", ["a₂₀ = S₂₀ − S₁₉"]),
        ("First find S₂₀. Put n = 20", ["S₂₀ = {5(20)²|2} + {3(20)|2}", "= {5(400)|2} + {60|2}", "= {2000|2} + 30", "= 1000 + 30 = 1030"]),
        ("Now find S₁₉. Put n = 19", ["S₁₉ = {5(19)²|2} + {3(19)|2}", "= {5(361)|2} + {57|2}", "= {1805|2} + {57|2}", "= {1862|2} = 931"]),
        ("Subtract", ["a₂₀ = 1030 − 931", "!a₂₀ = 99"]),
    ],
    "a₂₀ = 99",
    [("Quick check using the general formula aₙ = 5n − 1", ["a₂₀ = 5(20) − 1 = 99"])],
    short="Sum of n terms is 5n²/2 + 3n/2. Find the 20th term.")])


# ======================================================================= Q10
problem(10, "Which term? and the sum", ["an", "s2"], [5, 9, 13, 17, 21, 25], [part(
    "", "Which term of the AP 5, 9, 13, 17, … is 81? Also find the sum 5 + 9 + 13 + 17 + … + 81.",
    [
        ("Find a and d", ["a = 5,   d = 9 − 5 = 4"]),
        ("Set the nth term equal to 81", ["aₙ = a + (n − 1)d", "81 = 5 + (n − 1)(4)"]),
        ("Subtract 5 from both sides", ["81 − 5 = 4(n − 1)", "76 = 4(n − 1)"]),
        ("Divide by 4, then add 1", ["n − 1 = {76|4} = 19", "!n = 20"]),
        ("So 81 is the 20th term. Now the sum of all 20 terms", ["S₂₀ = {20|2} (5 + 81)"]),
        ("Add inside the bracket, then multiply", ["= 10 × 86", "!= 860"]),
    ],
    "81 is the 20th term,   Sum = 860",
    [("Quick check with the other formula", ["S₂₀ = 10 [10 + 19 × 4] = 10 × 86 = 860"])],
    short="Which term of 5, 9, 13, 17, … is 81? Find 5 + 9 + … + 81.")])


# ======================================================================= Q11
problem(11, "nth term from the sum", ["diff", "s2"], [7, 13, 17, 21, 25, 29], [
    part("(i)", "The sum of the first n terms of an AP is Sₙ = 2n² + 5n. Find the nth term.", [
        ("We use: aₙ = Sₙ − Sₙ₋₁", ["aₙ = Sₙ − Sₙ₋₁"]),
        ("Write Sₙ₋₁ by replacing n with n − 1", ["Sₙ₋₁ = 2(n − 1)² + 5(n − 1)"]),
        ("Expand (n − 1) squared as n² − 2n + 1", ["= 2(n² − 2n + 1) + 5n − 5", "= 2n² − 4n + 2 + 5n − 5", "= 2n² + n − 3"]),
        ("Subtract Sₙ₋₁ from Sₙ. Be careful with the minus signs", ["aₙ = (2n² + 5n) − (2n² + n − 3)", "= 2n² + 5n − 2n² − n + 3"]),
        ("2n² cancels. Combine the n terms", ["!aₙ = 4n + 3"]),
    ], "aₙ = 4n + 3", [("Quick check: the first term a₁ should equal S₁", ["a₁ = 4(1) + 3 = 7,   S₁ = 2 + 5 = 7"])]),
    part("(ii)", "If the nth term of an AP is 2n + 1, find the sum of the first n terms.", [
        ("Find the first term: put n = 1", ["a = a₁ = 2(1) + 1 = 3"]),
        ("The last term is the nth term", ["l = 2n + 1"]),
        ("Use the second sum formula", ["Sₙ = {n|2} (a + l)", "= {n|2} (3 + 2n + 1)"]),
        ("Add inside the bracket", ["= {n|2} (2n + 4)"]),
        ("Cancel the 2, then multiply out", ["= n (n + 2)", "!= n² + 2n"]),
    ], "Sₙ = n² + 2n", [("Quick check with n = 3: the terms are 3, 5, 7", ["S₃ = 9 + 6 = 15 = 3 + 5 + 7"])]),
])

# ======================================================================= Q12
problem(12, "nth term, first term and d from Sₙ", ["diff"], [2, 8, 14, 20, 26, 32], [part(
    "", "If the sum of the first n terms of an AP is Sₙ = 3n² − n, find its (i) nth term, (ii) first term and (iii) common difference.",
    [
        ("(i) Use aₙ = Sₙ − Sₙ₋₁. First write Sₙ₋₁", ["Sₙ₋₁ = 3(n − 1)² − (n − 1)"]),
        ("Expand (n − 1) squared", ["= 3(n² − 2n + 1) − n + 1", "= 3n² − 6n + 3 − n + 1", "= 3n² − 7n + 4"]),
        ("Subtract", ["aₙ = (3n² − n) − (3n² − 7n + 4)", "= 3n² − n − 3n² + 7n − 4"]),
        ("3n² cancels. Combine the n terms", ["!aₙ = 6n − 4"]),
        ("(ii) First term: put n = 1", ["a₁ = 6(1) − 4", "!a₁ = 2"]),
        ("(iii) Common difference: find a₂ and subtract", ["a₂ = 6(2) − 4 = 8", "d = a₂ − a₁ = 8 − 2", "!d = 6"]),
    ],
    "aₙ = 6n − 4,   a = 2,   d = 6",
    [("Quick check: S₁ = 3 − 1 = 2, and S₂ = 12 − 2 = 10 = 2 + 8", ["S₂ = 10 ✓"])],
    short="Sₙ = 3n² − n. Find the nth term, first term and common difference.")])

# ======================================================================= Q13
problem(13, "A sum with n terms", ["s2", "an"], [0.9, 0.8, 0.7, 0.6, 0.5, 0.4], [part(
    "", "Find the sum  (1 − 1/n) + (1 − 2/n) + (1 − 3/n) + … up to n terms.",
    [
        ("Find the first term", ["a = 1 − {1|n} = {n − 1|n}"]),
        ("Find the common difference: second term minus first", ["d = (1 − {2|n}) − (1 − {1|n})", "= 1 − {2|n} − 1 + {1|n}", "= −{1|n}"]),
        ("Find the last term, the nth term, by putting n in the pattern", ["l = 1 − {n|n} = 1 − 1 = 0"]),
        ("Use the second sum formula", ["Sₙ = {n|2} (a + l)", "= {n|2} ({n − 1|n} + 0)"]),
        ("The n on the top cancels the n on the bottom", ["!= {n − 1|2}"]),
    ],
    "Sₙ = {n − 1|2}",
    [("Quick check with n = 4: the terms are 3/4, 1/2, 1/4, 0", ["Sum = {3|4} + {2|4} + {1|4} + 0 = {6|4} = {3|2} = {4 − 1|2} ✓"])],
    short="Find (1 − 1/n) + (1 − 2/n) + (1 − 3/n) + … up to n terms.")])

# ======================================================================= Q14, Q15
problem(14, "Finding n and d", ["s2", "an"], [22, 19, 16, 13, 10, 7], [part(
    "", "In an AP the first term is 22, the nth term is −11 and the sum to n terms is 66. Find n and d.",
    [
        ("Write down what we know", ["a = 22,   l = aₙ = −11,   Sₙ = 66"]),
        ("Use the second sum formula", ["Sₙ = {n|2} (a + l)", "66 = {n|2} (22 + (−11))"]),
        ("Add inside the bracket", ["66 = {n|2} × 11"]),
        ("Multiply both sides by 2", ["132 = 11n"]),
        ("Divide both sides by 11", ["!n = {132|11} = 12"]),
        ("Now find d using the nth term formula", ["aₙ = a + (n − 1)d", "−11 = 22 + (12 − 1)d", "−11 = 22 + 11d"]),
        ("Subtract 22 from both sides", ["−11 − 22 = 11d", "−33 = 11d"]),
        ("Divide by 11", ["!d = −3"]),
    ],
    "n = 12,   d = −3",
    [("Quick check: the 12th term is 22 + 11(−3) = −11, and the sum is", ["S₁₂ = 6 (22 − 11) = 6 × 11 = 66 ✓"])])])

problem(15, "Finding n and d", ["s2", "an"], [8, 13, 18, 23, 28, 33], [part(
    "", "In an AP the first term is 8, the nth term is 33 and the sum to n terms is 123. Find n and d.",
    [
        ("Write down what we know", ["a = 8,   l = aₙ = 33,   Sₙ = 123"]),
        ("Use the second sum formula", ["Sₙ = {n|2} (a + l)", "123 = {n|2} (8 + 33)"]),
        ("Add inside the bracket", ["123 = {n|2} × 41"]),
        ("Multiply both sides by 2", ["246 = 41n"]),
        ("Divide both sides by 41", ["!n = {246|41} = 6"]),
        ("Now find d using the nth term formula", ["aₙ = a + (n − 1)d", "33 = 8 + (6 − 1)d", "33 = 8 + 5d"]),
        ("Subtract 8 from both sides", ["33 − 8 = 5d", "25 = 5d"]),
        ("Divide by 5", ["!d = 5"]),
    ],
    "n = 6,   d = 5",
    [("Quick check: the terms are 8, 13, 18, 23, 28, 33", ["8 + 13 + 18 + 23 + 28 + 33 = 123 ✓"])])])

# ======================================================================= Q16
problem(16, "nth term from the sum", ["diff"], [8, 18, 28, 38, 48, 58], [part(
    "", "If Sₙ, the sum of the first n terms of an AP, is Sₙ = 5n² + 3n, find its nth term.",
    [
        ("We use: aₙ = Sₙ − Sₙ₋₁", ["aₙ = Sₙ − Sₙ₋₁"]),
        ("Write Sₙ₋₁ by replacing n with n − 1", ["Sₙ₋₁ = 5(n − 1)² + 3(n − 1)"]),
        ("Expand (n − 1) squared", ["= 5(n² − 2n + 1) + 3n − 3", "= 5n² − 10n + 5 + 3n − 3", "= 5n² − 7n + 2"]),
        ("Subtract. Watch the signs", ["aₙ = (5n² + 3n) − (5n² − 7n + 2)", "= 5n² + 3n − 5n² + 7n − 2"]),
        ("5n² cancels. Combine the n terms", ["!aₙ = 10n − 2"]),
    ],
    "aₙ = 10n − 2",
    [("Quick check: a₁ = S₁", ["a₁ = 10 − 2 = 8,   S₁ = 5 + 3 = 8 ✓"])])])

# ======================================================================= Q17
problem(17, "Two clues about an AP", ["s1", "an"], [2, 4, 6, 8, 10, 12], [part(
    "", "The sum of the first six terms of an AP is 42. The ratio of its 10th term to its 30th term is 1 : 3. Calculate the first and the thirteenth term.",
    [
        ("Clue 1: the sum of 6 terms is 42", ["S₆ = {6|2} [2a + 5d] = 42", "3 (2a + 5d) = 42"]),
        ("Divide by 3", ["2a + 5d = 14      ...  (1)"]),
        ("Clue 2: the ratio of the 10th term to the 30th is 1 to 3", ["{a₁₀|a₃₀} = {1|3}", "{a + 9d|a + 29d} = {1|3}"]),
        ("Cross multiply", ["3 (a + 9d) = 1 (a + 29d)", "3a + 27d = a + 29d"]),
        ("Collect a on one side and d on the other", ["3a − a = 29d − 27d", "2a = 2d", "a = d      ...  (2)"]),
        ("Put a = d into equation (1)", ["2d + 5d = 14", "7d = 14", "d = 2"]),
        ("Then a equals d", ["!a = 2"]),
        ("Now the 13th term", ["a₁₃ = a + 12d = 2 + 12(2)", "= 2 + 24", "!a₁₃ = 26"]),
    ],
    "First term = 2,   13th term = 26",
    [("Quick check: the AP is 2, 4, 6, 8, …", ["S₆ = 2 + 4 + 6 + 8 + 10 + 12 = 42 ✓", "a₁₀ : a₃₀ = 20 : 60 = 1 : 3 ✓"])])])

# ======================================================================= Q18
problem(18, "Prove S₃ = 3(S₂ − S₁)", ["s1"], [1, 2, 3, 4, 5, 6], [part(
    "", "The sums of n, 2n and 3n terms of an AP are S₁, S₂ and S₃. Prove that S₃ = 3(S₂ − S₁).",
    [
        ("Write each sum with the formula Sₙ equals n over 2 times the bracket", ["Sₙ = {n|2} [2a + (n − 1)d]"]),
        ("S one is the sum of n terms", ["S₁ = {n|2} [2a + (n − 1)d]"]),
        ("S two is the sum of 2n terms. Replace n by 2n", ["S₂ = {2n|2} [2a + (2n − 1)d]", "= n [2a + (2n − 1)d]"]),
        ("S three is the sum of 3n terms. Replace n by 3n", ["S₃ = {3n|2} [2a + (3n − 1)d]"]),
        ("Now work out S two minus S one. Take n over 2 out as a common factor", ["S₂ − S₁ = {n|2} [2(2a + (2n − 1)d) − (2a + (n − 1)d)]"]),
        ("Open the brackets inside", ["= {n|2} [4a + (4n − 2)d − 2a − (n − 1)d]"]),
        ("Combine the a terms and the d terms", ["= {n|2} [2a + (4n − 2 − n + 1)d]", "= {n|2} [2a + (3n − 1)d]"]),
        ("Multiply by 3", ["3 (S₂ − S₁) = {3n|2} [2a + (3n − 1)d]"]),
        ("This is exactly S three", ["!3 (S₂ − S₁) = S₃"]),
    ],
    "S₃ = 3(S₂ − S₁)   — proved ✓",
    [("Quick check with a = 1, d = 1, n = 1: S₁ = 1, S₂ = 3, S₃ = 6", ["3 (3 − 1) = 6 = S₃ ✓"])],
    short="Prove S₃ = 3(S₂ − S₁), where S₁, S₂, S₃ are sums of n, 2n, 3n terms.")])

# ======================================================================= Q19
problem(19, "Prove the sum of (m + n) terms is 0", ["s1"], [3, 2, 1, 0, -1, -2], [part(
    "", "If the sum of m terms of an AP is the same as the sum of its n terms, show that the sum of its (m + n) terms is zero.",
    [
        ("Write down what is given: the two sums are equal", ["Sₘ = Sₙ"]),
        ("Use the sum formula on both sides", ["{m|2} [2a + (m − 1)d] = {n|2} [2a + (n − 1)d]"]),
        ("Multiply both sides by 2", ["m [2a + (m − 1)d] = n [2a + (n − 1)d]"]),
        ("Open the brackets", ["2am + m(m − 1)d = 2an + n(n − 1)d", "2am + (m² − m)d = 2an + (n² − n)d"]),
        ("Collect everything on the left side", ["2am − 2an + (m² − m − n² + n)d = 0"]),
        ("Factor: 2a times (m − n), and m² − n² is (m − n)(m + n)", ["2a (m − n) + [(m² − n²) − (m − n)] d = 0", "2a (m − n) + [(m − n)(m + n) − (m − n)] d = 0"]),
        ("Take (m − n) out as a common factor", ["(m − n) [2a + (m + n − 1) d] = 0"]),
        ("m and n are different, so m − n is not zero. So the other factor must be zero", ["2a + (m + n − 1) d = 0      ...  (★)"]),
        ("Now write the sum of (m + n) terms", ["Sₘ₊ₙ = {m + n|2} [2a + (m + n − 1) d]"]),
        ("The bracket is zero by (★)", ["= {m + n|2} × 0", "!= 0"]),
    ],
    "Sₘ₊ₙ = 0   — shown ✓",
    [("Quick check with the AP 3, 2, 1, 0, −1, −2, …: S₂ = 5 and S₃ = 6 are not equal, but S₃ = S₄ = 6 is", ["Here m = 3, n = 4, and S₇ = 3 + 2 + 1 + 0 − 1 − 2 − 3 = 0 ✓"])],
    short="If Sₘ = Sₙ, show that Sₘ₊ₙ = 0.")])

# ======================================================================= Q20
problem(20, "Common difference from Sₚ", ["diff", "d"], [1, 3, 5, 7, 9, 11], [part(
    "", "If the sum of the first p terms of an AP is ap² + bp, find the common difference.",
    [
        ("Find the first term: put p = 1", ["S₁ = a(1)² + b(1) = a + b", "first term = a + b"]),
        ("Find the sum of 2 terms: put p = 2", ["S₂ = a(2)² + b(2) = 4a + 2b"]),
        ("The second term is S two minus S one", ["second term = (4a + 2b) − (a + b)", "= 4a + 2b − a − b", "= 3a + b"]),
        ("Common difference is the second term minus the first term", ["d = (3a + b) − (a + b)", "= 3a + b − a − b"]),
        ("b cancels, and 3a minus a is 2a", ["!d = 2a"]),
    ],
    "d = 2a",
    [("Quick check with the general formula", ["aₚ = Sₚ − Sₚ₋₁ = 2ap − a + b,   so the terms rise by 2a each time ✓"])])])

# ======================================================================= Q21
problem(21, "Sum of n terms from two sums", ["s1"], [1, 3, 5, 7, 9, 11], [part(
    "", "If the sum of the first 7 terms of an AP is 49 and that of 17 terms is 289, find the sum of the first n terms.",
    [
        ("Use the sum formula for 7 terms", ["S₇ = {7|2} [2a + 6d] = 49", "7 (a + 3d) = 49"]),
        ("Divide by 7", ["a + 3d = 7      ...  (1)"]),
        ("Use the sum formula for 17 terms", ["S₁₇ = {17|2} [2a + 16d] = 289", "17 (a + 8d) = 289"]),
        ("Divide by 17", ["a + 8d = 17      ...  (2)"]),
        ("Subtract equation (1) from equation (2)", ["(a + 8d) − (a + 3d) = 17 − 7", "5d = 10", "d = 2"]),
        ("Put d = 2 into equation (1)", ["a + 3(2) = 7", "a + 6 = 7", "a = 1"]),
        ("Now the sum of n terms", ["Sₙ = {n|2} [2a + (n − 1)d]", "= {n|2} [2(1) + (n − 1)(2)]"]),
        ("Simplify inside the bracket", ["= {n|2} [2 + 2n − 2]", "= {n|2} × 2n"]),
        ("The 2s cancel", ["!= n²"]),
    ],
    "Sₙ = n²",
    [("Quick check: the AP is 1, 3, 5, 7, …", ["S₇ = 49 = 7² ✓,   S₁₇ = 289 = 17² ✓"])])])

# ======================================================================= Q22
problem(22, "Common difference from a, l and the sum", ["s2", "an"], [2, 5, 8, 11, 14, 17], [part(
    "", "In an AP the first term is 2, the last term is 29 and the sum of the terms is 155. Find the common difference.",
    [
        ("Write down what we know", ["a = 2,   l = 29,   Sₙ = 155"]),
        ("Use the second sum formula to find n", ["Sₙ = {n|2} (a + l)", "155 = {n|2} (2 + 29)", "155 = {n|2} × 31"]),
        ("Multiply both sides by 2", ["310 = 31n"]),
        ("Divide by 31", ["n = {310|31} = 10"]),
        ("Now use the nth term formula with l = 29", ["l = a + (n − 1)d", "29 = 2 + (10 − 1)d", "29 = 2 + 9d"]),
        ("Subtract 2 from both sides", ["27 = 9d"]),
        ("Divide by 9", ["!d = 3"]),
    ],
    "d = 3",
    [("Quick check: the terms are 2, 5, 8, 11, 14, 17, 20, 23, 26, 29", ["Sum = 5 × (2 + 29) = 5 × 31 = 155 ✓"])])])

# ======================================================================= Q23
problem(23, "Find the AP", ["s1"], [3, -1, -5, -9, -13, -17], [part(
    "", "In an AP the sum of the first ten terms is −150 and the sum of its next ten terms is −550. Find the AP.",
    [
        ("The first ten terms add up to −150", ["S₁₀ = −150"]),
        ("The first twenty terms are the first ten plus the next ten", ["S₂₀ = −150 + (−550) = −700"]),
        ("Use the sum formula for 10 terms", ["{10|2} [2a + 9d] = −150", "5 (2a + 9d) = −150"]),
        ("Divide by 5", ["2a + 9d = −30      ...  (1)"]),
        ("Use the sum formula for 20 terms", ["{20|2} [2a + 19d] = −700", "10 (2a + 19d) = −700"]),
        ("Divide by 10", ["2a + 19d = −70      ...  (2)"]),
        ("Subtract equation (1) from equation (2)", ["(2a + 19d) − (2a + 9d) = −70 − (−30)", "10d = −70 + 30", "10d = −40", "d = −4"]),
        ("Put d = −4 into equation (1)", ["2a + 9(−4) = −30", "2a − 36 = −30", "2a = 6", "a = 3"]),
        ("Build the AP: add d = −4 each time", ["!3, −1, −5, −9, −13, …"]),
    ],
    "The AP is 3, −1, −5, −9, …",
    [("Quick check: the first ten terms go 3 down to −33", ["S₁₀ = 5 (3 − 33) = 5 × (−30) = −150 ✓"])])])

# ======================================================================= Q24
problem(24, "Find the 25th term", ["s1", "an"], [10, 25, 40, 55, 70, 85], [part(
    "", "The sum of the first 14 terms of an AP is 1505 and its first term is 10. Find its 25th term.",
    [
        ("Write down what we know", ["a = 10,   n = 14,   S₁₄ = 1505"]),
        ("Use the sum formula", ["1505 = {14|2} [2(10) + (14 − 1)d]", "1505 = 7 [20 + 13d]"]),
        ("Divide both sides by 7", ["{1505|7} = 20 + 13d", "215 = 20 + 13d"]),
        ("Subtract 20 from both sides", ["195 = 13d"]),
        ("Divide by 13", ["d = {195|13} = 15"]),
        ("Now find the 25th term", ["a₂₅ = a + (25 − 1)d", "= 10 + 24 × 15", "= 10 + 360", "!a₂₅ = 370"]),
    ],
    "a₂₅ = 370",
    [("Quick check: S₁₄ with d = 15", ["a₁₄ = 10 + 13 × 15 = 205,   S₁₄ = 7 (10 + 205) = 7 × 215 = 1505 ✓"])])])

# ======================================================================= Q25
problem(25, "Seven cash prizes", ["s1"], [160, 140, 120, 100, 80, 60], [part(
    "", "₹700 is to be used to give seven cash prizes to students. Each prize is ₹20 less than the one before it. Find the value of each prize.",
    [
        ("The prizes make an AP. Seven prizes, ₹20 less each time, total ₹700", ["n = 7,   d = −20,   S₇ = 700"]),
        ("Use the sum formula", ["700 = {7|2} [2a + (7 − 1)(−20)]", "700 = {7|2} [2a − 120]"]),
        ("Multiply both sides by 2, then divide by 7", ["1400 = 7 (2a − 120)", "200 = 2a − 120"]),
        ("Add 120 to both sides", ["320 = 2a"]),
        ("Divide by 2", ["!a = 160"]),
        ("The first prize is ₹160. Subtract 20 each time to get the others", ["160, 140, 120, 100, 80, 60, 40"]),
    ],
    "₹160, ₹140, ₹120, ₹100, ₹80, ₹60, ₹40",
    [("Quick check: add all seven prizes", ["160 + 140 + 120 + 100 + 80 + 60 + 40 = 700 ✓"])],
    short="₹700 for 7 prizes, each ₹20 less than the one before. Find each prize.")])
