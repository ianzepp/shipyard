# Redirect Patterns

These patterns show how a rough idea becomes a structured corpus: repeatedly
asking a sharper question, branching, pressure-testing, and turning the result
into a durable artifact.

## Useful Redirect Types

### Scope Correction

Use when the agent starts building in the wrong medium or at the wrong scale.

Prompt shape:

```text
Timeout. This is actually a docs-only / design / research project for now.
```

### Coherence Check

Use after an initial scaffold exists.

Prompt shape:

```text
Do these docs accurately describe the goal of what I am trying to do here?
```

### Cold-Start Handoff

Use when the corpus should become durable enough for another model.

Prompt shape:

```text
Update this so another LLM can warm up on the project without me explaining it
again.
```

### Artifact Inventory

Use when an idea has an operating loop but no concrete document set.

Prompt shape:

```text
What core docs, records, or skills are required for the basic lifecycle?
```

### Collection Instead Of Single Doc

Use when one long doc would hide the useful structure.

Prompt shape:

```text
I think this should be a collection: a directory with phases, and within each
phase a collection of docs or skills. Show me an example.
```

### Example Before Execution

Use when the shape is uncertain.

Prompt shape:

```text
Show me the example shape first. If it lands, build it.
```

### Naming And Numbering Pass

Use after the tree exists but the ontology is not quite right.

Prompt shape:

```text
The tree is right, but the names/order should encode the model better.
```

### Human-Gate Elimination

Use for agent-native or automation-heavy ideas.

Prompt shape:

```text
Identify every step that requires a human, and think about how to eliminate or
minimize the human requirement.
```

### Pressure-Test Redirect

Use after a concept is structured but before committing to it.

Prompt shape:

```text
Pressure test would be useful. What breaks, what assumptions matter, and what
is the cheapest validation sequence?
```

### Pipeline Capture

Use after manually doing a good process once.

Prompt shape:

```text
Distill the process we just did into a predefined process that lives in this
repo, so the next rough idea can go through the same pipeline.
```

### Stage Addition

Use when the current pipeline is missing the next reusable step.

Prompt shape:

```text
The next skill after these would probably be <stage-name>, which produces
<artifact>. Add that.
```

### Extract To Dedicated Workspace

Use when an idea has enough mass to deserve its own corpus.

Prompt shape:

```text
New empty project here. I am extracting this idea into a project for continued
design work. Read the source idea and the surrounding context first.
```

### First Hard Constraint

Use once a scaffold exists and the idea needs reality pressure.

Prompt shape:

```text
No more phases for now. Pivot to research on the very start: what is the first
real-world bottleneck?
```

### Delivery Handoff

Use when a branch has become strong enough to plan concretely.

Prompt shape:

```text
This branch is the one. Turn it into a delivery artifact with stages,
workstreams, checkpoints, gate criteria, and open questions.
```

### Factory Handoff

Use when a phase tree should become an autonomous execution loop.

Prompt shape:

```text
This is now a phase set. Prepare the factory handoff, then run it phase by phase
with delivery specs, checkpoint gates, and commits.
```

## Branch Ledger Template

Use a compact ledger when the run spans multiple turns.

```markdown
# Big Bang Ledger

## Seed

Raw idea:

Current center:

## Branches

| Branch | Thesis | Status | Next Question |
|---|---|---|---|

## Pressure Tests

| Branch | Load-Bearing Assumption | Failure Mode | Cheapest Validation |
|---|---|---|---|

## Artifacts

| Artifact | Purpose | Status |
|---|---|---|

## Handoff Read

Current mode: Big Bang / Delivery-ready / Factory-ready

Promotion trigger:

Stop or escalation condition:

## Next Redirects

1.
2.
3.
```
