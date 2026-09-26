"""
analyzer/advice.py

Rule-based advice database for known Python errors.

Each entry maps an exception name to an ErrorAdvice object containing:
  - explanation : plain-English description of what the error means
  - root_cause  : the most likely reason it occurred
  - steps       : ordered list of fix steps (strings)
  - example_fix : a short before/after code snippet string

Design note: this module is intentionally self-contained and has no
Streamlit or I/O dependencies, making it straightforward to swap the
rule-based content for AI-generated advice in a later milestone.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ErrorAdvice:
    explanation: str
    root_cause: str
    steps: list[str]
    example_fix: str


# ---------------------------------------------------------------------------
# Advice database — add / edit entries here; keys must match exception names
# in analyzer/detector.py exactly.
# ---------------------------------------------------------------------------
ADVICE: dict[str, ErrorAdvice] = {

    "ModuleNotFoundError": ErrorAdvice(
        explanation=(
            "Python cannot locate a module you are trying to import. "
            "This usually means the package is not installed in the current environment, "
            "or the module name is misspelled."
        ),
        root_cause=(
            "The package is missing from the active virtual environment, "
            "or the import statement contains a typo."
        ),
        steps=[
            "Check the exact package name on PyPI (it may differ from the import name, "
            "e.g. `pip install Pillow` but `import PIL`).",
            "Install the missing package: `pip install <package-name>`.",
            "Confirm you are using the correct virtual environment: `which python` / `where python`.",
            "If the module is a local file, ensure it is on `sys.path` or in the same directory.",
        ],
        example_fix=(
            "# Before (raises ModuleNotFoundError)\n"
            "import pandas\n\n"
            "# Fix — install first, then import\n"
            "# $ pip install pandas\n"
            "import pandas as pd"
        ),
    ),

    "ImportError": ErrorAdvice(
        explanation=(
            "The module exists and can be found, but Python could not import "
            "a specific name or attribute from it."
        ),
        root_cause=(
            "The name being imported does not exist in the module, "
            "the module has a circular import, or a C extension failed to load."
        ),
        steps=[
            "Verify the exported name exists: open the module or check its `__all__`.",
            "Check for circular imports between your modules.",
            "Ensure compiled extensions (`.pyd` / `.so`) are built for the current Python version.",
            "Update or reinstall the package if it may be corrupt: `pip install --force-reinstall <pkg>`.",
        ],
        example_fix=(
            "# Before (raises ImportError)\n"
            "from os.path import doesnt_exist\n\n"
            "# Fix — import what actually exists\n"
            "from os.path import join, exists"
        ),
    ),

    "NameError": ErrorAdvice(
        explanation=(
            "Python encountered a name (variable, function, or class) that has not been "
            "defined in the current scope at the point where it is used."
        ),
        root_cause=(
            "The variable was never assigned, is defined after it is used, "
            "or is misspelled."
        ),
        steps=[
            "Check the spelling of the variable name — Python is case-sensitive.",
            "Make sure the variable is assigned before the line that uses it.",
            "If the name comes from an import, add the missing `import` statement.",
            "Check that the variable is not defined inside an `if` block that may not have run.",
        ],
        example_fix=(
            "# Before (raises NameError)\n"
            "print(total)\n\n"
            "# Fix — define before use\n"
            "total = 0\n"
            "print(total)"
        ),
    ),

    "UnboundLocalError": ErrorAdvice(
        explanation=(
            "A local variable is referenced inside a function before it has been assigned "
            "a value. Python decides a variable is local if it is assigned anywhere in the "
            "function, even after the reference."
        ),
        root_cause=(
            "A variable with the same name exists in an outer scope, but an assignment "
            "inside the function makes Python treat it as local — creating a reference "
            "before the assignment."
        ),
        steps=[
            "Move the assignment above the first use of the variable.",
            "If you intend to use an outer-scope variable, declare it with `global` or `nonlocal`.",
            "Consider passing the value as a function argument instead of relying on closures.",
        ],
        example_fix=(
            "# Before (raises UnboundLocalError)\n"
            "x = 10\n"
            "def update():\n"
            "    print(x)   # UnboundLocalError — x is assigned below\n"
            "    x = 20\n\n"
            "# Fix — use global or reorder\n"
            "def update():\n"
            "    global x\n"
            "    print(x)\n"
            "    x = 20"
        ),
    ),

    "TypeError": ErrorAdvice(
        explanation=(
            "An operation or function was applied to an object of an inappropriate type. "
            "For example, trying to add a string and an integer, or calling a non-callable."
        ),
        root_cause=(
            "A variable holds a different type than expected — often `None` is returned "
            "from a function when a value was expected, or user input was not converted."
        ),
        steps=[
            "Print or log `type(variable)` to inspect the actual type at runtime.",
            "Convert the value to the expected type explicitly (e.g. `int(x)`, `str(y)`).",
            "Check that functions return a value and do not accidentally return `None`.",
            "Review function signatures to ensure callers pass the correct number of arguments.",
        ],
        example_fix=(
            "# Before (raises TypeError)\n"
            "age = input('Enter age: ')   # input() returns str\n"
            "print(age + 1)\n\n"
            "# Fix — convert to int\n"
            "age = int(input('Enter age: '))\n"
            "print(age + 1)"
        ),
    ),

    "ValueError": ErrorAdvice(
        explanation=(
            "A function received an argument of the correct type but with an "
            "unacceptable value — for example, converting a non-numeric string to int, "
            "or unpacking the wrong number of items."
        ),
        root_cause=(
            "Unexpected or malformed input data that does not satisfy the function's "
            "value constraints."
        ),
        steps=[
            "Validate input before passing it to functions (e.g. check `s.isdigit()` before `int(s)`).",
            "Use `try / except ValueError` to handle bad input gracefully.",
            "When unpacking, confirm the iterable has exactly the expected number of items.",
            "Log the actual value that caused the error to understand the data problem.",
        ],
        example_fix=(
            "# Before (raises ValueError)\n"
            "number = int('abc')\n\n"
            "# Fix — validate first\n"
            "raw = 'abc'\n"
            "if raw.lstrip('-').isdigit():\n"
            "    number = int(raw)\n"
            "else:\n"
            "    number = 0   # or raise a descriptive error"
        ),
    ),

    "IndexError": ErrorAdvice(
        explanation=(
            "A sequence (list, tuple, string) was accessed with an index that is outside "
            "its valid range. Valid indices are `0` to `len(seq) - 1`, or `-len(seq)` to `-1`."
        ),
        root_cause=(
            "The list is shorter than expected, an off-by-one error in a loop, "
            "or the list is empty."
        ),
        steps=[
            "Check the list length before indexing: `if index < len(my_list):`.",
            "Use `enumerate()` in loops to avoid manual index arithmetic.",
            "Guard against empty lists: `if my_list:` before accessing elements.",
            "Consider using `.get()` on dicts (not applicable to lists) or slicing with defaults.",
        ],
        example_fix=(
            "# Before (raises IndexError)\n"
            "items = [1, 2, 3]\n"
            "print(items[5])\n\n"
            "# Fix — guard with length check\n"
            "idx = 5\n"
            "if idx < len(items):\n"
            "    print(items[idx])\n"
            "else:\n"
            "    print('Index out of range')"
        ),
    ),

    "KeyError": ErrorAdvice(
        explanation=(
            "A dictionary lookup used a key that does not exist in the dictionary."
        ),
        root_cause=(
            "The key was never added to the dict, the data source returned unexpected "
            "keys, or there is a typo in the key name."
        ),
        steps=[
            "Use `dict.get(key, default)` to return a default instead of raising.",
            "Check membership before access: `if key in my_dict:`.",
            "Print `my_dict.keys()` to inspect available keys at runtime.",
            "When parsing external data (JSON, API), validate expected keys exist first.",
        ],
        example_fix=(
            "# Before (raises KeyError)\n"
            "data = {'name': 'Alice'}\n"
            "print(data['age'])\n\n"
            "# Fix — use .get() with a default\n"
            "print(data.get('age', 'unknown'))"
        ),
    ),

    "AttributeError": ErrorAdvice(
        explanation=(
            "An attribute or method was accessed on an object that does not have it. "
            "A very common variant is accessing an attribute on `None`."
        ),
        root_cause=(
            "The object is `None` (a function returned nothing), the wrong type was passed, "
            "or there is a typo in the attribute name."
        ),
        steps=[
            "Add a `None` guard: `if obj is not None:` before accessing attributes.",
            "Use `hasattr(obj, 'attr_name')` to check existence at runtime.",
            "Check that the function or method actually returns the expected object.",
            "Verify spelling — attribute names are case-sensitive.",
        ],
        example_fix=(
            "# Before (raises AttributeError)\n"
            "result = some_function()   # returns None on failure\n"
            "print(result.name)\n\n"
            "# Fix — guard against None\n"
            "result = some_function()\n"
            "if result is not None:\n"
            "    print(result.name)\n"
            "else:\n"
            "    print('No result returned')"
        ),
    ),

    "SyntaxError": ErrorAdvice(
        explanation=(
            "Python's parser could not understand the source code. "
            "The file will not run at all until the syntax is fixed."
        ),
        root_cause=(
            "Missing colon after `if`/`for`/`def`, unmatched brackets or quotes, "
            "incorrect indentation, or use of a Python 2 construct in Python 3."
        ),
        steps=[
            "Look at the line number reported in the traceback — the actual mistake is "
            "often one line earlier.",
            "Check for mismatched parentheses, brackets, or quotes.",
            "Ensure every `if`, `for`, `while`, `def`, `class` ends with a colon `:`.",
            "Run `python -m py_compile your_file.py` to catch syntax errors without executing.",
        ],
        example_fix=(
            "# Before (SyntaxError — missing colon)\n"
            "if x > 0\n"
            "    print(x)\n\n"
            "# Fix\n"
            "if x > 0:\n"
            "    print(x)"
        ),
    ),

    "IndentationError": ErrorAdvice(
        explanation=(
            "Python requires consistent indentation to define code blocks. "
            "Mixing tabs and spaces, or inconsistent indent levels, causes this error."
        ),
        root_cause=(
            "Mixed tabs and spaces, copy-pasted code with different indentation, "
            "or a block that is accidentally un-indented."
        ),
        steps=[
            "Configure your editor to use spaces only (4 spaces per level is standard).",
            "Run `python -tt your_file.py` to flag tab/space mixing.",
            "Re-indent the offending block — don't just add spaces by eye.",
            "Use an auto-formatter like `ruff format` or `black` to fix indentation project-wide.",
        ],
        example_fix=(
            "# Before (IndentationError — mixed tabs/spaces)\n"
            "def greet():\n"
            "    print('Hello')  # spaces\n"
            "\tprint('World')   # tab\n\n"
            "# Fix — use spaces consistently\n"
            "def greet():\n"
            "    print('Hello')\n"
            "    print('World')"
        ),
    ),

    "FileNotFoundError": ErrorAdvice(
        explanation=(
            "Python tried to open or access a file or directory that does not exist "
            "at the given path."
        ),
        root_cause=(
            "The path is wrong (relative vs absolute), the file was deleted, "
            "or the working directory is not what you expect."
        ),
        steps=[
            "Print `os.getcwd()` to confirm the working directory.",
            "Use `os.path.exists(path)` to check before opening.",
            "Prefer `pathlib.Path` for cross-platform path handling.",
            "Use absolute paths or `__file__` relative paths in scripts.",
        ],
        example_fix=(
            "# Before (raises FileNotFoundError)\n"
            "with open('data.csv') as f:\n"
            "    content = f.read()\n\n"
            "# Fix — check existence first\n"
            "from pathlib import Path\n"
            "p = Path('data.csv')\n"
            "if p.exists():\n"
            "    content = p.read_text()\n"
            "else:\n"
            "    raise FileNotFoundError(f'File not found: {p.resolve()}')"
        ),
    ),

    "ZeroDivisionError": ErrorAdvice(
        explanation=(
            "The code attempted to divide a number by zero, which is mathematically undefined."
        ),
        root_cause=(
            "A divisor variable is zero due to empty data, a calculation bug, "
            "or unvalidated user input."
        ),
        steps=[
            "Add a guard: `if denominator != 0:` before dividing.",
            "Return a sensible default (e.g. `0` or `float('inf')`) when the denominator is zero.",
            "Trace back why the denominator is zero — the real bug is usually upstream.",
        ],
        example_fix=(
            "# Before (raises ZeroDivisionError)\n"
            "result = total / count\n\n"
            "# Fix — guard against zero\n"
            "result = total / count if count != 0 else 0"
        ),
    ),

    "RecursionError": ErrorAdvice(
        explanation=(
            "The call stack exceeded Python's recursion limit (default 1000). "
            "A function called itself too many times without reaching a base case."
        ),
        root_cause=(
            "Missing or unreachable base case in a recursive function, "
            "or accidentally infinite mutual recursion."
        ),
        steps=[
            "Verify the base case is correct and reachable for all inputs.",
            "Add a print/log to trace the recursion depth during debugging.",
            "Consider rewriting deep recursion as an iterative loop.",
            "As a last resort, increase the limit: `sys.setrecursionlimit(2000)` — but fix the root cause first.",
        ],
        example_fix=(
            "# Before (infinite recursion — missing base case)\n"
            "def factorial(n):\n"
            "    return n * factorial(n - 1)\n\n"
            "# Fix — add base case\n"
            "def factorial(n):\n"
            "    if n <= 1:\n"
            "        return 1\n"
            "    return n * factorial(n - 1)"
        ),
    ),

    "PermissionError": ErrorAdvice(
        explanation=(
            "The operating system denied access to a file or resource "
            "because the process lacks the required permissions."
        ),
        root_cause=(
            "The file is owned by another user, is read-only, or the process "
            "is not running with sufficient privileges."
        ),
        steps=[
            "Check file permissions: `ls -l file` (Linux/Mac) or Properties → Security (Windows).",
            "Run the script with elevated privileges only if absolutely necessary.",
            "Ensure no other process has the file locked.",
            "Write to a directory you own (e.g. the user's home directory) instead.",
        ],
        example_fix=(
            "# Before (raises PermissionError)\n"
            "with open('/etc/hosts', 'w') as f:\n"
            "    f.write('...')\n\n"
            "# Fix — write to a user-writable path\n"
            "from pathlib import Path\n"
            "dest = Path.home() / 'output.txt'\n"
            "dest.write_text('...')"
        ),
    ),

    "RuntimeError": ErrorAdvice(
        explanation=(
            "A generic error that does not fit any more-specific category. "
            "Typically raised explicitly by library code to signal an invalid state."
        ),
        root_cause=(
            "Library or framework code detected an inconsistent or unexpected program state. "
            "The full traceback message is the key clue."
        ),
        steps=[
            "Read the full error message carefully — it often explains the specific issue.",
            "Search the traceback for the first frame inside your own code.",
            "Check the library's documentation or GitHub issues for known causes.",
            "Ensure you are not calling async code from a synchronous context (common in web frameworks).",
        ],
        example_fix=(
            "# RuntimeError messages vary widely — read the traceback message.\n"
            "# Common pattern: async called from sync\n\n"
            "# Before\n"
            "import asyncio\n"
            "async def fetch(): ...\n"
            "fetch()  # RuntimeError: coroutine was never awaited\n\n"
            "# Fix\n"
            "asyncio.run(fetch())"
        ),
    ),

    "NotImplementedError": ErrorAdvice(
        explanation=(
            "A method or function stub was called but has not been implemented yet. "
            "It is intentionally raised to signal that a subclass must override it."
        ),
        root_cause=(
            "An abstract base class method was called on the base class directly, "
            "or a subclass forgot to implement a required method."
        ),
        steps=[
            "Identify the class and method in the traceback.",
            "Implement the method in your subclass.",
            "If it is an ABC, ensure your class inherits from it and overrides all abstract methods.",
            "Use `abc.ABC` and `@abstractmethod` to enforce implementation at class-definition time.",
        ],
        example_fix=(
            "# Before (raises NotImplementedError)\n"
            "class Base:\n"
            "    def process(self):\n"
            "        raise NotImplementedError\n\n"
            "obj = Base()\n"
            "obj.process()\n\n"
            "# Fix — implement in subclass\n"
            "class Concrete(Base):\n"
            "    def process(self):\n"
            "        return 'done'"
        ),
    ),

    "AssertionError": ErrorAdvice(
        explanation=(
            "An `assert` statement evaluated to `False`. "
            "Assertions are used to verify assumptions during development."
        ),
        root_cause=(
            "A precondition or invariant in the code is violated — "
            "the actual value did not match the expected value."
        ),
        steps=[
            "Read the assertion message (if any) for clues about what was expected.",
            "Add a descriptive message: `assert condition, 'Expected X but got Y'`.",
            "Trace the value that failed the assertion back to where it was set.",
            "Do not use assertions for input validation in production — use `if / raise` instead.",
        ],
        example_fix=(
            "# Before (AssertionError with no message)\n"
            "assert len(results) > 0\n\n"
            "# Fix — add a descriptive message\n"
            "assert len(results) > 0, f'Expected results but got empty list. Query: {query}'"
        ),
    ),

    "ConnectionError": ErrorAdvice(
        explanation=(
            "A network connection could not be established to a remote host."
        ),
        root_cause=(
            "The remote server is down, the URL/host is wrong, "
            "there is no internet connection, or a firewall is blocking the request."
        ),
        steps=[
            "Verify the URL and port are correct.",
            "Test connectivity: `ping <host>` or `curl <url>` from the terminal.",
            "Wrap the call in a `try / except` and implement retry logic with back-off.",
            "Check firewall or proxy settings if running in a corporate environment.",
        ],
        example_fix=(
            "# Before (may raise ConnectionError)\n"
            "import requests\n"
            "r = requests.get('https://api.example.com/data')\n\n"
            "# Fix — handle network errors gracefully\n"
            "import requests\n"
            "try:\n"
            "    r = requests.get('https://api.example.com/data', timeout=10)\n"
            "    r.raise_for_status()\n"
            "except requests.exceptions.ConnectionError as e:\n"
            "    print(f'Connection failed: {e}')"
        ),
    ),

    "TimeoutError": ErrorAdvice(
        explanation=(
            "An operation took longer than the allotted time and was cancelled."
        ),
        root_cause=(
            "Slow network, overloaded server, or no timeout was set and "
            "the operation waited indefinitely."
        ),
        steps=[
            "Always set explicit timeouts on network and I/O calls.",
            "Increase the timeout if the operation is legitimately slow.",
            "Add retry logic with exponential back-off.",
            "Investigate server-side performance if timeouts are frequent.",
        ],
        example_fix=(
            "# Before (no timeout — hangs indefinitely)\n"
            "import requests\n"
            "r = requests.get('https://slow-api.example.com')\n\n"
            "# Fix — set a timeout\n"
            "r = requests.get('https://slow-api.example.com', timeout=30)"
        ),
    ),

    "OSError": ErrorAdvice(
        explanation=(
            "A system-level error occurred, typically related to file I/O, "
            "process management, or operating-system resources. "
            "`FileNotFoundError` and `PermissionError` are subclasses."
        ),
        root_cause=(
            "The OS rejected the operation due to a missing file, permissions issue, "
            "full disk, or unavailable device."
        ),
        steps=[
            "Check `errno` or the error message for the specific OS code.",
            "Verify the path exists and is accessible.",
            "Ensure there is sufficient disk space.",
            "Catch the specific subclass (`FileNotFoundError`, `PermissionError`) when possible.",
        ],
        example_fix=(
            "# Generic OSError handling\n"
            "try:\n"
            "    with open('file.txt') as f:\n"
            "        data = f.read()\n"
            "except FileNotFoundError:\n"
            "    print('File not found')\n"
            "except PermissionError:\n"
            "    print('Access denied')\n"
            "except OSError as e:\n"
            "    print(f'OS error: {e}')"
        ),
    ),

    "MemoryError": ErrorAdvice(
        explanation=(
            "The Python process ran out of available RAM and could not allocate more."
        ),
        root_cause=(
            "Loading an excessively large dataset into memory at once, "
            "a memory leak, or insufficient RAM for the workload."
        ),
        steps=[
            "Process large files in chunks / streams instead of loading them whole.",
            "Use generators instead of materialising large lists.",
            "Profile memory usage with `tracemalloc` or `memory_profiler`.",
            "Consider using `numpy` or `pandas` with chunking for large datasets.",
        ],
        example_fix=(
            "# Before (loads entire file into RAM)\n"
            "with open('huge.csv') as f:\n"
            "    lines = f.readlines()\n\n"
            "# Fix — iterate line by line\n"
            "with open('huge.csv') as f:\n"
            "    for line in f:\n"
            "        process(line)"
        ),
    ),

    "StopIteration": ErrorAdvice(
        explanation=(
            "An iterator has been exhausted and `next()` was called on it "
            "outside of a loop or generator context."
        ),
        root_cause=(
            "Manually calling `next()` without a default, or a generator "
            "function returning early, causing a `StopIteration` that "
            "propagates unexpectedly."
        ),
        steps=[
            "Use `next(iterator, default)` to supply a fallback instead of raising.",
            "Use a `for` loop instead of manual `next()` calls.",
            "In generators, ensure `return` (not `raise StopIteration`) is used to exit.",
        ],
        example_fix=(
            "# Before (raises StopIteration)\n"
            "it = iter([1, 2, 3])\n"
            "while True:\n"
            "    val = next(it)   # raises when exhausted\n\n"
            "# Fix — use default sentinel\n"
            "it = iter([1, 2, 3])\n"
            "_DONE = object()\n"
            "while (val := next(it, _DONE)) is not _DONE:\n"
            "    print(val)"
        ),
    ),

    "OverflowError": ErrorAdvice(
        explanation=(
            "A numeric calculation produced a result too large to be represented "
            "by the float type (Python ints are arbitrary precision and rarely overflow)."
        ),
        root_cause=(
            "Very large exponentiation or math operations on `float` values, "
            "often in scientific or financial calculations."
        ),
        steps=[
            "Use Python's arbitrary-precision `int` arithmetic instead of `float` where possible.",
            "Use the `decimal` module for high-precision decimal arithmetic.",
            "Check for runaway loops or recursive calculations producing huge numbers.",
        ],
        example_fix=(
            "# Before (OverflowError with float)\n"
            "import math\n"
            "print(math.exp(1000))  # float overflow\n\n"
            "# Fix — use Decimal for large values\n"
            "from decimal import Decimal\n"
            "import decimal\n"
            "decimal.getcontext().prec = 50\n"
            "print(Decimal(1000).exp())"
        ),
    ),

    "IOError": ErrorAdvice(
        explanation=(
            "An alias for `OSError` in Python 3. Indicates a file I/O or OS-level failure."
        ),
        root_cause="See OSError — the cause is the same.",
        steps=[
            "Treat identically to `OSError`.",
            "Catch `OSError` (which covers `IOError`) in new code.",
        ],
        example_fix=(
            "# IOError is an alias for OSError in Python 3\n"
            "try:\n"
            "    with open('missing.txt') as f:\n"
            "        data = f.read()\n"
            "except OSError as e:\n"
            "    print(f'I/O error: {e}')"
        ),
    ),

    # Fallback for any error not in the catalogue above
    "Exception": ErrorAdvice(
        explanation=(
            "A generic Python exception was raised. "
            "This is the base class for most built-in exceptions."
        ),
        root_cause=(
            "See the full error message and traceback for the specific cause."
        ),
        steps=[
            "Read the complete traceback to find the line that raised the error.",
            "Search for the specific exception class name for targeted advice.",
            "Add logging to capture the error context in production.",
        ],
        example_fix=(
            "# Always catch specific exceptions when possible\n"
            "try:\n"
            "    risky_operation()\n"
            "except ValueError as e:\n"
            "    handle_value_error(e)\n"
            "except TypeError as e:\n"
            "    handle_type_error(e)\n"
            "except Exception as e:\n"
            "    log_unexpected_error(e)\n"
            "    raise"
        ),
    ),
}


def get_advice(error_name: str) -> ErrorAdvice | None:
    """
    Return advice for *error_name*, or None if not in the catalogue.

    This is the single function AI integration will override in a later milestone:
    replace the dict lookup with an LLM call while keeping the same return type.
    """
    return ADVICE.get(error_name)
