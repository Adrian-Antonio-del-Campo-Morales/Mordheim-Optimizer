# Mordheim Optimizer

Mordheim Optimizer is a Monte Carlo simulator for comparing warriors, advances,
weapons, armour, and equipment in one-on-one close combat.

The application uses an independent English knowledge base derived from
[The New Mordheimer](https://mordheimer.net/docs/introduction). It supports all
Core, Grade 1a, Grade 1b, and Grade 1c warbands except Court of the Profane
Pleasures. Grade 2 and higher warbands are outside the current scope.

## Features

- Canonical warband and warrior profile selection.
- Custom candidates and opponents.
- Legal weapon, armour, equipment, material, preparation, and poison loadouts.
- Individual and combined advance comparisons.
- Weighted random opponents.
- Configurable simulation counts and cancellable analysis runs.
- Excel profile and result workbooks using the native Mordheim format.
- Optional house rules and cost-aware MOTTA ranking.
- NumPy simulation with an optional compiled Cython kernel.

The optimizer estimates combat outcomes. It does not replace the game rules or
resolve movement, terrain, psychology, magic, campaign, or multi-model effects.
Deferred edge cases are listed in
[`notes/mordheim-rule-todos.md`](notes/mordheim-rule-todos.md).

## Download for Windows

Download the portable executable from the
[latest GitHub Release](https://github.com/Adrian-Antonio-del-Campo-Morales/Mordheim-Optimizer/releases/latest).
It is a single file and does not require Python or installation.


[Descargar Trollheim Optimizer Portable 6.1.0](https://github.com/Adrian-Antonio-del-Campo-Morales/Mordheim-Optimizer/releases/download/v1.0.0/Mordheim-Optimizer-Portable-1.0.0.exe)


Windows SmartScreen may warn about an unsigned application. Verify that the
file was downloaded from this repository before running it.

## Run from source

Python 3.10 or later is required.

```powershell
python -m pip install -r requirements.txt
python Mordheim_Optimizer.py
```

The installed GUI entry point is `mordheim`.

## Validate

```powershell
python tools\validate_knowledge_base.py
python tools\validate_mordheim_runtime_knowledge.py
python -m pytest -q
```

## Build for Windows

```powershell
.\build_Mordheim_ONEFILE.bat
.\build_Mordheim_INSTALLER.bat
```

Generated files are written under `dist/` and are not tracked.

## Project structure

- `src/mordheim_optimizer/`: application and simulation engine.
- `sources/knowledge/`: independent English Mordheim knowledge base.
- `tests/`: engine, rules, catalogue, workbook, and UI contract tests.
- `tools/`: knowledge capture, normalization, validation, and build helpers.
- `PROJECT_STATUS.md`: scope and implementation status.

Mordheim and related names and rules belong to their respective rights holders.
This project is an unofficial analytical tool.
