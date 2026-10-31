# Lab 5: Static Code Analysis - Music Catalog

Completed from https://github.com/SETAPESU26/L5_19_music_catalog
(source main tree: 152a52e48cbbfd00fe50f51180cbbf3dec28b454).

## Contents

- `music_catalog.py`: cleaned catalog and playlist manager.
- `issues.md`: findings, original line references and fixes.
- `reflection.md`: four relevant draft answers; the handout omits the actual questions.
- `reports/before/`: original Pylint, Bandit and Flake8 output.
- `reports/after/`: final output, exit codes, demo and regression test results.
- Root `*_report.txt`: copies of final reports for easy submission.
- `original/music_catalog.py`: uncorrected baseline, retained only as evidence.
- `test_music_catalog.py`: eight regression tests.
- `requirements.txt`: exact versions used to generate the reports.

## Run on Windows CMD

Python 3.12 was used for verification. No extra dependencies are needed for the demo.

```bat
python music_catalog.py
python -m unittest -v
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
pylint music_catalog.py > pylint_report.txt
bandit -r music_catalog.py > bandit_report.txt
flake8 music_catalog.py > flake8_report.txt
```

Expected demo: `multi-song playlist`, then `popular niche 1 290` or
`popular niche 2 290`. The song ID is random. Final Pylint: 10.00/10;
Bandit: no findings; Flake8: empty output and exit code 0.

Analyze only the cleaned root script for final submission. Recursive analysis
of the entire folder includes the intentionally unsafe original baseline.
Bandit writes progress messages to stderr; these were saved separately.

Functions now use snake_case. Serialized playlists are JSON bytes, not pickle.
The catalog is intentionally in-memory, matching the starter: songs disappear
when the process ends. No student identity is embedded.

## Commit requirement

The repository history contains a baseline commit followed by three tool-specific
fix commits: Bandit/security, Pylint/correctness, and Flake8/style with
documentation and verification. All lab files are under `L5_19_music_catalog/`.
