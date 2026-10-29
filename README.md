# Shipyard

Agent skills for the engineering process. They take an idea, or a large
feature nobody has scoped yet, and work it through planning and delivery until
it ships as verified commits.

Each skill is one stage. A stage reads the artifact an earlier stage left in
the repo, does one kind of work, and saves its own artifact for the next. The
stages are entry points, not a strict chain: enter at the one that fits the
work in front of you, and skip stages the work does not need.

```text
idea
  → big-bang       expand a rough idea into futures, options, and paths
  → goal-forge     converge fuzzy intent into one grounded goal document
  → goal-check     verify the goal is defined enough to build against
  → campaign       route several related goals through one completion contract
  → delivery       compile one outcome into a repo-aware implementation spec
  → slicer         cut the spec into small, disjoint, self-contained slices
  → factory        implement, verify, review, and commit phase by phase
  → auditor        independently audit the change and its evidence
  → polish         per-file closeout with a subtractive bias
shipped
```

Review lenses that factory, auditor, and polish call along the way:

| Skill | Use |
| --- | --- |
| `correctness` | Hunt behavioral bugs, invariant breaks, races, and data-loss risks. |
| `cleanliness` | Shape code for managed complexity: boundaries, size, dispatch, naming. |
| `housekeeping` | Repository maintenance at inflection points: format, lint, build, test hygiene. |
| `consequences` | Read-only trace of what a proposed change will affect before you build it. |
| `red-green` | Testability and coverage work through red-green loops. |
| `poker-face` | Audit completed work against what was promised. |

## Principles

- **The repo is ground truth.** Goals, campaigns, and specs record intent.
  Code, tests, and history record what exists. When they disagree, the repo
  wins and the document is the defect.
- **Scope is a contract.** Work admitted to a campaign stays mandatory until it
  is implemented and verified. Stages may sequence it; they may not quietly
  drop it.
- **Plans become edits, not more discovery.** A spec is ready when an
  implementer can start a named edit without rediscovering the architecture.
- **Tests prove the target.** Never weaken a test or a gate to get a green run.
- **Every stage leaves an artifact.** Work survives context limits, handoffs,
  and restarts because state lives in files, not in chat.

The skills work with one agent in one repo. Where a harness supports
subagents, factory and auditor use them for independent review and for
running slices with disjoint write scopes in parallel. Nothing requires them.

## Install

### Claude Code

```text
/plugin marketplace add ianzepp/shipyard
/plugin install shipyard@shipyard
```

### Other harnesses

Clone the repo and link each folder under `skills/` into your harness's skill
directory. For Codex:

```bash
git clone https://github.com/ianzepp/shipyard ~/shipyard
for s in ~/shipyard/skills/*/; do ln -s "$s" ~/.codex/skills/; done
```

Each skill is a folder with a `SKILL.md` (name, description, procedure), plus
optional `references/`, `scripts/`, and `agents/openai.yaml` metadata.

## License

MIT
