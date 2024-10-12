from pathlib import Path


def get_tmp():
    return Path(__file__, "../tmp").resolve()
