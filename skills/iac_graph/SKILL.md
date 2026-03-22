---
name: iac_graph
description: >
  Generate an interactive HTML dependency graph from a Terragrunt IAC monorepo (ebb-ebury-connect/dev).
  Scans HCL files to extract IAM roles, service accounts, workload identity bindings, and pub/sub subscriptions.
  Renders a styled, clickable SVG graph with a canvas focus mode: clicking a service account node shows its
  general_privilege and least_privilege roles, downstream subscriptions, and sub-role edges.
  Use when the user asks to "visualize IAC dependencies", "show IAC graph", "generate dependency map",
  "who uses this SA", "what roles does this service have", or "show iam graph for ebury-connect".
  Outputs a self-contained HTML file with dark theme, minimap, permission debug panel, zoom/pan, and focus canvas.
license: CC-BY-4.0
metadata:
  author: Marcos Gomes
  version: 1.0.0
  requires:
    - graphviz (dot binary)
    - python3
    - terragrunt
  gcp_projects:
    - ebb-ebury-connect-dev
---

# IAC Dependency Graph Skill

Generates an interactive HTML visualization of Terragrunt module dependencies for the `ebb-ebury-connect/dev` IAC monorepo.

## When to Use

- Visualize all dependencies between IAM roles, service accounts, pub/sub topics, subscriptions, Cloud Run, and Cloud SQL
- Debug "which SA has access to what" — shows `general_privilege` and `least_privilege` roles
- Understand workload identity bindings (K8s SA → GCP SA)
- Trace pub/sub subscription → SA → role chains
- On-call investigation: "who published to this topic?" or "which service reads from this sub?"

## Pipeline

```bash
cd /home/marcosgomes/Projects/Ebury-Brazil/ebb-platform/iac/ebb-iac-resource/ebb-ebury-connect/dev
terragrunt dag graph 2>/dev/null \
  | python3 filter_graph.py \
  | python3 svg_to_html.py > /tmp/ebb-graph.html
xdg-open /tmp/ebb-graph.html
```

## Scripts

| File | Purpose |
|------|---------|
| `filter_graph.py` | Reads Terragrunt DAG stdout + scans HCL files → emits styled DOT + writes `/tmp/ebb-perm-data.json` |
| `svg_to_html.py` | Reads DOT from stdin → `dot -Tsvg` → injects SVG + permission data into HTML template |
| `svg_template.html` | Full interactive HTML template (dark theme, canvas focus, permission panel) |

## Features

- **Node clustering** — IAM Roles (yellow), Service Accounts (blue), Pub/Sub (green), Cloud Run (orange), etc.
- **Focus mode** — Click a node to see only its direct connections in a clean canvas overlay
- **For SA nodes**: shows upstream `general_privilege_role`, downstream subscriptions, and `least_privilege_role` nodes (via subscription edges)
- **Permission debug panel** — workload identity bindings, IAM roles+permissions, services running as this SA
- **Zoom/pan** — scroll to zoom, drag to pan in both full graph and focus mode
- **Minimap** — always-visible overview with viewport indicator

## Architecture Notes

- SAs hold `general_privilege_role` directly via `project_roles` in their HCL
- `least_privilege_role` is NOT directly on the SA — it is attached to subscriptions that use the SA as push/pull identity
- The canvas focus mode shows both role types when clicking a SA: upstream (general) + sub-role row (least-privilege)
- HCL scanner reads `iam/roles/`, `iam/service-accounts/`, and `pub-sub/subscriptions/` directories
