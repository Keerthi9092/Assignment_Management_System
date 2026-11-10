from pathlib import Path
import csv
import random
import argparse
import json
import hashlib

from datetime import datetime, timedelta, timezone


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


def generate(out='data', seed=20261022, scale=1):

    rng = random.Random(seed)

    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)

    na = max(5, int(1000 * scale))
    nl = max(20, int(10000 * scale))
    ns = max(50, int(30000 * scale))

    d = {
        t: []
        for t in TABLES
    }

    stamp = lambda x: x.isoformat()

    start = datetime(
        2026, 2, 1,
        tzinfo=timezone.utc
    )

    def event(kind, key, action, time):
        d['audit_events'].append(
            dict(
                event_id=len(d['audit_events']) + 1,
                entity_type=kind,
                entity_id=key,
                action=action,
                event_time=stamp(time)
            )
        )

    # Generate courses

    for i, n in enumerate([
        'Programming',
        'Databases',
        'Web Development',
        'Data Structures',
        'Software Engineering'
    ], 1):

        d['courses'].append(
            dict(
                course_id=i,
                course_code=f'CSE{i:03d}',
                course_name=n,
                status='active'
            )
        )

    # Generate learners and enrollments

    for i in range(1, nl + 1):

        d['learners'].append(
            dict(
                learner_id=i,
                learner_code=f'LRN-{i:06d}',
                full_name=f'Synthetic Learner {i:05d}',
                email=f'learner{i}@example.invalid',
                status='active'
            )
        )

        for c in range(1, 6):

            d['enrollments'].append(
                dict(
                    enrollment_id=len(d['enrollments']) + 1,
                    course_id=c,
                    learner_id=i,
                    enrolled_at=stamp(
                        start - timedelta(days=10)
                    ),
                    enrollment_status='enrolled'
                )
            )

    # Generate assignments and rubrics

    for i in range(1, na + 1):

        aid = f'ASN-2026-{i:06d}'
        due = start + timedelta(days=10 + i % 40)
        rid = f'RUB-{aid}-01'

        d['assignments'].append(
            dict(
                assignment_id=aid,
                assignment_code=aid,
                course_id=(i - 1) % 5 + 1,
                title=f'{["Programming", "Database", "Web", "Algorithm", "Software"][(i - 1) % 5]} assignment {i}',
                published_at=stamp(start),
                due_at=stamp(due),
                timezone='UTC',
                max_score=100,
                status='published'
            )
        )

        d['rubrics'].append(
            dict(
                rubric_id=rid,
                assignment_id=aid,
                version_no=1,
                effective_from=stamp(start)
            )
        )

        criteria = [
            ('Correctness', 50),
            ('Quality', 30),
            ('Documentation', 20)
        ]

        for k, (name, mx) in enumerate(criteria, 1):

            d['rubric_criteria'].append(
                dict(
                    criterion_id=f'{rid}-C{k}',
                    rubric_id=rid,
                    criterion_name=name,
                    max_points=mx
                )
            )

        event(
            'assignment',
            aid,
            'PUBLISH',
            start
        )

    # Generate submissions, grades and feedback

    for i in range(ns):

        # Deterministic distinct learner/assignment pairs.
        # Attempt numbers retain uniqueness on repeated pairs.

        ai = i % na
        li = (i // na) % nl + 1
        attempt = i // (na * nl) + 1

        a = d['assignments'][ai]

        sid = (
            f'SUB-{a["assignment_id"]}'
            f'-LRN-{li:06d}-{attempt:02d}'
        )

        rid = f'RUB-{a["assignment_id"]}-01'

        missing = rng.random() < 0.04

        due = datetime.fromisoformat(a['due_at'])

        offset = rng.choice([
            -48, -24, -2, 0, 1, 12, 30
        ])

        submitted = due + timedelta(hours=offset)

        late = offset > 0

        d['submissions'].append(
            dict(
                submission_id=sid,
                submission_code=sid,
                assignment_id=a['assignment_id'],
                learner_id=li,
                attempt_no=attempt,
                submitted_at='' if missing else stamp(submitted),
                status='missing' if missing else (
                    'late' if late else 'graded'
                )
            )
        )

        if missing:
            continue

        # Submission artifacts

        d['submission_artifacts'].append(
            dict(
                artifact_id=f'ART-{i + 1:06d}',
                submission_id=sid,
                file_name=f'work_{i + 1}.pdf',
                file_size_bytes=rng.randint(1500, 120000),
                uploaded_at=stamp(submitted),
                note='Synthetic metadata; no actual file'
            )
        )

        # Calculate grades

        scores = [
            rng.randint(25, 50),
            rng.randint(15, 30),
            rng.randint(8, 20)
        ]

        total = sum(scores)

        pen = 5 if late else 0

        gid = f'GRD-{sid}'

        d['grades'].append(
            dict(
                grade_id=gid,
                submission_id=sid,
                rubric_id=rid,
                total_score=total,
                late_penalty=pen,
                final_score=max(0, total - pen),
                graded_at=stamp(
                    submitted + timedelta(days=1)
                )
            )
        )

        # Criterion scores

        for k, sc in enumerate(scores, 1):

            d['grade_criterion_scores'].append(
                dict(
                    score_id=f'{gid}-C{k}',
                    grade_id=gid,
                    criterion_id=f'{rid}-C{k}',
                    awarded_points=sc
                )
            )

        # Feedback

        d['feedback'].append(
            dict(
                feedback_id=f'FB-{i + 1:06d}',
                submission_id=sid,
                grade_id=gid,
                comments=(
                    'Strong work.'
                    if total >= 80
                    else 'Review criterion feedback and improve clarity.'
                )
            )
        )

        # Audit events

        event(
            'submission',
            sid,
            'SUBMIT',
            submitted
        )

        # Generate appeals

        if i % 60 == 0:

            d['appeals'].append(
                dict(
                    appeal_id=f'APP-2026-{len(d["appeals"]) + 1:06d}',
                    submission_id=sid,
                    learner_id=li,
                    status='pending',
                    reason='Request criterion review',
                    created_at=stamp(
                        submitted + timedelta(days=2)
                    )
                )
            )

    # CSV headers for empty tables

    headers = {
        'resubmissions': [
            'resubmission_id',
            'original_submission_id',
            'new_submission_id',
            'status'
        ]
    }

    # Export generated data into CSV files

    for t, rows in d.items():

        with (out / (t + '.csv')).open(
            'w',
            newline='',
            encoding='utf-8'
        ) as f:

            w = csv.DictWriter(
                f,
                fieldnames=(
                    list(rows[0])
                    if rows
                    else headers[t]
                )
            )

            w.writeheader()
            w.writerows(rows)

    return {
        t: len(r)
        for t, r in d.items()
    }


if __name__ == '__main__':

    p = argparse.ArgumentParser()

    p.add_argument(
        '--out',
        default='data'
    )

    p.add_argument(
        '--scale',
        type=float,
        default=1
    )

    p.add_argument(
        '--seed',
        type=int,
        default=20261022
    )

    a = p.parse_args()

    if not 0 < a.scale <= 10:
        p.error(
            'scale must be above 0 and at most 10'
        )

    print(
        json.dumps(
            generate(a.out, a.seed, a.scale),
            indent=2
        )
    )