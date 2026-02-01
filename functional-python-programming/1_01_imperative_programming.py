"""
The variable `n` ranges over values where (1 <= n < 10). Because the loop iterates through these values in order,
we can guarantee that it terminates once `n == 10`. Equivalent logic could be implemented in C or Java using their
primitive (non-object) data types.

Python, however, does not use primitive types in the same way. To be precise, we can instead fully embrace Python’s
object-oriented model.

In imperative programming, variables are used to explicitly represent the state of the program. Assignment statements
update these variables, advancing the computation toward completion.
"""
class SummableList(list):
    def sum(self):
        s = 0
        for v in self.__iter__():
            s += v
        return s
