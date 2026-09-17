def add(a, b):
    """Two independent bugs live here, simulating two overnight CI failures."""
    return a - b  # BUG: should be a + b


def is_even(n):
    return n % 2 == 0  # fixed by Agent B, in its own worktree
