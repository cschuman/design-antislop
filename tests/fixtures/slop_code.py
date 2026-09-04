# Deliberate slop. Used by the test suite. Do not "fix" this file.
def load(path):
    try:
        return open(path).read()
    except Exception:
        pass
