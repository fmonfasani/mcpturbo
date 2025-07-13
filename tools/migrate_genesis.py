import argparse
import shutil
import datetime
from pathlib import Path

class GenesisMigrator:
    """Migrate resources from a Genesis Engine installation."""

    def __init__(self, genesis_root: Path, repo_root: Path):
        self.genesis_root = Path(genesis_root)
        self.repo_root = Path(repo_root)
        self.report_lines = []

    def _copy_tree(self, src: Path, dest: Path):
        if not src.exists():
            self.report_lines.append(f"⚠️ Source not found: {src}")
            return
        for item in src.rglob('*'):
            target = dest / item.relative_to(src)
            if item.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target)
        self.report_lines.append(f"Copied {src} -> {dest}")

    def migrate_cli_commands(self):
        src = self.genesis_root / 'packages' / 'cli' / 'genesis_cli' / 'commands'
        dest = self.repo_root / 'packages' / 'cli' / 'mcpturbo_cli' / 'commands'
        self._copy_tree(src, dest)

    def migrate_templates(self):
        src = self.genesis_root / 'packages' / 'templates' / 'genesis_templates'
        dest = self.repo_root / 'packages' / 'templates' / 'mcpturbo_templates'
        self._copy_tree(src, dest)

    def migrate_workflows(self):
        src = self.genesis_root / 'packages' / 'workflows' / 'genesis_workflows'
        dest = self.repo_root / 'packages' / 'workflows' / 'mcpturbo_workflows'
        self._copy_tree(src, dest)

    def write_report(self) -> Path:
        report_path = self.repo_root / 'MIGRATION_REPORT.md'
        with report_path.open('w', encoding='utf-8') as f:
            f.write('# Migration Report\n\n')
            f.write(f'Date: {datetime.datetime.utcnow().isoformat()}Z\n\n')
            for line in self.report_lines:
                f.write(f'- {line}\n')
        return report_path

    def run(self):
        self.migrate_cli_commands()
        self.migrate_templates()
        self.migrate_workflows()
        return self.write_report()


def main():
    parser = argparse.ArgumentParser(description='Migrate Genesis Engine resources')
    parser.add_argument('genesis_path', help='Path to Genesis Engine installation')
    parser.add_argument('--repo-root', default=Path(__file__).resolve().parents[1], help='Target repo root')
    args = parser.parse_args()

    migrator = GenesisMigrator(Path(args.genesis_path), Path(args.repo_root))
    report = migrator.run()
    print(f'Migration complete. Report written to {report}')

if __name__ == '__main__':
    main()
