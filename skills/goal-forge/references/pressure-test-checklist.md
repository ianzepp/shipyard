# Pressure Test Checklist

Use this reference during the pressure-test phase. Answer from code and data before asking the user.

## Design Tree

For each decision branch:

- What decision needs to be made?
- Which earlier decisions does it depend on?
- What would change if this branch chose option A versus option B?
- Which code path, schema, generated client, database, fixture, log, screenshot, PR, or transcript can answer it?
- What did the evidence say?
- What remains unknowable without user preference or authorization?

Do not move to dependent branches while their parent decision is still vague.

## Problem

- What problem is actually being solved?
- What user or operator pain triggered this?
- Is the requested solution only one possible solution?
- What would make this work unnecessary?

## Scope

- What is in the first phase?
- What is explicitly out of scope?
- What adjacent work is tempting but should wait?
- What existing behavior must remain unchanged?

## Data And Truth

- Which database, API, event stream, file format, or generated client is authoritative?
- Are docs or PRDs making claims that code contradicts?
- Are there real examples, logs, records, screenshots, or saved artifacts?
- What assumptions still lack evidence?
- Did the agent inspect the code/data itself rather than asking the user to go find it?
- Is every major claim in the goal tied to an artifact, command, query, or explicit user statement?

## Agent Execution

- Can an implementation agent start without rereading the whole repo?
- Are paths, commands, and source packets exact?
- Are acceptance criteria objective?
- Are stop conditions clear?
- Does validation prove the user-facing flow, not only a unit seam?

## Risk And Exit

- Is a kill switch, flag, rollback, removal plan, opt-out, or monitoring threshold needed?
- Is the exit strategy worth its complexity?
- Has the user approved including that strategy?
- Are destructive actions, credentials, and production writes forbidden unless explicitly authorized?

## Release Posture

- Does the work affect user-visible behavior, CLI/API contracts, schemas, config, migrations, package metadata, or operator workflows?
- Should the first useful milestone end with a version bump, changelog entry, release notes, tag, deployment plan, migration note, or explicit deferred-release decision?
- Is external publication, production deployment, registry publishing, or a destructive migration a separate authorization gate?
- What evidence identifies the repo's current release convention and last released version?

## Completion

- Would another agent know when to stop?
- Could the goal be misread into a much larger project?
- Could the agent declare victory while the user still cannot test or feel the result?
- What is the single most important ambiguity left?
