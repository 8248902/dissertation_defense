.PHONY: all slides notes

all: slides notes

slides:
	latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build defense.tex
	cp build/defense.pdf defense.pdf

notes:
	latexmk -pdf -interaction=nonstopmode -halt-on-error -jobname=defense-notes -outdir=build notes.tex
	cp build/defense-notes.pdf defense-notes.pdf
