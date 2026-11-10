from pathlib import Path
import csv

from collections import Counter
from flask import Flask, render_template, request, abort, jsonify


app = Flask(__name__)

DATA = Path(__file__).resolve().parent / 'data'


TABLES = (
    'courses',
    'learners',
    'enrollments',
    'assignments',
    'rubrics',
    'rubric_criteria',
    'submissions',
    'submission_artifacts',
    'grades',
    'grade_criterion_scores',
    'feedback',
    'resubmissions',
    'appeals',
    'audit_events'
)


def load(name):
    p = DATA / (name + '.csv')

    if not p.exists():
        return []

    with p.open(newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


@app.context_processor
def context():
    return dict(tables=TABLES)


@app.get('/')
def dashboard():
    counts = {
        t: len(load(t))
        for t in TABLES
    }

    submissions = load('submissions')

    statuses = Counter(
        r.get('status', 'unknown')
        for r in submissions
    )

    return render_template(
        'dashboard.html',
        counts=counts,
        recent=load('assignments')[:6],
        statuses=statuses,
        total=len(submissions)
    )


@app.get('/records/<name>')
def records(name):
    if name not in TABLES:
        abort(404)

    data = load(name)

    cols = list(data[0]) if data else []

    q = request.args.get('q', '').strip()
    status = request.args.get('status', '')

    options = sorted({
        r['status']
        for r in data
        if r.get('status')
    })

    filtered = [
        r for r in data
        if (
            not q
            or q.casefold() in ' '.join(
                str(v) for v in r.values()
            ).casefold()
        )
        and (
            not status
            or r.get('status') == status
        )
    ]

    try:
        page = max(1, int(request.args.get('page', '1')))
    except ValueError:
        page = 1

    pages = max(1, (len(filtered) + 24) // 25)

    page = min(page, pages)

    return render_template(
        'records.html',
        name=name,
        columns=cols,
        rows=filtered[(page - 1) * 25:page * 25],
        q=q,
        status=status,
        options=options,
        page=page,
        pages=pages,
        count=len(filtered)
    )


@app.get('/detail/<name>/<int:index>')
def detail(name, index):
    if name not in TABLES:
        abort(404)

    data = load(name)

    if index < 1 or index > len(data):
        abort(404)

    return render_template(
        'detail.html',
        name=name,
        row=data[index - 1]
    )


@app.get('/api/<name>')
def api(name):
    if name not in TABLES:
        abort(404)

    return jsonify(load(name)[:100])


@app.errorhandler(404)
def missing(error):
    return render_template('error.html'), 404


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=False
    )