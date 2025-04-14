SHELL := /bin/bash

VENV = .venv
PYTHON = $(VENV)/bin/python
MAIN = main.py

banner:
	@echo "  ██████████   █████████  ███████████ ██████   ██████"
	@echo " ░░███░░░░░█  ███░░░░░███░░███░░░░░░█░░██████ ██████ "
	@echo "  ░███  █ ░  ███     ░░░  ░███   █ ░  ░███░█████░███ "
	@echo "  ░██████   ░███          ░███████    ░███░░███ ░███ "
	@echo "  ░███░░█   ░███          ░███░░░█    ░███ ░░░  ░███ "
	@echo "  ░███ ░   █░░███     ███ ░███  ░     ░███      ░███ "
	@echo " ██████████ ░░█████████  █████       █████     ██████"
	@echo "░░░░░░░░░░   ░░░░░░░░░  ░░░░░       ░░░░░     ░░░░░  "

create:
	python3 -m venv .venv

run:
	@echo "Ejecutando simulación..."
	@source $(VENV)/bin/activate && \
	$(PYTHON) $(MAIN)

install:
	.venv/bin/pip install -r requirements.txt

typecheck:
	mypy main.py
	mypy processing/

test:
	python -m unittest discover -s tests

build: banner create install run 
