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

## Branch coverage

From the same `Lab 6` directory:

```powershell
Write-Output 'PES1UG24AM201 - Lab 6 - Branch Coverage'
& $labPython -m coverage erase --data-file=.coverage.branch_coverage
& $labPython -m coverage run --data-file=.coverage.branch_coverage --source=parking_fee --branch -m pytest -q BranchCoverageTest_PES1UG24AM201_parking_fee.py
& $labPython -m coverage report --data-file=.coverage.branch_coverage -m --fail-under=90
& $labPython -m coverage json --data-file=.coverage.branch_coverage -o evidence/PES1UG24AM201/branch_coverage_local.json
& $labPython -c "import json; s=json.load(open('evidence/PES1UG24AM201/branch_coverage_local.json'))['files']['parking_fee.py']['summary']; p=100*s['covered_branches']/s['num_branches']; print('Branch-only coverage: {}/{} = {:.2f}%'.format(s['covered_branches'],s['num_branches'],p)); assert p >= 90"
```

Verified result: **50 passed; 34/34 statements = 100%; 24/24 branches = 100%**.
There are zero missing statements, missing branches, or partial branches.
The branch suite independently covers time boundaries (0/30/31/59/60/61/120/121),
all vehicle rates, EV truck exemption, lost-ticket interactions, slot
availability and priority, and resident/nonresident pass prices.

## Analysis and evidence

The original two starter cases covered **15/34 statements = 44.12%** and
**8/24 branches = 33.33%**. Their branch-mode terminal report displays
40% combined coverage. The terminal `Cover` column in branch mode combines
statements and branches; it is not a standalone branch percentage.

Line coverage checks which executable statements ran. Branch coverage also
checks alternative control-flow outcomes. The code suite reaches every
statement but has no exact-hour case and no supported nonresident pass
case. The separate branch suite adds those alternative outcomes and other
boundary/interaction checks.

Coverage is restricted to `parking_fee.py`, with fresh, separate data for
each suite. No application changes, coverage exclusions, mocks, or merged
suite results were used to reach the target. The exact delivered scripts
were also rerun independently from the ZIP in a fresh folder.

Verified on Windows with Python 3.12.14, pytest 9.2.0, and coverage 7.17.0.
Saved JSON and baseline reports are in `verification/`. Terminal process
output for the final suites is under `Lab 6/evidence/PES1UG24AM201/`.

## Screenshot status

**Actual terminal screenshots still need local capture.** The Markdown
placeholders and text logs are not screenshot images. Only capture results
after the >=90% target has been achieved.

Use Windows Snipping Tool (`Win+Shift+S`) after running the commands above.
Include the SRN, explicit test command, pass count, report command, and
complete coverage table. Save the actual images in
`Lab 6/evidence/PES1UG24AM201/` with these names:

- `CodeCoverage_PES1UG24AM201.png`
- `BranchCoverage_PES1UG24AM201.png`

The code screenshot must show 11 passed, 34 statements, 0 missing, 100%.
The branch screenshot must show 50 passed, 34 statements, 0 missing,
24 branches, 0 partial branches, 100%. The independent JSON check should
show 24/24 = 100.00% branch-only coverage.

After capturing them, add and commit the actual images in this personal
repository. Two separate coverage commits are already part of the upload
history; screenshots can be added in follow-up commits. The instructor
repository should not receive these changes.

From this assignment folder after capturing the images:

```powershell
git add -- 'Lab 6/evidence/PES1UG24AM201/CodeCoverage_PES1UG24AM201.png'
git commit -m "PES1UG24AM201: add code coverage terminal screenshot"
git add -- 'Lab 6/evidence/PES1UG24AM201/BranchCoverage_PES1UG24AM201.png'
git commit -m "PES1UG24AM201: add branch coverage terminal screenshot"
git push origin main
```

High coverage does not prove correctness for every possible input or
exhaustive path/condition coverage.
