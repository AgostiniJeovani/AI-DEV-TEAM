---
name: dependency-safety-gate
description: Assess a proposed application dependency before adding or installing it. Use whenever an AI-DEV-TEAM implementation would change a package manifest, lockfile, container image, SDK, plugin, or build dependency.
---

# Dependency safety gate

Use this skill before a package, SDK, container image, plugin, or build tool is
added, updated, or installed. It is a risk-reduction gate; it cannot prove that
third-party code has no malware.

1. Confirm the approved use case and why existing project capabilities do not
   satisfy it. Prefer a small, mature, actively maintained, widely used option
   from an official registry or publisher.
2. Inspect the exact package name and version for typosquatting, publisher or
   organization, official links, release cadence, maintainer health, license,
   known advisories, compatibility, transitive footprint, and install/postinstall
   scripts. Use authoritative registries and advisory sources where possible.
3. Ask `security-engineer` for a proportional review when the package handles
   auth, crypto, payments, uploads, AI tools, data access, native code, build
   hooks, or privileged execution.
4. Record the need, candidate alternatives, evidence, version, risks,
   installation scripts, owner, and decision in the project checkpoint or
   handoff. Pin the selected version and retain the lockfile.
5. Install only project-locally and only after the decision passes. Never use a
   global install, `curl | shell`, a package from an untrusted source, or a
   bypass for package scripts or lockfiles merely to make progress.

Block and return to the human when provenance cannot be established, an
unexplained install script or high-impact advisory remains, the package needs
privileged access, or the risk materially exceeds the approved project scope.
