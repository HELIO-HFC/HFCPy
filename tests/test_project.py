# SPDX-License-Identifier: EUPL-1.2
"""Consistency checks of the project configuration (badges, CI, metadata)."""

from __future__ import annotations

import importlib.util
import re
import tomllib
from pathlib import Path
from types import ModuleType
from urllib.parse import unquote

import pytest

ROOT = Path(__file__).parent.parent
VERSION = re.compile(r"\d+\.\d+")


def classifier_versions() -> list[str]:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
    prefix = "Programming Language :: Python :: "
    return [
        c.removeprefix(prefix)
        for c in pyproject["project"]["classifiers"]
        if c.startswith(prefix) and VERSION.fullmatch(c.removeprefix(prefix))
    ]


def test_tested_python_versions_are_consistent() -> None:
    versions = classifier_versions()
    assert versions

    github = (ROOT / ".github/workflows/ci.yml").read_text()
    match = re.search(r"python-version: \[(.*)\]", github)
    assert match, "No Python matrix in the GitHub workflow"
    assert VERSION.findall(match.group(1)) == versions

    gitlab = (ROOT / ".gitlab-ci.yml").read_text()
    match = re.search(r"PYTHON_VERSION: \[(.*)\]", gitlab)
    assert match, "No Python matrix in the GitLab pipeline"
    assert VERSION.findall(match.group(1)) == versions

    readme = (ROOT / "README.rst").read_text()
    match = re.search(r"img\.shields\.io/badge/python-(\S+)-blue", readme)
    assert match, "No Python versions badge in the README"
    assert VERSION.findall(unquote(match.group(1))) == versions


@pytest.fixture(scope="module")
def coverage_badge() -> ModuleType:
    path = ROOT / ".github/scripts/coverage_badge.py"
    spec = importlib.util.spec_from_file_location("coverage_badge", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    ("percent", "message", "color"),
    [
        (100, "100%", "brightgreen"),
        (93.4, "93%", "brightgreen"),
        (85, "85%", "green"),
        (72.6, "73%", "yellowgreen"),
        (65, "65%", "yellow"),
        (50, "50%", "orange"),
        (12, "12%", "red"),
    ],
)
def test_coverage_badge(
    coverage_badge: ModuleType, percent: float, message: str, color: str
) -> None:
    assert coverage_badge.badge(percent) == {
        "schemaVersion": 1,
        "label": "coverage",
        "message": message,
        "color": color,
    }


def test_coverage_badge_main(coverage_badge: ModuleType, tmp_path: Path) -> None:
    output = tmp_path / "coverage.json"
    coverage_badge.main(["93", str(output)])
    assert '"message": "93%"' in output.read_text()
