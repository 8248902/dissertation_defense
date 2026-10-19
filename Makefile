PYTHON ?= python3

.PHONY: all slides notes script metadata check refs

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

# Refresh only from a fresh, completed thesis build.
refs:
	@test -n "$(THESIS_BUILD)" || (echo "Usage: make refs THESIS_BUILD=/path/to/fresh/build"; exit 2)
	$(PYTHON) reference_support.py --thesis-build "$(THESIS_BUILD)"
