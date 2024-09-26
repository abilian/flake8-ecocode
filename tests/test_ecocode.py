from __future__ import annotations

import ast
from textwrap import dedent

import pytest

from flake8_ecocode import EcocodePlugin as Plugin


@pytest.mark.parametrize(
    "s",
    [
        "",
        "print('hello')",
        "for var in (var2 for var2 in range(100)): ...",
    ],
)
def test_ok(s):
    run_test(s, [])


def test_ec404_bad():
    s = "for var in [var2 for var2 in range(100)]: ..."
    run_test(s, ["EC404"])


def test_c35_bad():
    s = dedent(
        """
        try:
            f = open(path)
            print(fh.read())
        except:
            print('No such file '+path)
        finally:
            f.close()
        """
    ).strip()
    run_test(s, ["EC35"])


def run_test(s: str, expected_errors: list[str]):
    errors = list(Plugin(ast.parse(s)).run())
    assert len(errors) == len(expected_errors)
    for error, expected_error in zip(errors, expected_errors):
        assert error[2].startswith(expected_error)
