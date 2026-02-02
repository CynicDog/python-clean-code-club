class SummableList(list):
    """
    Compute a sum by defining stateful, imperative behavior directly on a data structure.

    The variable `n` ranges over values where (1 <= n < 10). Because the loop iterates through
    these values in order, we can guarantee that it terminates once `n == 10`. Equivalent
    logic could be implemented in C or Java using their primitive (non-object) data types.

    Python, however, does not use primitive types in the same way. Instead, we can embrace
    its object-oriented model by defining behavior directly on data structures.

    In imperative programming, variables explicitly represent program state. Assignment
    statements update these variables step by step, advancing the computation toward
    completion.
    """
    def sum(self):
        s = 0
        for v in self.__iter__():
            s += v
        return s

"""
Accumulate qualifying values imperatively and compute their sum using stateful behavior defined on the list itself.
"""
m = SummableList()
for n in range(1, 10):
    if n % 3 == 0 or n % 5 == 0:
        m.append(n)


def functional_sum(seq):
    """
    Compute the sum of a sequence using recursion.

    The definition consists of two cases. The base case states that the sum of an empty
    sequence is 0. The recursive case states that the sum of a sequence is the first element
    plus the sum of the remaining elements.

    Because each recursive call operates on a shorter sequence, the computation is
    guaranteed to eventually reach the base case and terminate.
    """
    if len(seq) == 0:
        return 0
    return seq[0] + functional_sum(seq[1:])


def until(n, filter_func, v):
    """
    Define a sequence of values using recursion.

    The value `v` is compared against the upper bound `n`. When `v == n`, the resulting
    sequence is empty, which forms the base case of the recursion.

    For values below `n`, the given `filter_func` determines whether `v` is included in
    the result. Accepted values are placed in a single-element list and combined with the
    remainder of the sequence; rejected values are skipped. Each recursive call advances
    `v`, ensuring termination.
    """
    if v == n:
        return []
    if filter_func(v):
        return [v] + until(n, filter_func, v + 1)
    else:
        return until(n, filter_func, v + 1)

"""
Generate qualifying values functionally by defining sequence construction through recursion rather than mutable state.
"""
mult_3_5 = lambda x: x % 3 == 0 or x % 5 == 0
until(10, mult_3_5, 3)


"""
Compute a sum using a functional hybrid by composing generator expressions.

Values are produced lazily by iterable expressions rather than accumulated through
mutable state or explicit recursion. The variable `n` is bound to each generated value
to describe membership in the sequence, not to represent the state of the computation.
"""
functional_sum(n for n in range(1, 10) if n % 3 == 0 or n % 5 == 0)
