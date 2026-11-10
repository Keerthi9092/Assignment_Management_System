# AssignmentHub — polished Flask browsing prototype

## Run on Windows CMD
1. Extract this ZIP into a NEW folder, separate from your old project.
2. Open CMD in that folder.
3. `python -m venv venv`
4. `venv\Scripts\activate`
5. `python -m pip install -r requirements.txt`
6. `python app.py`
7. Open http://127.0.0.1:5000/
Stop with Ctrl+C. No MySQL setup is needed.

## Included
Responsive navy/purple dashboard, live CSV counts, submission breakdown, 14 entity browsing screens, search, status filtering, pagination, assignment detail screen, CSV generator, tests and bundled full-scale demo data. All assets are local. No CDN or internet needed after installing Flask.

## Data
Bundled: 1,000 assignments, 10,000 synthetic learners, 30,000 submission records. Names/emails are synthetic. Metadata does not refer to actual uploaded files. All learners are enrolled in all five courses for this simplified demo. Dates are UTC. Rubrics total 100 points; late work loses 5 points once. Missing submissions have no grade. Appeals are pending only; resubmissions table is an empty placeholder.
Regenerate: `python generator.py --scale 1 --seed 20261022`
Starter: `python generator.py --scale 0.01`
Back up edited CSVs before regenerating.

## Honest scope
This is a complete runnable FRONTEND/READ-ONLY PROTOTYPE, not the complete original business workflow. No login, roles, uploads, MySQL integration, editing, grade revisions, appeal decisions or policy-controlled resubmissions. It does not meet every original synthetic-data acceptance criterion: anomaly injection, separate ground truth and complete lifecycle validation are not provided. Do not describe it as production ready. Existing MySQL tables are not changed.

## Tests
`python -m unittest discover -s tests -v`
Python syntax and dataset checks were run when packaged. Flask runtime tests require installed dependencies; see validation/build_report.json for exact verification scope.
