# Tests Directory

This directory contains tests for the HR System API.

## Note on Python 3.10+ Features

The test file `test_employee_features.py` intentionally uses Python 3.10+ features (specifically the `match`/`case` structural pattern matching syntax) to demonstrate failing CI runs on older Python versions.

### Expected CI Behavior:
- **Python 3.9**: Tests will fail with a `SyntaxError` due to the match/case syntax
- **Python 3.10+**: Tests will pass successfully

This is intentional and serves as a demonstration for the GitHub MCP server to identify PRs with failing CI checks.
