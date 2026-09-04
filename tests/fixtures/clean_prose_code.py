"""Ordinary identifiers that a case-blind abbreviation rule used to flag.

Regression guard. slopcheck compiles every pattern with re.IGNORECASE, which
silently defeats a pattern that means to be case-sensitive. This file is full
of plain words containing the letters "id", "api" and so on, and must stay
clean. See the case-sensitivity test in run_tests.py.
"""

CONFIDENCE_FLOOR = 0.75


def rank_candidates(candidates, gauge_readings):
    """Order candidates by confidence, discarding anything under the floor."""
    accepted = []
    for candidate in candidates:
        confidence = candidate.score / max(len(gauge_readings), 1)
        if confidence < CONFIDENCE_FLOOR:
            continue
        accepted.append((confidence, candidate))
    accepted.sort(key=lambda pair: pair[0], reverse=True)
    return [candidate for _, candidate in accepted]


def validates(reading):
    """A reading validates when it is inside the gauge's rated range."""
    return 0.0 <= reading.inches <= reading.gauge.rated_maximum
