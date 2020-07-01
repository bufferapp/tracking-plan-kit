.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo -e "Usage: \tmake [TARGET]\n"
	@echo -e "Targets:"
	@echo -e "  init            Initialize the Python enviroment, make sure to run this before using other make commands."
	@echo -e "  test            Runs the suite of unit tests."



.PHONY: init
init:
	@pipenv --three install --dev

.PHONY: test
 test:
	@export PIPENV_VERBOSITY=-1 && pipenv run pytest