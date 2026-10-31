# Static analysis reflection

The repository asks for four reflection questions, but the supplied four-page
handout does not contain their wording. The following are four relevant draft
reflection answers, not a claim that these are the missing official questions.
Review these answers and replace the prompts if your teacher supplies them.

## 1. What did each tool contribute?

Pylint identified the shared mutable default, bare exception, naming issues,
missing docstrings and unnecessary branching. Bandit identified SQL injection
risk, unsafe pickle loading, the pickle import and a random-number advisory.
Flake8 identified long lines, a bare exception, an ambiguous variable name and
multiple statements on one line. Their overlap helped cross-check findings,
while their different focuses exposed issues one tool alone could miss.

## 2. Which issues deserved priority, and why?

The medium-severity SQL and pickle findings deserved priority. SQL parameters
keep song names separate from executable SQL, including names containing quotes.
JSON decodes data without executing arbitrary serialized Python objects. The
mutable default was also significant because it silently joined playlists from
independent calls. Style fixes followed the security and correctness changes.

## 3. How were fixes verified?

The three tools were rerun against the cleaned `music_catalog.py`, without
suppressing findings. Pylint reached 10.00/10, Bandit found zero issues, and
Flake8 returned an empty report with exit code zero. Eight automated runtime
checks covered isolated and explicit playlists, hostile-looking SQL input,
empty catalogs, popularity boundaries, JSON round trips, invalid JSON playlist
structures and random ID membership. The demonstration still prints the
multi-song message, popular/niche labels, a valid random ID and 290 total plays.

## 4. What are the limitations and lessons?

A clean static-analysis result does not prove functional correctness. Empty
catalog behavior and JSON validation needed inspection and runtime checks.
Bandit's random advisory is conservative for a non-security music shuffle;
using `secrets.choice` resolves it without a suppression. JSON deliberately
supports simple playlist data rather than arbitrary Python objects, so old
pickle data cannot be loaded. Clear names, parameterized queries and focused
checks make the program easier to maintain and explain.
