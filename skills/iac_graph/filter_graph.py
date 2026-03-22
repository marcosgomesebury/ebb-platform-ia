import sys
import re
import os
import json

raw = sys.stdin.read()

# ── IAM HCL Scanner ───────────────────────────────────────────────────────────
def scan_iam_data(base_dir):
    data = {"sas": {}, "roles": {}}

    def read_hcl(path):
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                return f.read()
        except Exception:
            return ""

    def resolve_dep(hcl_dir, config_path):
        abs_p = os.path.normpath(os.path.join(hcl_dir, config_path))
        return os.path.relpath(abs_p, base_dir).replace(os.sep, "/")

    # ── Scan roles ────────────────────────────────────────────────────────────
    roles_dir = os.path.join(base_dir, "iam", "roles")
    if os.path.exists(roles_dir):
        for role_name in sorted(os.listdir(roles_dir)):
            hcl_path = os.path.join(roles_dir, role_name, "terragrunt.hcl")
            if not os.path.isfile(hcl_path):
                continue
            content = read_hcl(hcl_path)
            # permissions list: find each individual "permission.string" in the permissions = [...] block
            # Use a two-step approach to avoid bracket-nesting issues
            perm_block_m = re.search(r'permissions\s*=\s*\[([^\]]+)\]', content, re.DOTALL)
            perms = re.findall(r'"([a-z][a-zA-Z0-9.]+\.[a-zA-Z][a-zA-Z0-9]+)"',
                               perm_block_m.group(1)) if perm_block_m else []
            rid_m = re.search(r'role_id\s*=\s*"([^"]+)"', content)
            data["roles"][f"iam/roles/{role_name}"] = {
                "role_id": rid_m.group(1) if rid_m else role_name,
                "permissions": perms,
            }

    # ── Scan service accounts ─────────────────────────────────────────────────
    sa_dir = os.path.join(base_dir, "iam", "service-accounts")
    if os.path.exists(sa_dir):
        for sa_name in sorted(os.listdir(sa_dir)):
            hcl_path = os.path.join(sa_dir, sa_name, "terragrunt.hcl")
            if not os.path.isfile(hcl_path):
                continue
            content = read_hcl(hcl_path)
            hcl_dir  = os.path.dirname(os.path.abspath(hcl_path))
            sa_key   = f"iam/service-accounts/{sa_name}"

            # Dependency blocks: name → resolved node ID
            deps = {}
            for dep_name, dep_path in re.findall(
                r'dependency\s+"([^"]+)"\s*\{[^}]*config_path\s*=\s*"([^"]+)"',
                content, re.DOTALL
            ):
                deps[dep_name] = resolve_dep(hcl_dir, dep_path)

            # Workload Identity: look for svc.id.goog[ns/ksa] anywhere in the file
            wi_bindings = []
            for full_member in re.findall(
                r'serviceAccount:[^"]*\.svc\.id\.goog\[([^\]]+)\]', content
            ):
                wi_bindings.append({"ksa": full_member})

            # Project IAM roles: search for block between "project_iam_members" and
            # the matching closing ] — we scan line by line to avoid bracket confusion
            project_roles = []
            in_block = False
            brace_depth = 0
            entry_lines = []
            for line in content.splitlines():
                if not in_block:
                    if re.search(r'project_iam_members\s*=\s*\[', line):
                        in_block = True
                        brace_depth = 0
                        entry_lines = []
                else:
                    stripped = line.strip()
                    if stripped == '{':
                        brace_depth += 1
                        entry_lines = []
                    elif stripped in ('}', '},'):
                        brace_depth -= 1
                        if brace_depth == 0:
                            # Parse this entry
                            entry_text = "\n".join(entry_lines)
                            # literal role string
                            lit = re.search(r'role\s*=\s*"([^"]+)"', entry_text)
                            if lit:
                                project_roles.append({"role": lit.group(1), "permissions": []})
                            else:
                                # dependency reference
                                dep_ref = re.search(r'role\s*=\s*dependency\.(\w+)\.', entry_text)
                                if dep_ref:
                                    dep_key  = dep_ref.group(1)
                                    role_node = deps.get(dep_key, "")
                                    perms    = data["roles"].get(role_node, {}).get("permissions", [])
                                    role_id  = data["roles"].get(role_node, {}).get("role_id", dep_key)
                                    project_roles.append({"role": role_id, "node": role_node, "permissions": perms})
                            entry_lines = []
                    elif stripped == ']' and brace_depth == 0:
                        in_block = False
                    else:
                        entry_lines.append(line)

            data["sas"][sa_key] = {"wi": wi_bindings, "project_roles": project_roles}

    # ── Scan pub-sub subscriptions (they hold least_privilege roles) ──────────
    # Each sub HCL: dependency → least_privilege_role, and the sub is linked
    # to a SA via the role name convention (ebb_wp_X_least_privilege = SA ebb-wp-X)
    pubsub_dir = os.path.join(base_dir, "pub-sub", "subscriptions")
    if os.path.exists(pubsub_dir):
        for sub_name in sorted(os.listdir(pubsub_dir)):
            hcl_path = os.path.join(pubsub_dir, sub_name, "terragrunt.hcl")
            if not os.path.isfile(hcl_path):
                continue
            content = read_hcl(hcl_path)
            hcl_dir = os.path.dirname(os.path.abspath(hcl_path))
            sub_key = f"pub-sub/subscriptions/{sub_name}"

            # Collect all dependency role references
            deps = {}
            for dep_name, dep_path in re.findall(
                r'dependency\s+"([^"]+)"\s*\{[^}]*config_path\s*=\s*"([^"]+)"',
                content, re.DOTALL
            ):
                deps[dep_name] = resolve_dep(hcl_dir, dep_path)

            # Collect all iam_members entries that reference a role dependency
            sub_roles = []
            in_block, brace_depth, entry_lines = False, 0, []
            for line in content.splitlines():
                stripped = line.strip()
                if not in_block:
                    if re.search(r'iam_members\s*=\s*\[', line):
                        in_block = True; brace_depth = 0; entry_lines = []
                else:
                    if stripped == '{': brace_depth += 1; entry_lines = []
                    elif stripped in ('}', '},'):
                        brace_depth -= 1
                        if brace_depth == 0:
                            entry_text = "\n".join(entry_lines)
                            dep_ref = re.search(r'role\s*=\s*dependency\.(\w+)\.', entry_text)
                            if dep_ref:
                                dep_key   = dep_ref.group(1)
                                role_node = deps.get(dep_key, "")
                                perms     = data["roles"].get(role_node, {}).get("permissions", [])
                                role_id   = data["roles"].get(role_node, {}).get("role_id", dep_key)
                                sub_roles.append({"role": role_id, "node": role_node, "permissions": perms})
                            entry_lines = []
                    elif stripped == ']' and brace_depth == 0:
                        in_block = False
                    else:
                        entry_lines.append(line)

            if sub_roles:
                data.setdefault("sub_roles", {})[sub_key] = sub_roles

    return data



# Scan HCL data from cwd (the IAC base directory)
iam_data = scan_iam_data(os.getcwd())
try:
    with open("/tmp/ebb-perm-data.json", "w") as f:
        json.dump(iam_data, f)
except Exception:
    pass


# Rejoin lines wrapped mid-token by terragrunt
joined_lines = []
buf = ""
for line in raw.split("\n"):
    stripped = line.strip()
    if not stripped:
        continue
    buf = (buf + " " + stripped).strip() if buf else stripped
    if stripped.endswith(";") or stripped in ("{", "}") or stripped == "digraph {":
        joined_lines.append(buf)
        buf = ""
if buf:
    joined_lines.append(buf)

edges = []
all_nodes = set()

for line in joined_lines:
    line = line.strip()
    if "->" in line:
        match = re.match(r'"(.+?)"\s*->\s*"(.+?)"', line)
        if match:
            src, dst = match.group(1), match.group(2)
            edges.append((src, dst))
            all_nodes.add(src)
            all_nodes.add(dst)
    elif line.startswith('"') and line.endswith('" ;'):
        match = re.match(r'"(.+?)"', line)
        if match:
            all_nodes.add(match.group(1))

# Short label: last 2 path segments
def short(n):
    parts = n.split("/")
    return "\\n".join(parts[-2:]) if len(parts) >= 2 else n

# Lineage tiers: left-to-right flow of dependency
# (tier, cluster_id, label, bg_color, fill_color, font_color, predicate)
TIERS = [
    (0, "roles",    "IAM Roles",              "#2d2006", "#FBBC04", "#1e1e2e", lambda n: "iam/roles" in n),
    (0, "sa",       "Service Accounts",       "#0d1f3a", "#4285F4", "white",   lambda n: "service-accounts" in n),
    (0, "artifact", "Artifact Registry",      "#1a0d2e", "#7c3aed", "white",   lambda n: "artifact-registry" in n),
    (1, "topics",   "Pub/Sub Topics",         "#062010", "#34A853", "white",   lambda n: "pub-sub/topics" in n),
    (1, "subs",     "Pub/Sub Subscriptions",  "#0d2106", "#7CB342", "white",   lambda n: "pub-sub/subscriptions" in n),
    (2, "run",      "Cloud Run",              "#2a1000", "#FF6D00", "white",   lambda n: "cloud-run" in n),
    (2, "sched",    "Cloud Scheduler",        "#1a0a2a", "#9C27B0", "white",   lambda n: "cloud-scheduler" in n),
    (2, "gcs",      "Cloud Storage",          "#2a0606", "#EA4335", "white",   lambda n: "cloud-storage" in n),
    (3, "sql",      "Cloud SQL",              "#062020", "#00BCD4", "white",   lambda n: "cloud-sql" in n),
    (3, "compute",  "Compute Engine",         "#1a1a06", "#CDDC39", "#1e1e2e", lambda n: "compute-engine" in n),
    (3, "firestore","Firestore",              "#06201a", "#00897B", "white",   lambda n: "firestore" in n),
    (3, "other",    "Other",                  "#1e1e2e", "#585b70", "white",   lambda n: True),
]

def get_tier(n):
    for tier, cid, label, bg, fill, fc, pred in TIERS:
        if pred(n):
            return (tier, cid, label, bg, fill, fc)
    return (3, "other", "Other", "#1e1e2e", "#585b70", "white")

# Group nodes into clusters
clusters = {}
for n in sorted(all_nodes):
    key = get_tier(n)
    clusters.setdefault(key, []).append(n)

print('digraph {')
print('  graph [')
print('    bgcolor="#11111b"')
print('    fontname="Helvetica"')
print('    fontcolor="#cdd6f4"')
print('    fontsize=14')
print('    splines=curved')
print('    nodesep=0.55')
print('    ranksep=1.8')
print('    rankdir=TB')
print('    pad=1.0')
print('    concentrate=true')
print('  ];')
print('  node [')
print('    shape=box')
print('    style="filled,rounded"')
print('    fontname="Helvetica"')
print('    fontsize=11')
print('    margin="0.22,0.14"')
print('    penwidth=0')
print('    width=2.0')
print('  ];')
print('  edge [')
print('    color="#3a3a5a"')
print('    arrowsize=0.7')
print('    penwidth=1.2')
print('  ];')

# Emit clusters sorted by tier
for (tier, cid, label, bg, fill, fc), cnodes in sorted(clusters.items()):
    if not cnodes:
        continue
    print(f'  subgraph cluster_{cid} {{')
    print(f'    label="{label}"')
    print(f'    style="filled,rounded"')
    print(f'    fillcolor="{bg}"')
    print(f'    color="{fill}40"')
    print(f'    fontcolor="{fill}"')
    print(f'    fontsize=13')
    print(f'    fontname="Helvetica-Bold"')
    print(f'    margin=20')
    for n in sorted(cnodes):
        lbl = short(n)
        print(f'    "{n}" [label="{lbl}", fillcolor="{fill}", fontcolor="{fc}", tooltip="{n}"];')
    print('  }')

# SA nodes at the top; let everything else flow naturally from edges
sa_nodes = [n for n in all_nodes if "service-accounts" in n]
if sa_nodes:
    nlist = " ".join(f'"{n}"' for n in sorted(sa_nodes))
    print(f'  {{ rank=min; {nlist} }}')

for src, dst in edges:
    print(f'  "{src}" -> "{dst}";')

print('}')

