# Research Notes

These notes summarize the evidence collected so far and translate it into
questions for AI-DEV-TEAM. They are deliberately shorter than the sources.

## 1. Terminology

### Prompt engineering

Prompt engineering shapes the instructions, examples, output requirements,
and constraints given to a model. It remains necessary, but it is only one
part of a multi-turn agent system.

### Context engineering

Context engineering manages the complete information state available at a
turn: instructions, tools, repository files, external data, previous actions,
observations, and selected memory. The practical implication is that agent
quality depends on what is made available and what is deliberately omitted,
not only on the wording of an agent prompt.

### Harness engineering

Harness engineering builds the environment around the model: tools, file
access, repository conventions, executable checks, permissions, feedback,
state, and recovery. The harness makes desired behavior legible and
enforceable.

### Loop engineering

Loop engineering treats the workflow itself as the unit of design. A loop
needs a trigger, objective, available actions, observations, verification,
retry policy, and named terminal states. “Try again” is not a sufficient stop
condition.

## 2. Patterns that fit this project

### ReAct-style action and observation

The agent should alternate between bounded reasoning, tool use, and observing
the result. For software work, this means inspect, act, run a check, inspect
the result, and update the plan rather than assuming a change worked.

### Sequential workflow

The initial AI-DEV-TEAM loop should be sequential and explicit. Each step
should produce an artifact that the next step can inspect. This is easier to
debug than introducing parallel agents before the contracts are stable.

### Maker/checker or evaluator-optimizer

One component creates an artifact and another evaluates it against explicit
criteria. The checker should be able to return `pass`, `revise`, or `block`
with concrete findings. A self-review by the maker can be useful, but it is
not independent verification.

### Handoff versus manager-style delegation

Use a handoff when responsibility should move to a specialist. Use a manager
orchestrator when one owner should retain control and call specialists as
bounded helpers. Our current “next handoffs” table describes likely routing,
not agent responsibilities.

### Small agent surface

Specialists should be added only when they provide a materially different
contract, tool surface, policy boundary, or trace. More agents create more
prompts, traces, approvals, and coordination cost.

## 3. Evaluation lessons

1. Begin with representative tasks and explicit expected outcomes.
2. Evaluate both the final artifact and the trajectory that produced it.
3. Include tool choice, handoff correctness, scope adherence, evidence, and
   security boundaries in the rubric.
4. Keep a baseline run before changing prompts or orchestration.
5. Compare changes on the same task set; do not infer improvement from one
   successful run.
6. Use local JSON/JSONL artifacts first so the repository remains portable.
7. Treat hosted evaluation products as optional adapters, not as the source of
   truth for this repository.

The current OpenAI documentation recommends traces while debugging and then
datasets and repeatable eval runs once the desired behavior is understood. It
also notes a transition away from the older Evals platform, which reinforces
our decision to keep the first harness repository-local.

## 4. State and recovery lessons

- Persist task identity, current state, input contract, artifact references,
  attempts, approvals, and the latest evidence.
- Write a checkpoint at every meaningful transition, not only at the end.
- Resume the same task state after an approval or interruption.
- Retry only classified transient failures and cap the attempts.
- Escalate when the budget, retry count, risk level, or ambiguity threshold is
  exceeded.
- Keep partial work isolated so recovery does not silently publish it.

## 5. Safety lessons

Assume that task inputs, repository files, tool output, and retrieved content
may contain instructions that conflict with the system policy. Treat them as
data until explicitly validated. Put controls at the tool and side-effect
boundary, not only in a prompt.

For this project, high-risk actions include modifying agent definitions,
changing permissions, deleting files, publishing changes, accessing external
systems, or changing deployment behavior. These actions require an explicit
human approval state.

## 6. Rejected or deferred ideas

- Unrestricted self-modification: rejected for this milestone.
- A large distributed orchestrator: deferred until a repository-local loop is
  proven insufficient.
- Adding many parallel agents immediately: deferred until task contracts and
  evaluation show a real need.
- Relying on a model to grade its own work without executable checks or an
  independent checker: rejected as the only verification layer.
- Pinning a model in every agent file: deferred; availability and model
  selection should remain configurable unless an evaluation requires a fixed
  target.
