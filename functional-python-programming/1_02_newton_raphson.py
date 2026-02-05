"""
Square root approximation using functional iteration.

This module demonstrates how a traditionally stateful numerical algorithm
(Newton–Raphson square root approximation) can be expressed using functional
concepts such as pure functions, generators, and recursion.

Instead of mutating variables inside loops, the algorithm models state as a
sequence of values that converge toward the desired result.
"""

def next_(n, x):
    """
    Compute the next approximation of sqrt(n) from a current approximation
    as a single Newton–Raphson update step.

    No state is stored or mutated. Each call depends only on its inputs.
    """
    return (x + n / x) / 2


def repeat(f, a):
    """
    Turns a single-step function into an infinite sequence by repeatedly applying a function.

    The first yielded value is the initial seed `a`. Each subsequent value
    is computed by applying `f` to the previous value.

    This replaces an explicit loop with an infinite generator that models
    state progression as a stream of values.
    """
    yield a
    yield from repeat(f, f(a))


def within(e, iterable):
    """
    Consumes the infinite sequence safely.

    Two successive values from the iterable are compared. When their absolute
    difference is less than or equal to `epsilon`, the approximation is
    considered accurate enough and is returned.

    This function safely terminates consumption of an otherwise infinite
    sequence.
    """
    def head_tail(e, a, iterable):
        b = next(iterable)
        if abs(a - b) <= e:
            return b
        return head_tail(e, b, iterable)

    return head_tail(e, next(iterable), iterable)


def sqrt(a0, e, n):
    """
    Compute the square root of `n` using functional composition.

    - `a0` is the initial approximation
    - `e` is the allowed error tolerance
    - `n` is the value whose square root is desired

    The approximation sequence is generated lazily and terminated once
    convergence is detected.
    """
    step = lambda x: next_(n, x)
    return within(e, repeat(step, a0))


"""
Example usage.

The initial guess does not need to be exact. Values closer to the true square
root will converge more quickly, but 1.0 works well for most inputs.
"""
if __name__ == "__main__":
    result = sqrt(1.0, 0.0001, 3)
    print(result)
