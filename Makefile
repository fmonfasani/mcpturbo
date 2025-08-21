.PHONY: setup lint test bench

setup:
	pip install -e '.[dev]'
	pre-commit install

lint:
	pre-commit run --all-files

test:
	pytest

bench:
	pytest --benchmark-only
