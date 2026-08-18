from pathlib import Path
import tomllib


ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = ROOT / "agents"
EXPECTED = {
    "project-configurator", "requirements-analyst", "system-analyst",
    "system-architect", "frontend-engineer", "backend-engineer",
    "uiux-designer", "data-ai-engineer", "qa-engineer", "code-reviewer",
    "security-engineer", "devops-engineer", "technical-writer",
}
REQUIRED = {"name", "description", "developer_instructions"}
ALLOWED = REQUIRED | {"model", "model_reasoning_effort", "sandbox_mode", "mcp_servers", "skills"}
READ_ONLY = {
    "project-configurator", "requirements-analyst", "system-analyst",
    "system-architect", "uiux-designer", "qa-engineer", "code-reviewer",
    "security-engineer",
}


def main() -> int:
    files = {path.stem: path for path in AGENTS_DIR.glob("*.toml")}
    errors = []
    if set(files) != EXPECTED:
        errors.append(f"agent_files={sorted(set(files) ^ EXPECTED)}")
    parsed = {}
    for name, path in sorted(files.items()):
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError) as exc:
            errors.append(f"invalid_toml={name}:{exc}")
            continue
        parsed[name] = data
        missing = REQUIRED - set(data)
        unsupported = set(data) - ALLOWED
        if missing:
            errors.append(f"missing_required={name}:{sorted(missing)}")
        if unsupported:
            errors.append(f"unsupported_fields={name}:{sorted(unsupported)}")
        if data.get("name") != name:
            errors.append(f"name_mismatch={name}:{data.get('name')!r}")
    names = [data.get("name") for data in parsed.values()]
    if len(names) != len(set(names)):
        errors.append("duplicate_names=true")
    for name in READ_ONLY:
        if parsed.get(name, {}).get("sandbox_mode") != "read-only":
            errors.append(f"not_read_only={name}")
    docs = [ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "docs" / "agent-contract.md",
            ROOT / "docs" / "handoff-protocol.md", ROOT / "docs" / "workflow.md",
            ROOT / "docs" / "reading-guide.md", ROOT / "docs" / "testing.md",
            ROOT / "setup" / "README.md"]
    missing_docs = [str(path.relative_to(ROOT)) for path in docs if not path.exists()]
    if missing_docs:
        errors.append(f"missing_documentation={missing_docs}")
    print(f"agent_count={len(parsed)}")
    print(f"unique_names={len(names) == len(set(names))}")
    print(f"missing_required={sum('missing_required=' in e for e in errors)}")
    print(f"unsupported_fields={sum('unsupported_fields=' in e for e in errors)}")
    print(f"architect_read_only={parsed.get('system-architect', {}).get('sandbox_mode') == 'read-only'}")
    print(f"documentation_complete={not missing_docs}")
    if errors:
        print("validation=failed")
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("toml_valid=true")
    print("validation=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
