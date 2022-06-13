install:
	pip install -e .
	pip install -r requirements.txt --upgrade
	pip install -r requirements_dev.txt --upgrade
	pre-commit install

test:
	pytest

cov:
	pytest --cov=src/pptrees

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
	doc8 doc/

update:
	pur

update2:
	pre-commit autoupdate --bleeding-edge
