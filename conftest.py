from __future__ import annotations


def pytest_addoption(parser):
    parser.addoption(
        "--show_diff",
        action="store_true",
        default=False,
        help="Will show a visual comparison if a graphical unit test fails.",
    )
    parser.addoption(
        "--set_test",
        action="store_true",
        default=False,
        help="Will create the control data for EACH running test.",
    )
