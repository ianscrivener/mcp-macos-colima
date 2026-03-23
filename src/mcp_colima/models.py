from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class CommandResponse(BaseModel):
    error: bool = False
    command: list[str]
    exit_code: int = 0
    stdout: str = ""
    stderr: str = ""
    data: Any | None = None
    message: str | None = None
