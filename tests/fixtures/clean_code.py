import logging


def load(path):
    """Return the file's contents, or None when it is missing."""
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        logging.warning("no such file: %s", path)
        return None
