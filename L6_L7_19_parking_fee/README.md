# Lab 6: Code and Branch Coverage - PES1UG24AM201

Assignment: parking fee, parking-slot allocation, and monthly passes.

The application and original starter tests are unchanged copies of
[the instructor repository](https://github.com/SETAPESU26/L6_L7_19_parking_fee/tree/af37455c32c127506e00acc63ccd5e3309c7ce0b/Lab%206).
Original application Git blob: `d9f49287f5bc2dcc5c93b6f7c0cb44a73cf155f5`.
The instructor repository was not modified.

## Run the tests

From this `L6_L7_19_parking_fee` folder, with Python 3.x available:

```powershell
python -m venv .venv
$labPython = (Resolve-Path .\.venv\Scripts\python.exe).Path
& $labPython -m pip install -r requirements.txt
Set-Location 'Lab 6'
```

Keep this PowerShell window open. The handout-required test filenames must
be passed explicitly; a bare `pytest` command discovers only the starter file.

## Code coverage

```powershell
Write-Output 'PES1UG24AM201 - Lab 6 - Code Coverage'
& $labPython -m coverage erase --data-file=.coverage.code_coverage
& $labPython -m coverage run --data-file=.coverage.code_coverage --source=parking_fee -m pytest -q CodeCoverageTest_PES1UG24AM201_parking_fee.py
& $labPython -m coverage report --data-file=.coverage.code_coverage -m --fail-under=90
```

Verified result: **11 passed; 34/34 statements = 100%**.
The code suite retains the starter scenarios and covers every executable
statement, including validation errors, charges, discounts, slot results,
and pass pricing.

## Baseline and evidence

The original starter file passes 2 cases with 44.12% statement coverage
(15/34) and 33.33% branch coverage (8/24). Baseline JSON and process output
are stored in `verification/`. Final code coverage is measured only on
`parking_fee.py`, using fresh coverage data.

The code-coverage terminal log and an explicit screenshot placeholder are
in `Lab 6/evidence/PES1UG24AM201/`. Capture a real local terminal screenshot
showing the SRN, test command, 11 passed, and the 100% report; save it as
`CodeCoverage_PES1UG24AM201.png` in that evidence folder. The text log does
not replace a screenshot. Branch coverage is delivered in the next commit.
