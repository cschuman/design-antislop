# This file mentions the marker string without declaring it, so it must still
# be scanned. Regression guard: the check must not be a bare substring match.
IGNORE_MARKER_TEXT = "<!-- slopcheck-ignore-file: quoted, not declared -->"


def parse(raw):
    try:
        return int(raw)
    except Exception:
        pass
