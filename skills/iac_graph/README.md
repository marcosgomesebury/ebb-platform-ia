# Skill: IAC Dependency Graph

Generates a self-contained interactive HTML visualization of Terragrunt IAC dependencies for the `ebb-ebury-connect/dev` monorepo.

## Usage

```bash
cd /home/marcosgomes/Projects/Ebury-Brazil/ebb-platform/iac/ebb-iac-resource/ebb-ebury-connect/dev

terragrunt dag graph 2>/dev/null \
  | python3 /path/to/filter_graph.py \
  | python3 /path/to/svg_to_html.py > /tmp/ebb-graph.html

xdg-open /tmp/ebb-graph.html
```

## Requirements

- `graphviz` installed (`apt install graphviz`)
- `terragrunt` configured and authenticated
- Run from the IAC monorepo root (e.g. `ebb-ebury-connect/dev`)

## What It Shows

- **IAM Roles** (yellow) — `general_privilege` and `least_privilege` roles
- **Service Accounts** (blue) — GCP SAs with workload identity info
- **Pub/Sub Topics + Subscriptions** (green)
- **Cloud Run** (orange), **Cloud Scheduler** (purple), **Cloud SQL** (cyan), **Cloud Storage** (red)

## Interaction

| Action | Result |
|--------|--------|
| Click a node | Focus canvas: shows only directly connected nodes |
| Click a SA | Shows `general_privilege` (above), subscriptions (middle), `least_privilege` via subs (bottom row 🔑) |
| Scroll | Zoom in/out |
| Drag | Pan |
| Esc | Return to full graph |
| Click info panel → 🔑/🛡️/🚀 | See WI binding, IAM roles, runners for that SA |

## Files

- `filter_graph.py` — Processes Terragrunt DOT output and scans HCL files for IAM metadata
- `svg_to_html.py` — Converts DOT to SVG and injects into the HTML template
- `svg_template.html` — Self-contained dark-themed interactive HTML template
