import suppress_warnings

if __name__ == "__main__":
    import pytest
    import sys
    sys.exit(pytest.main(["-v"] + sys.argv[1:]))