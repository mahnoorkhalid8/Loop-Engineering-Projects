from bugs import add, is_even

def run():
    assert add(2, 3) == 5, f"add(2,3) should be 5, got {add(2,3)}"
    assert is_even(4) is True, f"is_even(4) should be True, got {is_even(4)}"
    assert is_even(3) is False, f"is_even(3) should be False, got {is_even(3)}"
    print("ALL TESTS PASSED")

if __name__ == "__main__":
    run()
