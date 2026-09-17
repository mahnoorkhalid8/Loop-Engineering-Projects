#!/usr/bin/env bash
# Rebuilds demo-repo from scratch and runs one full beat of the morning
# triage loop: find candidates -> draft each in an isolated worktree ->
# reviewer verdict -> merge PASS, escalate FAIL -> update progress.md.
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
rm -rf demo-repo wt-fix-tax wt-fix-restock wt-pricing-format
mkdir demo-repo
cd demo-repo
git init -q
git config user.email "demo@example.com"
git config user.name "Loop Demo"

cat > discount.py << 'EOF'
def apply_tax(amount, rate):
    """rate is a fraction, e.g. 0.08 for 8% tax."""
    return amount + rate  # BUG: should be amount * (1 + rate)
EOF

cat > inventory.py << 'EOF'
def last_restocked(dates):
    """dates is a list of restock timestamps, oldest first."""
    return dates[len(dates)]  # BUG: off-by-one, should be dates[len(dates) - 1]
EOF

cat > pricing.py << 'EOF'
def serialize_price(cents):
    """Public API used by the mobile app and the partner integration."""
    return cents
EOF

cat > tests.py << 'EOF'
from discount import apply_tax
from inventory import last_restocked

def run():
    assert round(apply_tax(100, 0.08), 2) == 108.0, f"apply_tax(100,0.08) should be 108.0, got {apply_tax(100, 0.08)}"
    assert last_restocked([1, 2, 3]) == 3, "last_restocked should return the last item"
    print("ALL TESTS PASSED")

if __name__ == "__main__":
    run()
EOF

cat > test_discount.py << 'EOF'
from discount import apply_tax

def run():
    assert round(apply_tax(100, 0.08), 2) == 108.0, f"apply_tax(100,0.08) should be 108.0, got {apply_tax(100, 0.08)}"
    print("test_discount: PASSED")

if __name__ == "__main__":
    run()
EOF

cat > test_inventory.py << 'EOF'
from inventory import last_restocked

def run():
    assert last_restocked([1, 2, 3]) == 3, "last_restocked should return the last item"
    print("test_inventory: PASSED")

if __name__ == "__main__":
    run()
EOF

cat > advisory.md << 'EOF'
# Simulated overnight advisory

`pricing.py`'s `serialize_price()` currently returns a raw integer
(cents). A "safe fix" was proposed to make it return a formatted string
(`"$1.08"`) for readability -- but `serialize_price()` is called by the
mobile app and the partner integration (see its docstring). Changing its
return type is a **public behavior change**, not an internal fix.
EOF

git add -A && git commit -q -m "initial: two overnight CI failures, one stable public API, plus tests"

echo "### STEP 1: find the work ###"
echo "(would be: failing CI + advisory.md, in a real run)"

echo
echo "### STEP 2: draft each candidate in its own worktree ###"
git worktree add -q -b claude/fix-tax ../wt-fix-tax
git worktree add -q -b claude/fix-restock ../wt-fix-restock
git worktree add -q -b claude/pricing-string-format ../wt-pricing-format

(cd ../wt-fix-tax && \
  sed -i 's/return amount + rate  # BUG: should be amount \* (1 + rate)/return amount * (1 + rate)/' discount.py && \
  git add -A && git commit -q -m "fix: apply_tax should multiply, not add")

(cd ../wt-fix-restock && \
  sed -i 's/return dates\[len(dates)\]  # BUG: off-by-one, should be dates\[len(dates) - 1\]/return dates[len(dates) - 1]/' inventory.py && \
  git add -A && git commit -q -m "fix: last_restocked off-by-one")

(cd ../wt-pricing-format && \
  sed -i 's/return cents/return f"\${cents\/100:.2f}"/' pricing.py && \
  git add -A && git commit -q -m "fix: format serialize_price as currency string for readability")

echo
echo "### STEP 3: reviewer verdicts ###"
echo "-- claude/fix-tax --"
(cd ../wt-fix-tax && $PYTHON test_discount.py)
echo "-- claude/fix-restock --"
(cd ../wt-fix-restock && $PYTHON test_inventory.py)
echo "-- claude/pricing-string-format --"
(cd ../wt-pricing-format && $PYTHON -c "
from pricing import serialize_price
r = serialize_price(108)
print('serialize_price(108) =', repr(r), '| type:', type(r).__name__, '-- return type changed on a documented public API -> FAIL')
")

echo
echo "### STEP 4: merge PASS, leave FAIL unmerged ###"
git merge -q claude/fix-tax -m "merge: fix-tax (reviewer: PASS)"
git merge -q claude/fix-restock -m "merge: fix-restock (reviewer: PASS)"
echo "full suite on master:"
$PYTHON tests.py
echo "pricing.py on master (untouched -- FAIL branch never merged):"
$PYTHON -c "from pricing import serialize_price; print(serialize_price(108), type(serialize_price(108)).__name__)"

git worktree remove ../wt-fix-tax --force 2>/dev/null || true
git worktree remove ../wt-fix-restock --force 2>/dev/null || true
git worktree remove ../wt-pricing-format --force 2>/dev/null || true
git worktree prune

echo
echo "### final history ###"
git log --oneline --graph
