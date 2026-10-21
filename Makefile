PYTHON ?= python3
# The presenter needs pypdf; use PYTHON if it has it, otherwise a throwaway uv environment.
PRESENTER_PYTHON ?= $(shell $(PYTHON) -c 'import pypdf' 2>/dev/null && echo $(PYTHON) || echo 'uv run --no-project --with pypdf python3')
# The Anki deck needs genanki (see anki/README.txt).
ANKI_PYTHON ?= /home/q/g/r/.venv/bin/python

.PHONY: all slides notes script committee metadata check refs presenter anki

# Everything: four PDFs, metadata, the Pympress PDF, and the Anki deck (it reads source-map.csv).
all:
	$(PYTHON) build_script.py --target all
	$(PYTHON) update_metadata.py
	$(PRESENTER_PYTHON) build_presenter.py
	$(ANKI_PYTHON) anki/build_deck.py

slides:
	$(PYTHON) build_script.py --target slides

notes:
	$(PYTHON) build_script.py --target notes

script:
	$(PYTHON) build_script.py --target script

# Committee handout: main slides, the backups in committee-backups.txt, references.
committee:
	$(PYTHON) build_script.py --target committee

metadata:
	$(PYTHON) update_metadata.py

check:
	$(PYTHON) build_script.py --check-only

# Refresh only from a fresh, completed thesis build.
refs:
	@test -n "$(THESIS_BUILD)" || (echo "Usage: make refs THESIS_BUILD=/path/to/fresh/build"; exit 2)
	$(PYTHON) reference_support.py --thesis-build "$(THESIS_BUILD)"

# Full script and linked MP4 panels for Pympress on two monitors.
presenter:
	$(PRESENTER_PYTHON) build_presenter.py

anki:
	$(ANKI_PYTHON) anki/build_deck.py
