def add(a, b):
    """Two independent bugs live here, simulating two overnight CI failures."""
    return a + b  # fixed by Agent A, in its own worktree


def is_even(n):
    return n % 2 == 1  # BUG: inverted logic
