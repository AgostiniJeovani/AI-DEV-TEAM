# Skills

This is step 5 of the guided path. Skills are reusable operating procedures;
agents are the specialists who carry them out. Activation exposes each skill as
an individual safe junction in your Codex skills folder, without replacing your
other personal skills.

| Skill | When it applies | Result |
|---|---|---|
| `web-cloud-project-intake` | You want to turn an idea, source material, or existing repository into a new web/cloud project. | A human-approved Project Brief. |
| `web-cloud-project-delivery` | A Project Brief, target directory, source of truth, and primary stack are approved. | A `rapid_mvp` or `standard` delivery with only the necessary specialist handoffs. |
| `dependency-safety-gate` | A package, SDK, image, plugin, build tool, manifest, or lockfile would change. | A documented pass or block before local installation. |
| `local-app-validation` | Implementation is ready for independent verification or a retry completed. | Traceable command and browser evidence with `pass`, `revise`, or `block`. |

For a simple local CRUD MVP, `rapid_mvp` is the default lane: one compact plan,
only the required sequential writers, and one independent QA gate. UI work
cannot pass from API/build evidence alone; it needs a fresh interactive browser
check at desktop and mobile widths. A reproduced local startup, port, runtime,
asset, or browser-reachability failure is handed to `debug-engineer` for one
bounded correction before independent validation repeats; this is a conditional
recovery path, not another required skill or routine stage.

Use the skills in that order for a new application. The first two are not
required when you deliberately invoke an individual agent on an existing
project; in that mode no `.ai-dev-team/` control folder is created.

Each skill is intentionally small and points back to the agent definitions and
[`AGENTS.md`](../AGENTS.md) for authority. They do not grant permission to
install, deploy, create Git state, access credentials, or act outside the
target project.

## Next step

Read [`docs/README.md`](../docs/README.md) completely to understand the
checkpoint, recovery, and evaluation mechanics behind the optional loop.
