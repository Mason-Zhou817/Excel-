from __future__ import annotations

from pathlib import Path


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def project_path(*parts: str) -> Path:
    return project_root().joinpath(*parts)


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
