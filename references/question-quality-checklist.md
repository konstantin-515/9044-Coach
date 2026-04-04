# Question Quality Checklist

Use this file as the final quality gate before returning a generated question or workspace.

## Similarity Check

- Do not stay too close to one original lab or weekly test question.
- It is fine to reuse a pattern, but change the story, data, constraints, or combination of operations.
- If one source strongly inspired the result, describe it as "in the style of the local archive".

## Solvability Check

- The task must be solvable from the written statement alone.
- Input and output rules must be unambiguous.
- If sorting, deduplication, case normalization, or formatting matters, say it explicitly.

## Sample And Edge Case Check

- Include at least one normal case and one edge case.
- The edge case should test a realistic mistake, not a contrived trick.
- Sample outputs should be hand-checkable from the sample inputs.

## Workspace Consistency Check

If files are generated on disk:

- `README.md` must name the correct target file
- `tests/` must reference the actual target filename
- files mentioned in `README.md` must exist
- expected outputs must match the provided sample data
- the generated folder should be usable immediately after `cd` into it

## Study Value Check

- The question should help the user practice a recognisable 9044-style skill.
- Difficulty should come from realistic constraints and precision, not obscurity.
- The result should encourage programming practice, not just reading.
