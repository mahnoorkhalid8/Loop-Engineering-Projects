#!/usr/bin/env bash
# Rebuilds demo-repo from scratch and runs the full worktree-isolation demo:
#   Step A: two "agents" editing the same checkout -> a fix silently lost
#   Step B: same two fixes, via git worktrees -> both fixes survive
# Safe to re-run any time; it deletes and recreates demo-repo/ each time.
set -e
cd "$(dirname "$0")"

PYTHON=""
for candidate in python3 python; do
    if "$candidate" --version >/dev/null 2>&1; then
        PYTHON="$candidate"
        break
    fi
done
if [ -z "$PYTHON" ]; then
    echo "error: no working 'python3' or 'python' found on PATH" >&2
    exit 1
fi
rm -rf demo-repo wt-fix-add wt-fix-even
mkdir demo-repo
cd demo-repo
git init -q
git config user.email "demo@example.com"
git config user.name "Loop Demo"

cat > bugs.py << 'EOF'
def add(a, b):
    """Two independent bugs live here, simulating two overnight CI failures."""
    return a - b  # BUG: should be a + b


def is_even(n):
    return n % 2 == 1  # BUG: inverted logic
EOF

cat > tests.py << 'EOF'
from bugs import add, is_even

def run():
    assert add(2, 3) == 5, f"add(2,3) should be 5, got {add(2,3)}"
    assert is_even(4) is True, f"is_even(4) should be True, got {is_even(4)}"
    assert is_even(3) is False, f"is_even(3) should be False, got {is_even(3)}"
    print("ALL TESTS PASSED")

if __name__ == "__main__":
    run()
EOF

git add -A && git commit -q -m "initial: two broken functions, two failing tests"

echo "############################################"
echo "# STEP A: no isolation -- two agents race on one checkout"
echo "############################################"
AGENT_A_VERSION='def add(a, b):
    """Two independent bugs live here, simulating two overnight CI failures."""
    return a + b  # fixed by Agent A


def is_even(n):
    return n % 2 == 1  # BUG: inverted logic'

AGENT_B_VERSION='def add(a, b):
    """Two independent bugs live here, simulating two overnight CI failures."""
    return a - b  # BUG: should be a + b


def is_even(n):
    return n % 2 == 0  # fixed by Agent B'

echo "$AGENT_A_VERSION" > bugs.py
echo "Agent A wrote its fix."
echo "$AGENT_B_VERSION" > bugs.py
echo "Agent B (started from the stale original) wrote its fix, overwriting A's."
echo
echo "--- result: Agent A's fix is gone ---"
$PYTHON tests.py || echo "(tests fail -- add() is still broken, proving the collision)"
echo

git checkout -q -- bugs.py
echo "############################################"
echo "# STEP B: isolated worktrees -- same two fixes, no collision"
echo "############################################"
git worktree add -q -b claude/fix-add ../wt-fix-add
git worktree add -q -b claude/fix-even ../wt-fix-even

cd ../wt-fix-add
sed -i 's/return a - b  # BUG: should be a + b/return a + b  # fixed by Agent A, in its own worktree/' bugs.py
git add -A && git commit -q -m "fix: add() should sum, not subtract"

cd ../wt-fix-even
sed -i 's/return n % 2 == 1  # BUG: inverted logic/return n % 2 == 0  # fixed by Agent B, in its own worktree/' bugs.py
git add -A && git commit -q -m "fix: is_even() had inverted logic"

cd ../demo-repo
git merge -q claude/fix-add -m "merge: fix-add"
git merge -q claude/fix-even -m "merge: fix-even"

echo "--- merged bugs.py: both fixes present ---"
cat bugs.py
echo
echo "--- running tests on the merged result ---"
$PYTHON tests.py

git worktree remove ../wt-fix-add 2>/dev/null || rm -rf ../wt-fix-add
git worktree remove ../wt-fix-even 2>/dev/null || rm -rf ../wt-fix-even
git worktree prune

echo
echo "--- final git history (the diamond merge) ---"
git log --oneline --graph
