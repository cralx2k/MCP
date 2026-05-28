from mcp_stdio_server import add, subtract, reverse_text


def run_smoke_tests() -> None:
    """Run basic checks for all three MCP tool functions."""
    tests = [
        ("add", add(5, 3), 8),
        ("subtract", subtract(10, 4), 6),
        ("reverse_text", reverse_text("hello"), "olleh"),
    ]

    failures = []
    for name, actual, expected in tests:
        if actual != expected:
            failures.append(f"{name}: expected {expected!r}, got {actual!r}")

    if failures:
        print("SMOKE TEST FAILED")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print("SMOKE TEST PASSED")
    for name, actual, _ in tests:
        print(f"- {name}: {actual!r}")


if __name__ == "__main__":
    run_smoke_tests()
