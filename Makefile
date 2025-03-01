.PHONY: install dev-install test lint clean

install:
	pip install .

dev-install:
	pip install -e ".[dev]"

test:
	pytest

lint:
	flake8 harness_debugger
	mypy harness_debugger

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete 