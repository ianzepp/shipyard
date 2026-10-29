---
name: big-bang
description: Expand a rough idea into structured futures, options, and planning paths.
---

# Big Bang

Use this skill when the user brings a rough idea and wants an agent to help it
blossom into a wide but coherent design corpus.

Big Bang is a planning, research, analysis, and ideation skill. It is for
figuring out possible futures, consequences, tradeoffs, judgment calls, and the
direction a project should plan toward. Even when the seed is a software project,
do not treat Big Bang as a code generation or project-scaffolding mode.

Big Bang may produce planning artifacts for software work: architecture options,
stage maps, research briefs, risk registers, decision ledgers, product surfaces,
acceptance-shape notes, and delivery/factory handoff packets. It should not
write application code, scaffold a repo, generate boilerplate, install
dependencies, or begin implementation unless the user explicitly switches out of
Big Bang or asks for a delivery/factory handoff and approves implementation.

The job is not to pick the first good answer. The job is to repeatedly widen,
name, test, choose, recurse, and organize the idea until the user has a useful
map of possible directions and the strongest next branches are ready for deeper
planning.

Do not treat uncertainty or branch points as automatic stopping points. Treat a
branch point as a reflection checkpoint: name the decision, state what is at
stake, choose the best one or two branches by default, and keep exploring those
branches until the recursion budget is spent, the corpus reaches a handoff
point, or a human decision is genuinely required.

Ask the user to choose only when the next step would commit external money,
public positioning, production work, irreversible repo changes, sensitive
personal material, or a strategic identity choice that cannot be usefully
explored in parallel. Otherwise, make a provisional call, record it as such, and
continue.

Big Bang is upstream of `goal-forge`, `delivery`, and `factory`:

- use Big Bang to expand a rough idea into branches, tests, artifacts, and a
  coherent option corpus
- use `delivery` when one chosen branch needs to become an executable delivery
  plan with stages, workstreams, checkpoints, and gates
- use `factory` when the chosen branch has become a multi-phase phase set that
  should be executed, checked, committed, and resumed autonomously
- use `goal-forge` when a rough idea needs one grounded goal document before
  any plan or execution

For software projects, this boundary matters: Big Bang decides where the work
should go and what consequences follow; delivery/factory decide how to execute
that work. Keep the mode boundary explicit in handoff reads.

Borrow factory discipline during ideation: maintain a ledger, preserve phase
boundaries, define checkpoints, and keep enough state to survive compaction.
Do not hand off to factory just because the idea is large. Hand off when there
is a selected branch, a phase set, a target workspace, and a checkpoint policy.

## Depth Contract

Big Bang should be deeper than a single large file. At the start of a run,
choose and announce an intensity level, inferred from the user's request unless
they specify one:

- **Spark**: one-pass synthesis, light research, one durable artifact. Use only
  when the user asks for a quick pass or the seed is small.
- **Expansion**: multi-artifact ideation with bounded research, branch records,
  pressure tests, and a decision ledger. This is the default.
- **Cosmic Background Radiation**: full corpus exploration with branch trees,
  research briefs, creative variants, validation plans, and a delivery handoff.
  Use when the user says to go wild, run the pipeline, explore all the ways,
  or otherwise asks for significant depth.

For Expansion and Cosmic Background Radiation, do not stop after the first
branch map. Create a corpus directory or index once the idea clearly exceeds one
chat answer. Continue into at least the top one or two branches and produce the
next concrete artifacts those branches need.

Use a recursion budget so exploration stays useful:

- Spark: depth 1, no more than 1 artifact unless obviously useful
- Expansion: depth 2-3, usually 3-7 artifacts
- Cosmic Background Radiation: depth 3-5, usually a corpus directory with
  branch records, research briefs, decision ledger, and handoff map

Stop recursing within a branch when:

- the branch is dominated by another branch
- the next question needs live expert input or real-world validation
- the branch has a clear delivery/factory handoff
- further detail would be fake precision
- the recursion budget is spent

## Operating Loop

Run this loop until the user stops, chooses a branch, or the corpus reaches a
clear handoff point:

1. **Capture the seed**
   - Preserve the raw idea in the user's words.
   - Name the apparent center of gravity.
   - Separate facts, assumptions, taste, constraints, and open questions.
2. **Ask or answer the next unlocking question**
   - Identify one question that will split the idea into meaningful branches.
   - If a reasonable provisional answer can be inferred, answer it yourself,
     mark it provisional, and continue.
   - Ask the user only when the answer is required to avoid waste or harm.
   - Prefer questions about audience, operating model, trust, economics,
     automation boundary, hard constraints, and first wedge.
3. **Branch**
   - Generate several plausible directions from the answer.
   - Give each branch a short name and a one-line thesis.
   - Do not collapse branches too early.
4. **Pressure-test**
   - For each promising branch, identify load-bearing assumptions, failure
     modes, human gates, regulatory or operational friction, and cheapest
     validation steps.
   - Keep the pressure test concrete and unsentimental.
5. **Choose the next exploration branches**
   - Rank the branches by promise, urgency, reversibility, learning value, and
     risk.
   - Pick one lead branch and optionally one contrasting branch.
   - Record why they were chosen and why the other branches were parked.
   - Continue down those chosen branches instead of waiting for the user by
     default.
6. **Convert insight into artifacts**
   - When a branch stabilizes, create or update an artifact: idea record,
     index, tree, phase map, skill, pitch, research brief, model, or decision
     ledger.
   - Prefer durable Markdown in the active repo or workspace when the work is
     becoming larger than chat.
   - Treat each artifact as an input to the next loop, not as a polished final
     answer.
7. **Redirect and repeat**
   - End each pass with the next 1-3 useful redirects.
   - If the user gives no redirect but has asked for depth, continue with the
     recorded lead branch until a stop condition is reached.
   - Use the user's redirect to continue the loop rather than restarting.

## Delivery And Factory Bridge

As branches mature, decide whether the next move is still Big Bang, a delivery
handoff, or a factory handoff.

Stay in Big Bang when:

- the real center is still moving
- multiple branches remain plausible
- the hardest assumptions have not been pressure-tested
- the corpus needs more idea records, research briefs, pitch variants, or
  lifecycle sketches
- the next branch point can be explored provisionally without committing the
  user to money, public launch, production, or irreversible identity choices

Invoke `delivery` when:

- the user has selected a branch or asks to turn one branch into an
  implementation plan
- acceptance criteria can be stated
- the next artifact should be a normalized spec, repo-aware baseline, unit
  graph, workstreams, checkpoints, and gate plan

Invoke `factory` when:

- the user asks to execute, keep going autonomously, or run the phase set
- there is a durable phase list or lifecycle tree
- each phase can have a delivery spec, checkpoint target, validation policy,
  and commit unit (per-slice by default; see factory
  [Commits](../factory/SKILL.md#commits))
- the work should continue across many turns or compaction cycles without
  restarting the idea discovery process

When handing off to factory, prepare a compact factory-ready bundle:

- `Phase Set Source`
- `Selected Branch`
- `Target Workspace`
- `Delivery Spec Directory`
- `Checkpoint Policy`
- `Commit Unit`
- `Completed Big Bang Artifacts`
- `Open Questions`
- `Stop Or Escalation Conditions`

## Default Questions

Use questions like:

- What is the real center here, and what is just surface dressing?
- Who buys first, uses first, or benefits first?
- Is this internal infrastructure, a product, an operating company, or a
  support function?
- What must be true for this to work?
- What would kill it fastest?
- Where does a human still have to intervene, and can that be removed?
- What is the first narrow wedge?
- What is the first real-world bottleneck?
- What are the best one or two branches to play out without asking the user yet?
- What decision can be made provisionally, and what would reverse it?
- What branch should be parked, and what evidence would revive it?
- Does the current corpus explain this well enough for another model to warm up
  cold?
- Should this be one document, a directory tree, a reusable skill, or a repo?

See `references/redirect-patterns.md` for example redirect patterns.

## Corpus Shape

When the idea grows beyond chat, prefer this progression:

1. raw source material
2. structured idea record
3. index or registry
4. pressure-test sections
5. pitch or narrative artifact
6. research briefs for hard unknowns
7. phase or lifecycle tree
8. reusable process skill
9. delivery or implementation plan
10. factory-ready phase set

Do not create all of these by default. But for Expansion and Cosmic Background
Radiation runs, assume one large file is only the opening move. Add the next
artifact when a branch, decision, research unknown, creative direction, or
validation path would otherwise be buried inside a monolith.

See `references/artifact-ladder.md` for the artifact progression and
`references/factory-delivery-bridge.md` for the handoff rules.

## Multi-Turn Discipline

For long runs:

- Keep a visible working state: current seed, branches, pressure-test results,
  artifacts created, next redirects.
- Keep a decision ledger: branch points encountered, provisional choices made,
  branches explored, branches parked, and evidence needed to reverse a choice.
- After each major turn, summarize the branch map and the strongest unresolved
  questions.
- Use delivery-style artifact flow: each new artifact should name its producer,
  consumer, and unresolved ambiguity.
- Use factory-style ledger fields when the run becomes multi-phase: current
  phase, completed phases, pending phases, checkpoint policy, and stop
  conditions.
- Across compaction, resume from the latest artifact and branch ledger instead
  of starting over.
- If the user says "continue", "next", "run the pipeline", or "send it",
  proceed with the next recorded redirect.

## Stop Conditions

Stop expanding and recommend a handoff when:

- one branch clearly dominates and is ready for a goal document (`goal-forge`)
  or for delivery planning
- a branch has a phase set that is ready for factory execution
- the next question requires external research or expert review
- the corpus is coherent enough for another model to warm up cold
- the user asks to commit, archive, or switch from ideation to implementation

Do not stop merely because there is a branch point. Stop when the branch point
cannot be played out responsibly without the user, or when the chosen branch has
reached a real handoff boundary.

## Output Shape

Use this default response shape:

1. `Current Read` - short statement of the idea's center
2. `Branches` - named options with one-line theses
3. `Decision Read` - the branch point, what is at stake, and the provisional
   choice of one or two branches to explore next
4. `Pressure Test` - load-bearing assumptions and likely failure modes
5. `Artifacts` - files created or updated, including branch records and ledgers
   when the run is deeper than Spark
6. `Next Redirects` - 1-3 questions or artifact moves that can drive the next
   loop
7. `Handoff Read` - stay in Big Bang, invoke goal-forge, invoke delivery, or invoke factory

Keep the output compact enough that the user can redirect easily.
