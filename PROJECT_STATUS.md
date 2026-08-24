# Simulator Status

This document is the single source for project status, modelling decisions, and
pending work. Canonical rules and data live in `sources/knowledge` and must not
be duplicated here.

## Scope

The application uses Monte Carlo simulation for one-on-one close-combat duels.
Fighters begin engaged, the charging fighter is chosen at random, and attacks,
wounds, saves, critical hits, states, and recovery are resolved. Duels still
unresolved after 50 turns are excluded from the final win percentage.

Covered features:

- final Mordheim modifiers applicable to the duel;
- general and exclusive weapons with direct effects;
- armour, protection, materials, drugs, poisons, and consumables;
- directly applicable skills implemented and verified by the engine;
- configurable opponents and weighted random profiles with legal equipment.

Movement, terrain, multiple combats, psychology, magic, prayers, campaigns, and
effects requiring decisions outside the represented duel are out of scope.

## Modelling decisions

- The Serpent Staff always uses its special attack.
- `Sweep` is activated automatically when its expected value exceeds that of
  normal attacks.
- The Ball and Chain retains its combat effects, but not uncontrolled movement
  or scenery collisions.
- Pikes are simulated with both fighters already in contact; the optional
  advantage for attacking from 8 cm away is not assumed.
- Random profiles and weights are representative rather than a reconstruction
  of a complete warband or current budget.
- Random equipment moderately favours inexpensive, common options.

## Remaining work

- TODO: optional replacement attacks (`Bear Hug`, `Bull Charge`, `Energy Focus`,
  `Wraith Touch`). They require a future per-round tactical-choice framework.
- TODO if scope expands: multi-model, multi-limb, Leadership, deployment,
  terrain, and other pre-contact mechanics. The rationale and exact boundary
  are recorded in `notes/mordheim-rule-todos.md`.
- Continue replacing representative enemy presets with filters backed directly
  by canonical Mordheim warband profiles.

## Performance

- The NumPy engine processes combat in batches of 100,000 to limit memory peaks
  and distribute work evenly.
- Configuration batches are sent to workers in groups of two to avoid a worker
  receiving disproportionately long work.
- Configurations producing the same effective fighter are calculated once; their
  rows share the result because no mechanical difference warrants another run.
- The Cython kernel accelerates simple weapon-and-rule duels. Fighters using
  skills, poisons, materials, or unsupported mechanics are routed to the full
  NumPy engine without changing the simulation.
- The compiled kernel is included in the portable executable and adds no end-user
  dependencies.

## Verification

Run before preparing a distribution:

```powershell
python -m pytest -q
python tools\validate_knowledge_base.py
python tools\benchmark_native_kernel.py -n 500000
```

Regenerate the portable executable only when preparing a new release.
