.PHONY: runserver
runserver:
	poetry run uvicorn main:app --reload

.PHONY: install
install:
	poetry install

.PHONY: flake8
flake8:
	poetry run flake8 .

.PHONY: black-check
black-check:
	poetry run black --check .  

.PHONY: black-diff
black-diff:
	poetry run black --diff .

.PHONY: black
black:
	poetry run black .

.PHONY: isort-check
isort-check:
	poetry run isort . --check-only

.PHONY: isort-diff
isort-diff:
	poetry run isort . --diff

.PHONY: isort
isort:
	poetry run isort .

.PHONY: exportreq
exportreq:
	poetry export -f requirements.txt --output requirements.txt
