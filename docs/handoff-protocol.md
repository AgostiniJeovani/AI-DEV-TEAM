# Handoff Protocol

A handoff is the contract between agents. It reduces repetition, makes
decisions auditable, and clarifies what still needs human judgment.

## Format

```text
HANDOFF
From: <agent>
To: <agent or user>
Objective: <expected result>
Context: <repository, requirements, and evidence analyzed>
Decisions: <decisions made and reasons>
Artifacts: <files, diagrams, tests, or links>
Open items: <open questions and missing information>
Risks: <risk, impact, and mitigation>
Next step: <concrete action, owner, and completion condition>
```

## Rules

- Separate observed facts from inferences.
- The next agent should be able to start without repeating the investigation.
- Highlight irreversible decisions, high risks, and external actions.
- A handoff is not automatic approval: the recipient still validates its own
  scope.
