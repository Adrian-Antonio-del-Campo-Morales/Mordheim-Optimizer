"""Validate the canonical Mordheim knowledge base without changing it."""

from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "sources" / "knowledge"
PLACEHOLDERS = (
    "source_text",
    "see source",
    "source_preserved",
    "preserved within",
    "characteristics_and_rules",
)
CHARACTERISTICS = {"M", "WS", "BS", "S", "T", "W", "I", "A", "Ld"}
SOURCE_FIELDS = {"manual", "printed_page", "section"}


def load_yaml(path: Path, errors: list[str]):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # The filename matters more than twenty traceback lines.
        errors.append(f"Invalid YAML in {path.relative_to(ROOT)}: {exc}")
        return None


def valid_source(source) -> bool:
    return isinstance(source, dict) and SOURCE_FIELDS <= set(source) and all(
        source.get(field) not in (None, "") for field in SOURCE_FIELDS
    )


def validate_band(path: Path, band_ids: set[str], errors: list[str]) -> int:
    text = path.read_text(encoding="utf-8")
    lowered = text.lower()
    for marker in PLACEHOLDERS:
        if marker in lowered:
            errors.append(f"Obsolete marker '{marker}' in {path.name}")

    band = load_yaml(path, errors)
    if not isinstance(band, dict):
        return 0

    band_id = band.get("id")
    if not band_id or band_id in band_ids:
        errors.append(f"Missing or duplicate warband ID in {path.name}: {band_id!r}")
    band_ids.add(band_id)
    if not valid_source(band.get("source")):
        errors.append(f"Warband without structured source in {path.name}")

    profiles = band.get("profiles", [])
    local_profiles = {profile.get("id") for profile in profiles}
    if None in local_profiles or len(local_profiles) != len(profiles):
        errors.append(f"Profiles with missing or duplicate IDs in {path.name}")
    equipment_lists = band.get("equipment_lists", [])
    list_ids = {entry.get("id") for entry in equipment_lists}
    if None in list_ids or len(list_ids) != len(equipment_lists):
        errors.append(f"Equipment lists with missing or duplicate IDs in {path.name}")
    for equipment_list in equipment_lists:
        if not valid_source(equipment_list.get("source")):
            errors.append(f"Equipment list without source in {path.name}: {equipment_list.get('id')}")

    for member in band.get("roster", {}).get("members", []):
        if member.get("profile_id") not in local_profiles:
            errors.append(f"Unknown roster profile in {path.name}: {member.get('profile_id')}")
        maximum = member.get("maximum")
        if maximum is not None and member.get("minimum", 0) > maximum:
            errors.append(f"Impossible roster allowance in {path.name}: {member.get('profile_id')}")

    for profile in profiles:
        stats = profile.get("characteristics", {})
        if set(stats) != CHARACTERISTICS:
            errors.append(f"Incomplete profile in {path.name}: {profile.get('id')}")
        for list_id in profile.get("equipment_lists", []):
            if list_id not in list_ids:
                errors.append(f"Unknown equipment list in {path.name}: {list_id}")
        if not valid_source(profile.get("source")):
            errors.append(f"Profile without structured source in {path.name}: {profile.get('id')}")
        for rule in profile.get("rules", []):
            if not valid_source(rule.get("source")):
                errors.append(f"Profile rule without source in {path.name}: {rule.get('id')}")

    for rule in band.get("band_rules", []):
        if not valid_source(rule.get("source")):
            errors.append(f"Warband rule without source in {path.name}: {rule.get('id')}")

    return len(profiles)


def validate_catalogs(errors: list[str]) -> int:
    record_ids: set[str] = set()
    records = 0
    for path in sorted((KB / "catalog").glob("*.yaml")):
        data = load_yaml(path, errors)
        if not isinstance(data, dict):
            continue
        if "records" not in data:
            continue
        for record in data["records"]:
            record_id = record.get("id")
            if not record_id or record_id in record_ids:
                errors.append(f"Missing or duplicate catalogue ID: {record_id!r} ({path.name})")
            record_ids.add(record_id)
            if not (record.get("source") or record.get("source_url")):
                errors.append(f"Record without source: {record_id} ({path.name})")
            if not record.get("rule_summary"):
                errors.append(f"Record without rule: {record_id} ({path.name})")
            records += 1
    return records


def validate_scope(band_ids: set[str], errors: list[str]) -> int:
    scope = load_yaml(KB / "index" / "warband-scope.yaml", errors)
    if not isinstance(scope, dict):
        return 0
    entries = scope.get("warbands", [])
    scoped_ids = {entry.get("id") for entry in entries if isinstance(entry, dict)}
    if scoped_ids != band_ids:
        missing = sorted(scoped_ids - band_ids)
        extra = sorted(band_ids - scoped_ids)
        errors.append(f"Scope/runtime mismatch (missing={missing}, extra={extra})")
    grades = set(scope.get("in_scope_grades", []))
    if grades != {"core", "1a", "1b", "1c"}:
        errors.append(f"Unexpected in-scope grades: {sorted(grades)}")
    if "court-of-the-profane-pleasures" in scoped_ids:
        errors.append("Court of the Profane Pleasures must remain excluded")
    return len(entries)


def main() -> None:
    errors: list[str] = []
    band_ids: set[str] = set()
    profile_count = 0
    band_paths = sorted((KB / "bands").glob("*.yaml"))

    for path in band_paths:
        profile_count += validate_band(path, band_ids, errors)

    if len(band_paths) != 49:
        errors.append(f"Warband count is {len(band_paths)}; expected 49")

    catalog_count = validate_catalogs(errors)
    scope_count = validate_scope(band_ids, errors)

    if errors:
        raise SystemExit("\n".join(f"- {error}" for error in errors))

    print(
        f"OK: {len(band_paths)} warbands, {profile_count} profiles, "
        f"{catalog_count} catalogue rules and {scope_count} scoped entries"
    )


if __name__ == "__main__":
    main()
