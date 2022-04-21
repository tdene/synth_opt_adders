install:
	pip install -e .
	pre-commit install

test:
	pytest

cov:
	pytest --cov= pptrees

mypy:
	mypy . --ignore-missing-imports

lint:
	flake8

pylint:
	pylint pptrees

lintd2:
	flake8 --select RST

lintd:
	pydocstyle pptrees

doc8:
	doc8 docs/

update:
	pur

update2:
	pre-commit autoupdate --bleeding-edge
