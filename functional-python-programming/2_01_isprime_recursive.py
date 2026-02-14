"""
Functional Primality Testing via Tail Recursion.

This module demonstrates how to implement a primality test using recursive
logic rather than imperative loops. It leverages the concept of trial
division limited by the square root of the target number.

The algorithm models the search for a divisor as a sequence of state
transitions, passing the current candidate divisor forward until a
base case (factor found or limit reached) is satisfied.
"""

import sys

sys.setrecursionlimit(1000) # default

def isprimer(n):
    """
    Determine if a number n is prime using functional recursion.
    """
    def isprime(k, coprime):
        """
        Internal tail-recursive function to test potential factors.
        """
        if coprime * coprime > k: return True
        if k % coprime == 0: return False
        return isprime(k, coprime + 2)

    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    return isprime(n, 3)


if __name__ == "__main__":
    test_values = [2, 3, 4, 17, 25, 97, 100, 101]

    print(f"{'Number':<10} | {'Is Prime?':<10}")
    print("-" * 25)

    for val in test_values:
        print(f"{val:<10} | {isprimer(val):<10}")