bootstrap:
	test -s ./pyproject.toml || { poetry config virtualenvs.in-project true --local; poetry init --no-interaction; }
	rm -rf .venv
	poetry install --no-root

test_all:
	./.venv/bin/coverage run -m pytest -v -s tests

show_coverage:
	./.venv/bin/coverage report -m tests/test_class_books_collector.py