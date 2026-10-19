DEFENSE: SPOKEN MATHEMATICS
Prepared for the current defense, 19 October 2026.

START HERE

Import defense-core.apkg into Anki for the 48 essential rehearsal cards.
Open Anki, choose File > Import, and select the package.

defense-oral.apkg contains all 90 cards: the same 48 core cards plus 42 deeper
follow-ups. The two packages use the same deck, model, and note identities.
Importing the full package later adds the follow-ups to the same deck.
If you want everything immediately, import only defense-oral.apkg.

HOW TO PRACTICE

Answer aloud before revealing the back. Aim for a clear 20–40 second answer,
with a little longer for the central proof sketch. Use your own wording.

The back gives one possible spoken answer and three recall anchors.
"If pressed" holds an extra qualification or calculation; the source panel
points back to the current slide pages and compiled dissertation references.
Grade whether you conveyed the idea accurately and fluently, including the
qualification that matters. Exact wording and notation are not the target.

Start with the core cards. Then work through follow-ups in the areas where
you hesitate. Finish by explaining the mean/fluctuation flow proof, the
stereo attenuation example, and the talk's common question without a card.
Keep rehearsing the actual slides as well: these cards prepare explanations
and interruptions, rather than the timing or transitions of the whole talk.

CONTENTS

                         Core   Follow-up   Total
Foundations                4        2         6
Temporal reconstruction   13       10        23
Optical flow              17       19        36
Stereo depth              10       10        20
Connecting the talk         4        1         5
Total                     48       42        90

Cards emphasize what the observations determine, what regularization selects,
why proof assumptions matter, and which conclusion a theorem supports.
There are no reverse cards or theorem-number memorization cards.

In Anki's Browse window, use tag:priority::core or tag:priority::followup.
Topic tags are topic::foundations, topic::temporal, topic::flow,
topic::stereo, and topic::synthesis. New cards are exported core first;
Anki's own deck options determine presentation order and daily limits.

OTHER FILES

preview.html          Open in a browser; expand a question after answering.
cards.txt             Editable source for all prompts and answers.
slide_titles.json     Stable title anchors, resolved to current deck pages.
defense-oral.tsv      Alternative Basic-note import, with HTML and tags.
build_deck.py         Rebuilds both packages, TSV, preview, and manifest.
manifest.json         Counts, validation scope, and source/output hashes.

Use the TSV as an alternative to the package, not an additional import.
It includes HTML directives and three columns: Front, Back, Tags.

SCOPE AND REBUILDING

The active core.tex, backup.tex, and defense-script.md determine the scope.
The sibling dissertation_thesis and the 10 October Chapters 3–4 proof
reference supply detail and proof qualifications. The deck is deliberately
weighted toward temporal reconstruction and the main flow theorem.

From the defense directory, rebuild with the supplied environment:

  /home/q/g/r/.venv/bin/python anki/build_deck.py

The environment uses genanki 0.13.1 and its dependencies. The builder checks
source labels, slide references, unique cards, rendered fields, package
integrity, and the TSV round trip. A desktop Anki GUI import was not run.
Card headers use slide keys; slide_titles.json maps them to titles, which
are resolved against the current source map so inserted backups shift safely.
After substantive changes to the talk, review the answers as well as
rebuilding: the builder validates references, not the meaning of the prose.
