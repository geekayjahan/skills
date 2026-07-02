# Anti-Patterns

Failure modes that make skills underperform or rot. The pre-grading sweep in step 4
of the build loop (SKILL.md) runs against this list.

## In the instructions

- **Explaining what the model already knows.** No definitions of common formats,
  no "PDFs are documents that...". Add only knowledge the model lacks: your
  schemas, your conventions, your procedures.
- **Option buffets.** "You can use pypdf, or pdfplumber, or PyMuPDF..." forces a
  re-decision on every run. Name one default; add an alternative only with the
  named condition that makes it the better choice.
- **Vague gates.** "If appropriate", "when well understood", "may require input".
  Key every condition to something observable: a file that exists, an artifact the
  user supplied, a check that failed.
- **Rules without reasons.** "ALWAYS output JSON" invites exceptions; "Output JSON
  so downstream tools can parse it" holds, because the reason travels with the rule.
- **Unexplained constants.** `TIMEOUT = 47` with no justification gets cargo-culted
  or arbitrarily changed. State where the number comes from or derive it.
- **Time-anchored content.** "Before August 2025, use the old endpoint" goes stale
  invisibly. Describe the current pattern; move legacy handling to an explicitly
  labeled old-patterns section.
- **Drifting terminology.** "Endpoint" in one paragraph, "URL" in the next, "route"
  in a third reads as three concepts. Pick one word per concept and keep it.

## In the files

- **Audience documents.** No README, CHANGELOG, INSTALLATION_GUIDE, or notes about
  how the skill was made. A skill is read by an agent doing a job; every file that
  isn't for that job is noise it may load.
- **Scripts that punt.** A script that prints "handle this case yourself" pushes
  the hard part back onto the model at its least reliable moment. Handle errors in
  the script, with messages that say what to do next.
- **Backslash paths.** `scripts\helper.py` breaks off Windows. Forward slashes
  everywhere.

## Over time

- **Slop accumulation.** Every AI-written edit tends to add padding, restatement,
  and hedges; a skill maintained without subtraction degrades the model it was
  meant to sharpen. The pruning pass in
  [self-improving.md](self-improving.md) is the counterweight — it is not optional
  for skills that get edited.
