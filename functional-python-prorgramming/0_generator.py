def echo():
    """
    Demonstrate that a generator is a bidirectional coroutine rather than
    a simple value producer.

    When execution reaches the `yield` expression, the function pauses and
    produces a value to the caller. At this suspension point, the generator
    maintains its internal state.

    Unlike ordinary functions, a generator may later be resumed. When resumed
    using `.send(value)`, the value provided by the caller becomes the result
    of the suspended `yield` expression.

    In this way, `yield` serves two roles:

    1. It produces a value outward to the caller.
    2. It later receives a value sent back inward.

    This two-way data flow is the conceptual foundation of Python's
    `Generator[YieldType, SendType, ReturnType]` type:

        YieldType  -> type of values produced by `yield`
        SendType   -> type of values accepted via `.send(...)`
        ReturnType -> final value produced when the generator terminates

    In this example:

        YieldType  = str     ("ready")
        SendType   = str     ("hello")
        ReturnType = None    (no explicit return statement)

    The generator completes when execution reaches the end of the function
    body, at which point Python raises `StopIteration` internally to signal
    termination.
    """
    received = yield "ready"
    print("Got:", received)


"""
Drive the generator manually to make its lifecycle explicit.

1. Create the generator object. (No code runs yet.)
2. Start execution with `next(...)` until the first `yield`.
3. Resume execution by sending a value back into the suspended frame.
4. Observe termination via StopIteration.
"""
g = echo()

print(next(g))     # Step 1: start execution; yields "ready"
g.send("hello")    # Step 2: resume execution; "hello" is assigned to `received`