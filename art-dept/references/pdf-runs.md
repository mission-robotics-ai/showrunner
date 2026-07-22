# Merged print runs

One PDF per paper stock, each sign repeated its quantity, so the human prints exactly one copy of each file. This removes the two failure modes of a 15-file print job: picking through files and miscounting quantities.

## Build

`scripts/pdf_runs.py build <manifest.json>` — manifest maps run-file → ordered list of `[pdf, qty]` pairs:

```json
{
  "tabloid-run.pdf": [["s01.pdf", 2], ["s02.pdf", 1]],
  "letter-run.pdf":  [["s03.pdf", 10], ["s07.pdf", 2]]
}
```

Mixed orientations inside one run are fine — same stock, the shop prints the file.

## Verify (mandatory)

`scripts/pdf_runs.py verify <manifest.json>` — page-counts every run against the manifest sum and prints per-page dimensions. Run after **every** regeneration; a silent count drift means someone prints the wrong kit. State the expected counts in the builder spec so the builder verifies too.

## When a run changes after distribution

Say it plainly to whoever holds the files: which run files changed, and that they must re-download. Per-sign PDFs stay published alongside runs for one-off reprints.
