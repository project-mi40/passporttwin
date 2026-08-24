# Contributing to PassportTwin

This project has two contributors: Alexander Castillo (Track A) and Pau Modolell Rodríguez
(Track B). This document exists so both of you follow the same conventions without needing
to re-negotiate them every sprint.

## Branching

- `main` — always runnable via `docker compose up`. Never commit directly to `main`.
- `track-a/<feature>` — Alexander's working branches (e.g. `track-a/aas-submodel-nameplate`).
- `track-b/<feature>` — Pau's working branches (e.g. `track-b/drift-model-v1`).
- Open a Pull Request into `main` when a feature meets the Definition of Done (see README).

## Commit messages

Use a short prefix indicating the layer, matching the architecture (L1–L6):

```
[L3] Add Nameplate AAS submodel schema
[L4] Implement drift regression baseline
[docs] Add ADR-004: Power BI vs Grafana split
```

## Pull Requests

- Reference the related backlog task (Notion) in the PR description.
- At least one of you reviews the other's PR before merging, even informally.
- The PR template in `.github/PULL_REQUEST_TEMPLATE.md` is filled in automatically — complete it.

## Sprint discipline

- Every sprint ends with an integration point: both tracks' work must run together via
  `docker compose up`, even if functionality is partial.
- If a feature isn't ready by sprint end, it stays on its branch — `main` is never broken
  for a demo.
