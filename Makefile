PIP ?= pip3
PYTHON ?= python3
COVERAGE ?= coverage


config:
	$(PIP) install pycodestyle
	$(PIP) install coverage
	$(PIP) install -r requirements.txt


lint:
	@echo "\n==> Lint All .py Files:"
	@find app -type f -name \*.py | while read file; do pycodestyle --config=./pycodestyle --first "$$file" --format 'Code:%(code)s File:%(path)s Line:%(row)d Column:%(col)d Info:%(text)s' || exit 1; done


test:
	@echo "\n==> Run Test Cases:"
	$(PYTHON) manage.py test


coverage:
	$(COVERAGE) run --source='.' manage.py test app
	$(COVERAGE) report -m


ci: test coverage lint
	@echo "\n==> All quality checks passed"

.PHONY: ci