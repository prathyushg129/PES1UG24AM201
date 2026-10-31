# Identified issues and fixes

Line references refer to `original/music_catalog.py`. The original source is
retained as evidence only; analyze the cleaned root file for final results.
Medium-severity security findings are listed first. No high-severity findings
were reported. All findings were fixed without disabling checks.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Bandit B608 | Security, medium | 10 | Interpolating title and artist into SQL permits injection and breaks quoted names. | Use SQLite `?` placeholders and a separate parameter tuple. |
| Bandit B301 | Security, medium | 33 | Untrusted pickle data can execute code while loading. | Replace pickle with UTF-8 JSON and validate a list of strings. Old pickle blobs are intentionally unsupported. |
| Bandit B403 | Security, low | 1 | Import of unsafe pickle serialization. | Remove pickle and import JSON. |
| Bandit B311 | Security advisory, low | 17 | Standard random generator is unsuitable for security uses. This shuffle is not security-sensitive. | Use `secrets.choice` to meet the requirement to resolve all Bandit findings. |
| Pylint W0102 | Bug | 9 | Default list is reused across independent calls. | Default to `None`, then create a fresh list; preserve explicitly supplied lists. |
| Pylint W0702 / Flake8 E722 | Reliability | 37-40 | Bare exception hides programming and database errors. | Remove blanket catch; use SQL `COALESCE` for an empty sum and allow real database errors to propagate. |
| Pylint C0114 / C0116 | Documentation | 1, 9, 15, 20, 28, 32, 36, 43 | Module and functions lack explanations. | Add module and function docstrings. |
| Pylint C0103 | Naming | 9, 15, 28, 32, 36 | Function names do not follow snake_case. | Rename functions and update every call. |
| Pylint R1705 | Maintainability | 22-25 | Else after an unconditional return adds nesting. | Return the classification directly after the unknown check. |
| Pylint C0301 / Flake8 E501 | Style | 6, 10, 21, 49 | Long lines exceed style limits. | Wrap SQL and function calls across lines. |
| Pylint C0321 / Flake8 E701 | Style | 48 | Compound statement shares one line. | Put the print statement on its own indented line. |
| Flake8 E741 | Readability | 47 | Variable `l` resembles the number one. | Use `restored_playlist`. |
| Pylint C0305 / Flake8 W391 | Style | EOF | Extra trailing blank line in analyzed baseline. | Retain exactly one terminating newline. |
| Manual inspection | Edge case | 15-17 | Choosing from an empty catalog raises an exception. | Return `None` when no IDs exist. |
| Manual inspection | Import behavior | 52 | Demo executes when imported. | Add a `__main__` guard and close the connection after the standalone demo. |

Pylint also suggested an f-string (C0209) for the original SQL expression.
Parameterized SQL resolves that finding and the injection risk together;
an f-string would retain the security issue.

## Verification

| Check | Before | After |
|---|---|---|
| Pylint | 4.29/10 | 10.00/10 |
| Bandit | 2 medium and 2 low findings | 0 findings |
| Flake8 | 8 findings | 0 findings |
| Runtime regression tests | Not part of the supplied starter | 8 passing |

Raw output and process exit codes are in `reports/before` and `reports/after`.
An empty Flake8 report with exit code 0 means no violations were found.
