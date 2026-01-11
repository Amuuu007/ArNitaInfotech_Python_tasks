# Example functions to test
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

def greet(name):
    return f"Hello, {name}!"

# Test cases: (function, input, expected_output)
tests = [
    (add, (2, 3), 5),
    (add, (10, -5), 5),
    (multiply, (4, 5), 20),
    (multiply, (3, 0), 0),
    (greet, ("Alice",), "Hello, Alice!"),
    (greet, ("Bob",), "Hello, Bob!"),
]

# Run tests
passed = 0
failed = 0

for func, inputs, expected in tests:
    try:
        actual = func(*inputs)
        if actual == expected:
            print(f"✓ PASS: {func.__name__}{inputs} → {actual}")
            passed += 1
        else:
            print(f"✗ FAIL: {func.__name__}{inputs}")
            print(f"  Expected: {expected}")
            print(f"  Actual: {actual}")
            failed += 1
    except Exception as e:
        print(f"✗ ERROR: {func.__name__}{inputs}")
        print(f"  {type(e).__name__}: {e}")
        failed += 1

# Summary
print(f"\n{passed} passed, {failed} failed")
