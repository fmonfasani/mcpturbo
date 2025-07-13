#!/usr/bin/env python3
import argparse
import shutil
from pathlib import Path
from datetime import datetime


class GenesisMigrator:
    """Copy resources from Genesis Engine into this repo."""

    def __init__(self, genesis_path: str, repo_root: Path | None = None):
        self.genesis_path = Path(genesis_path).expanduser().resolve()
        self.repo_root = repo_root or Path(__file__).resolve().parent.parent
        self.report_lines: list[str] = []

    def _find_source(self, candidates: list[str]) -> Path | None:
        for rel in candidates:
            path = self.genesis_path / rel
            if path.exists():
                return path
        return None

    def _copy_tree(self, src: Path | None, dest: Path):
        if not src or not src.exists():
            self.report_lines.append(f"⚠️ Source not found: {src}")
            return 0
        count = 0
        for file in src.rglob('*'):
            if file.is_file():
                relative = file.relative_to(src)
                target = dest / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file, target)
                count += 1
        self.report_lines.append(f"Copied {count} files from {src} to {dest}")
        return count

    def migrate(self) -> Path:
        """Perform migration and generate report."""
        cli_src = self._find_source([
            'cli/commands',
            'packages/cli/commands'
        ])
        templates_src = self._find_source([
            'templates',
            'packages/templates'
        ])
        workflows_src = self._find_source([
            'workflows',
            'packages/workflows'
        ])

        cli_dest = self.repo_root / 'packages' / 'cli' / 'commands'
        templates_dest = self.repo_root / 'packages' / 'templates' / 'migrated'
        workflows_dest = self.repo_root / 'packages' / 'orchestrator' / 'workflows'

        cli_dest.mkdir(parents=True, exist_ok=True)
        templates_dest.mkdir(parents=True, exist_ok=True)
        workflows_dest.mkdir(parents=True, exist_ok=True)

        self.report_lines.append(f"Migration started: {datetime.utcnow().isoformat()}\n")
        self._copy_tree(cli_src, cli_dest)
        self._copy_tree(templates_src, templates_dest)
        self._copy_tree(workflows_src, workflows_dest)

        report_path = self.repo_root / 'MIGRATION_REPORT.md'
        report_content = '# Migration Report\n\n' + '\n'.join(self.report_lines)
        report_path.write_text(report_content)
        return report_path


def main() -> None:
    parser = argparse.ArgumentParser(description='Migrate Genesis Engine resources')
    parser.add_argument('genesis_path', help='Path to Genesis Engine installation')
    parser.add_argument('--repo-root', help='Repository root', default=None)
    args = parser.parse_args()

    migrator = GenesisMigrator(args.genesis_path, Path(args.repo_root) if args.repo_root else None)
    report = migrator.migrate()
    print(f'Migration finished. Report generated at {report}')


if __name__ == '__main__':
    main()
