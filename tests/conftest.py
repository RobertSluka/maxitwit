# conftest.py is a local plugin for pytest, a testing framework for Python. It's used to define setup methods that are common to multiple test files.

def pytest_addoption(parser):
    parser.addoption(
        "--force", action="store_true", default=False, help="Skip warning question"
    )
    parser.addoption(
        "--container",
        action="store_true",
        default=False,
        help="Run tests in a container",
    )