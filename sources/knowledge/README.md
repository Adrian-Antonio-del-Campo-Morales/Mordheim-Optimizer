# Mordheim knowledge base

This directory is the canonical, English-language rules reference for Mordheim
Optimizer. Its primary source is [The New Mordheimer](https://mordheimer.net/docs/introduction).

## Scope

The initial target is every warband classified by Mordheimer.net as **Core**,
**Grade 1a**, **Grade 1b**, or **Grade 1c**. Grade 2 and higher warbands are
explicitly out of scope. The catalogue is source-led: every factual record must
link to a page URL and identify the source publication stated by the website.

`index/warband-scope.yaml` is the complete intake register and `bands/` contains
one normalized, runtime-readable roster per supported warband. The Court of the
Profane Pleasures is intentionally excluded by project decision.

## Editorial rules

* Store structured facts and concise rule summaries, not a mirror of the web
  site or its prose.
* Use inches, gold crowns (`gc`), and the original English names.
* Preserve variants when the site lists them separately (for example, the two
  Amazon and Night Goblin entries).
* Treat the website's Grade and cited publication as source metadata, not as a
  game rule.
* Use the comparison log in `notes/` to identify changes required in the
  simulator; it is deliberately temporary and non-canonical.

## Current baseline

The knowledge base currently contains 49 source-normalized warbands covering
Core and Grades 1a–1c. Each record includes roster limits, profiles, equipment
lists, skill access, profile rules, band rules, and retained source sections.
Run `python tools/validate_mordheim_runtime_knowledge.py` to verify the runtime
contract. Differences from Mordheim and mechanics requiring engine work are
recorded in `notes/mordheim-rule-todos.md`.
