.PHONY: env run clean format lint test check
.venv:
	uv sync --dev

env: .venv

run: env
	uv run fastapi dev expoplanner/main.py

clean:
	uv cache clean
	uv cache prune
	rm -r .venv
	rm -f tmp.db

format: env
	uv run ruff format .

lint: format
	uv run ruff check .

test:
	uv run pytest -s

check: clean lint test
