
#!/usr/bin/env python3
import argparse
from pathlib import Path
from datetime import datetime


class MigrationValidator:
    """Validate migrated packages and agents."""

    def __init__(self, repo_root: Path | None = None):
        self.repo_root = repo_root or Path(__file__).resolve().parent.parent
        self.report_lines: list[str] = []

    def _log(self, message: str):
        self.report_lines.append(message)

    def validate_imports(self):
        packages = [
            "mcpturbo_cli",
            "mcpturbo_templates",
            "mcpturbo_generators",
            "mcpturbo_agents",
            "mcpturbo_core",
            "mcpturbo_orchestrator",
        ]
        for pkg in packages:
            try:
                __import__(pkg)
                self._log(f"✅ Imported {pkg}")
            except Exception as exc:
                self._log(f"❌ Failed to import {pkg}: {exc}")

    def validate_agents(self):
        try:
            from mcpturbo_agents.base_agent import LocalAgent
            from mcpturbo_agents.registry import AgentRegistry

            agent = LocalAgent("validator", "ValidationAgent")
            registry = AgentRegistry()
            registry.register(agent)

            if registry.get("validator"):
                self._log("✅ Agent registry operational")
            else:
                self._log("❌ Agent registry failed to register agent")
        except Exception as exc:
            self._log(f"❌ Agent validation failed: {exc}")

    def run(self) -> Path:
        self._log(f"Validation started: {datetime.utcnow().isoformat()}\n")
        self.validate_imports()
        self.validate_agents()
        report_path = self.repo_root / "VALIDATION_REPORT.md"
        report_path.write_text("# Validation Report\n\n" + "\n".join(self.report_lines))
        return report_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate migrated packages")
    parser.add_argument("--repo-root", help="Repository root", default=None)
    args = parser.parse_args()
    validator = MigrationValidator(Path(args.repo_root) if args.repo_root else None)
    report = validator.run()
    print(f"Validation finished. Report generated at {report}")


if __name__ == "__main__":

    main()
