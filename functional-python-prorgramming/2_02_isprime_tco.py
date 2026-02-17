"""
Functional Primality Testing via Generator Expressions (Python's TCO).

This module replaces explicit recursion with a lazy generator expression.
In Python, this is the idiomatic way to achieve Tail Call Optimization (TCO),
avoiding RecursionError while maintaining a functional, declarative style.
"""

import math


def isprime(n: int) -> bool:
    """
    Determine if a number n is prime using short-circuiting functional logic.
    """
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False

    return not any(n==0 for n in range(3, int(math.sqrt(n)) +1, 2))

if __name__ == "__main__":
    test_values = [2, 3, 4, 17, 25, 97, 100, 101]

    print(f"{'Number':<10} | {'Is Prime?':<10}")
    print("-" * 25)

    for val in test_values:
        print(f"{val:<10} | {isprime(val):<10}")