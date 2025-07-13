
import argparse
import importlib
import sys
import datetime
from pathlib import Path

class MigrationValidator:
    """Validate migrated packages and basic agent initialization."""

    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.report_lines = []

    def _import_package(self, pkg_dir: Path):
        name = f"mcpturbo_{pkg_dir.name}"
        module_path = pkg_dir / name
        if not module_path.exists():
            self.report_lines.append(f"⚠️ Package {name} not found")
            return
        sys.path.insert(0, str(pkg_dir))
        try:
            importlib.import_module(name)
            self.report_lines.append(f"Imported {name}")
        except Exception as e:
            self.report_lines.append(f"Failed to import {name}: {e}")
        finally:
            if str(pkg_dir) in sys.path:
                sys.path.remove(str(pkg_dir))

    def load_packages(self):
        packages_dir = self.repo_root / 'packages'
        for pkg in packages_dir.iterdir():
            if pkg.is_dir():
                self._import_package(pkg)

    def init_agents(self):
        sys.path.insert(0, str(self.repo_root / 'packages' / 'agents'))
        try:
            from mcpturbo_agents import create_simple_agent, registry
            agent = create_simple_agent('validation-agent')
            self.report_lines.append('Created agent: validation-agent')
            if registry.exists('validation-agent'):
                self.report_lines.append('Agent registry operational')
        except Exception as e:
            self.report_lines.append(f'Agent initialization failed: {e}')
        finally:
            path = str(self.repo_root / 'packages' / 'agents')
            if path in sys.path:
                sys.path.remove(path)

    def write_report(self) -> Path:
        report_path = self.repo_root / 'VALIDATION_REPORT.md'
        with report_path.open('w', encoding='utf-8') as f:
            f.write('# Validation Report\n\n')
            f.write(f'Date: {datetime.datetime.utcnow().isoformat()}Z\n\n')
            for line in self.report_lines:
                f.write(f'- {line}\n')
        return report_path

    def run(self):
        self.load_packages()
        self.init_agents()
        return self.write_report()


def main():
    parser = argparse.ArgumentParser(description='Validate migrated MCPturbo packages')
    parser.add_argument('--repo-root', default=Path(__file__).resolve().parents[1], help='Root of repository to validate')
    args = parser.parse_args()

    validator = MigrationValidator(Path(args.repo_root))
    report = validator.run()
    print(f'Validation complete. Report written to {report}')

if __name__ == '__main__':

    main()
