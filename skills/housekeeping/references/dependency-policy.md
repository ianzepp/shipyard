# Dependency Policy

Ecosystem-specific dependency hygiene. Load during mechanical step 1.3 (environment verification) or any intentional dependency upgrade, when inspecting or changing lockfiles, package managers, or dependency versions.

## Global Rules

- Prefer locked dependency graphs. Keep ecosystem-appropriate lockfiles; do not weaken existing pinning.
- Where the ecosystem supports it, configure minimum package release age or cooldown before install/upgrade.
- Before any dependency or lockfile upgrade, check the target package and version for compromise, malware, hijack, or supply-chain incidents using primary advisories or ecosystem security tooling.
- Do not upgrade packages just to chase freshness. Upgrade only to restore installability, fix a lint/build/test blocker, or align with repo policy.
- If a package-managed component has no lockfile, treat that as housekeeping debt. Add or restore the lockfile when standard for the ecosystem; keep install commands strict.

## Clean Environment By Language

Build/check only: this table never runs tests. Clean commands are opt-in (only when the user asks or a stale build is suspected).

| Language | Action |
| --- | --- |
| Rust | Repo-standard `cargo check` / `cargo build`. Run `cargo clean` first only when the user asks or a stale build is suspected |
| TypeScript / JavaScript | Strict reinstall from lockfile (`npm ci`, `pnpm install --frozen-lockfile`, `yarn install --frozen-lockfile`, `bun install --frozen-lockfile`), then the project build; remove `node_modules` only when the user asks or a stale install is suspected |
| Go | Repo-native dependency refresh, then `go build`; do not clear shared global module caches by default |
| Python | Sync project-local env (`uv sync`, `poetry install`, `pip install -r requirements.txt`), then the project check/build; do not wipe global Python caches |

## Release-Age Controls

Inspect dependency policy files and package-manager config:

| Ecosystem | Prefer |
| --- | --- |
| npm | `min-release-age` in project or user config when supported |
| pnpm | `minimumReleaseAge` and `minimumReleaseAgeExclude` |
| Yarn | `npmMinimalAgeGate` and `npmPreapprovedPackages` |
| Bun | `minimumReleaseAge` |
| uv | `exclude-newer` with relative duration and package overrides where needed |
| pip | Preserve existing timestamp-gated installs; do not invent fragile workflows unless the repo clearly wants them |
| Rust | Preserve committed `Cargo.lock`; note gaps explicitly if release-age controls are unavailable |

Default when introducing a new cooldown and the repo has no preference: **7 days**. Narrow only for clearly trusted packages that must move faster.

## Upgrade Safety

Before changing a dependency version:

1. Check the target release for attacks, compromise reports, malicious publishes, or active advisories.
2. Prefer ecosystem advisories, package-manager audit tooling, OSV, GitHub advisories, or vendor incident reporting over secondary summaries.
3. If signals are suspicious or unresolved, stop and choose a safer version or ask the user.
4. After an intentional upgrade, keep the lockfile pinned and record the reason in the final summary.

## Lockfile Drift

- If lockfiles change because of an intentional reinstall, keep them when the package manager or repo policy expects updates.
- If lockfiles change unexpectedly during non-upgrade maintenance, inspect why before keeping them. Silent drift is a finding, not a cosmetic change.