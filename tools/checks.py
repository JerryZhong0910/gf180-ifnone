# SPDX-License-Identifier: Apache-2.0
from pathlib import Path
from hashlib import sha256


class ContractError(ValueError):
    def __init__(self, code, detail=''):
        self.code = code
        super().__init__(f'{code}: {detail}')


def require(truth, code, detail=''):
    if not truth:
        raise ContractError(code, detail)


def exact(actual, expected, code):
    if actual != expected:
        raise ContractError(code, f'expected {expected!r}, got {actual!r}')


def sha(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def ref(path):
    return dict(file=Path(path).name, sha256=sha(path))
