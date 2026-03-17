---
description: Rule for GitOps overlay updates
---

# ⚠️ DEPRECATED - This file has been moved

This rule has been integrated into `.github/copilot-instructions.md` following GitHub Copilot best practices.

Please refer to: `/home/marcosgomes/Projects/.github/copilot-instructions.md`

---

When applying GitOps configurations or refinements, strictly adhere to the following rule:

# STRICT Overlay Update Constraint

> [!IMPORTANT]
> **Overlays ONLY**: 
> - Modifications are PERMITTED ONLY within `overlays/ebb-dev`, `overlays/ebb-stg`, and `overlays/ebb-prd` directories.
> - Modifications are STRICTLY FORBIDDEN in the following directories:
>     - `base/`
>     - `application/`
>     - Any other overlay not starting with `ebb-` (e.g., `staging`, `production`, `sandbox`).
> 
> **Handling Shared Config**: If a configuration (like `namespace`) needs to be set for the `ebb-*` family, it must be explicitly defined in EACH separate overlay's `kustomization.yaml`, even if it repeats. Never modify the `base` to achieve this.

# Process
1. Verify the current directory structure.
2. Revert any accidental changes to `base` or `application`.
3. Apply all environment-specific logic, namespaces, and labels exclusively within the `ebb-dev`, `ebb-stg`, and `ebb-prd` overlays.
