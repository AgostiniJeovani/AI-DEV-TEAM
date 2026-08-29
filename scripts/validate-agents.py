from pathlib import Path
import tomllib


ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = ROOT / "agents"
SKILLS_DIR = ROOT / "skills"
EXPECTED = {
    "project-configurator", "requirements-analyst", "system-analyst",
    "system-architect", "frontend-engineer", "backend-engineer",
    "uiux-designer", "data-ai-engineer", "qa-engineer", "code-reviewer",
    "security-engineer", "devops-engineer", "technical-writer", "agent-engineer",
    "project-orchestrator", "debug-engineer",
}
EXPECTED_SKILLS = {
    "web-cloud-project-intake", "web-cloud-project-delivery",
    "dependency-safety-gate", "local-app-validation",
}
REQUIRED = {"name", "description", "developer_instructions"}
ALLOWED = REQUIRED | {"model", "model_reasoning_effort", "sandbox_mode", "mcp_servers", "skills"}
READ_ONLY = {
    "project-configurator", "requirements-analyst", "system-analyst",
    "system-architect", "uiux-designer", "qa-engineer", "code-reviewer",
    "security-engineer", "agent-engineer",
}


def read_skill_metadata(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing_front_matter")
    _, front_matter, _ = text.split("---\n", 2)
    metadata = {}
    for line in front_matter.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()
    return metadata


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
    skills = {path.parent.name: path for path in SKILLS_DIR.glob("*/SKILL.md")}
    if set(skills) != EXPECTED_SKILLS:
        errors.append(f"skill_files={sorted(set(skills) ^ EXPECTED_SKILLS)}")
    valid_skills = 0
    for name, path in sorted(skills.items()):
        try:
            metadata = read_skill_metadata(path)
        except (OSError, ValueError) as exc:
            errors.append(f"invalid_skill={name}:{exc}")
            continue
        if metadata.get("name") != name:
            errors.append(f"skill_name_mismatch={name}:{metadata.get('name')!r}")
        if not metadata.get("description"):
            errors.append(f"skill_description_missing={name}")
        else:
            valid_skills += 1
    docs = [ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "agents" / "README.md",
            ROOT / "setup" / "README.md", ROOT / "scripts" / "README.md",
            ROOT / "skills" / "README.md", ROOT / "docs" / "README.md",
            ROOT / "docs" / "evaluation" / "README.md"]
    missing_docs = [str(path.relative_to(ROOT)) for path in docs if not path.exists()]
    if missing_docs:
        errors.append(f"missing_documentation={missing_docs}")
    print(f"agent_count={len(parsed)}")
    print(f"unique_names={len(names) == len(set(names))}")
    print(f"missing_required={sum('missing_required=' in e for e in errors)}")
    print(f"unsupported_fields={sum('unsupported_fields=' in e for e in errors)}")
    read_only_agents = sorted(name for name in READ_ONLY if parsed.get(name, {}).get("sandbox_mode") == "read-only")
    print(f"read_only_count={len(read_only_agents)}")
    print(f"read_only_agents={','.join(read_only_agents)}")
    print(f"skill_count={len(skills)}")
    print(f"valid_skill_metadata={valid_skills == len(EXPECTED_SKILLS)}")
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
