PYTHON ?= python3

.PHONY: all slides notes script metadata check

all:
	$(PYTHON) build_script.py --target all
	$(PYTHON) update_metadata.py

slides:
	$(PYTHON) build_script.py --target slides

notes:
	$(PYTHON) build_script.py --target notes

script:
	$(PYTHON) build_script.py --target script

metadata:
	$(PYTHON) update_metadata.py

check:
	$(PYTHON) build_script.py --check-only
