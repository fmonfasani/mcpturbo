"""Generate TypeScript declaration files from Pydantic models."""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

from mcpturbo_shared_types import Message, Workflow

PACKAGE_ROOT = Path(__file__).resolve().parent.parent / "packages" / "shared-types"
TYPES_DIR = PACKAGE_ROOT / "types"
MODELS = [("message", Message), ("workflow", Workflow)]


def generate_ts() -> None:
    TYPES_DIR.mkdir(parents=True, exist_ok=True)
    for name, model in MODELS:
        schema = model.model_json_schema()
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(schema, tmp)
            tmp_path = Path(tmp.name)
        subprocess.run(
            [
                "datamodel-codegen",
                "--input",
                str(tmp_path),
                "--input-file-type",
                "jsonschema",
                "--output",
                str(TYPES_DIR / f"{name}.d.ts"),
                "--target",
                "typescript",
            ],
            check=True,
        )
        tmp_path.unlink()


if __name__ == "__main__":
    generate_ts()
