import subprocess
import sys
import os
from pathlib import Path


def test_genesis_cli_entry():
    script = Path(__file__).resolve().parents[1] / "mcpturbo_cli" / "main.py"
    env = dict(os.environ)
    root = Path(__file__).resolve().parents[3]
    env["PYTHONPATH"] = f"{root}/packages/agents:{root}"
    result = subprocess.run([sys.executable, str(script), "genesis"], capture_output=True, text=True, env=env)
    assert result.returncode == 0
    assert "Genesis agent registered" in result.stdout
