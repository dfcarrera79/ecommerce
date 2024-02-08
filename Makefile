.PHONY: install
install:
	poetry install

.PHONY: run-server
run-server:
	poetry run python src/main.py 

.PHONY: run-dev
run-dev:
	poetry run uvicorn src.main:app --reload	

.PHONY: update
update: install
