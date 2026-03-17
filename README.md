# EBB Platform IA - Automation & Intelligence Layer

Central repository for AI-powered automation, orchestration, and documentation for Ebury Brazil operations.

This repository provides the **intelligence layer** above the business domains (located in `../Ebury-Brazil/`), implementing Skills, Subagents, Rules, MCPs, and OpenSpec methodology for spec-driven development.

---

## 🗂️ Workspace Structure

```
/home/marcosgomes/Projects/
├── ebb-platform-ia/            # THIS REPOSITORY - Intelligence Layer
│   ├── openspec/               # Spec-Driven Development methodology
│   ├── skills/                 # AI automation skills  
│   ├── subagents/              # Autonomous orchestration agents
│   ├── docs/                   # Documentation & guides
│   └── pendencias/             # Task tracking
│
└── Ebury-Brazil/               # BUSINESS DOMAINS - Application Layer
    ├── ebb-client-journey/     # Customer journey, onboarding, compliance
    ├── ebb-money-flows/        # Payments, Pix, reconciliation
    ├── ebb-fx/                 # Foreign exchange
    ├── ebb-treasury/           # Treasury operations
    ├── ebb-platform/           # Infrastructure & IaC
    ├── ebb-ebury-connect/      # Ebury Connect integration
    └── ebb-bigdata/            # Data pipelines
```

---

## 📍 ebb-platform-ia Structure (This Repository)

```
ebb-platform-ia/
├── .github/                    # GitHub Actions & Copilot configuration
├── openspec/                   # Spec-Driven Development
│   ├── specs/                  # Domain specifications
│   ├── changes/                # Active change specs (delta)
│   ├── archive/                # Completed changes
│   ├── tasks.md                # Current tasks
│   └── README.md               # OpenSpec methodology
├── skills/                     # AI Automation Skills
│   ├── rdp_connect/
│   ├── ssh_connect/
│   ├── mysql_connect/
│   ├── kubernetes_debug/
│   └── TEMPLATE_*.md           # Templates for new components
├── subagents/                  # Autonomous Orchestrators
│   ├── database_diagnostic_agent.py
│   └── README.md
├── docs/                       # Documentation
│   └── RULES_SKILLS_MCPS_SUBAGENTS.md
├── pendencias/                 # Task tracking
└── README.md                   # This file
```

---

## 🎯 Ebury-Brazil Business Domains

Located at: `/home/marcosgomes/Projects/Ebury-Brazil/`

| Domain | Description | Apps | GitOps |
|--------|-------------|------|--------|
| **ebb-client-journey** | Onboarding, Compliance, Fraud, Risk | 2 (Temis suite) | 30+ repos |
| **ebb-money-flows** | Payments, Pix, Bacen, Reconciliation | 9+ apps | Multiple repos |
| **ebb-fx** | Foreign Exchange operations | forex-provider | - |
| **ebb-treasury** | Treasury & liquidity management | 5 services | Configs |
| **ebb-platform** | Infrastructure, IaC, CI/CD | - | - |
| **ebb-ebury-connect** | Ebury platform integration | - | - |
| **ebb-bigdata** | Data pipelines & analytics | - | - |

📚 **Full domain specifications:** [openspec/specs/](openspec/specs/)

---

## 📋 OpenSpec Methodology

This workspace follows **OpenSpec**, a lightweight spec-driven development approach:

- ✅ **Continuous context**: AI assistant maintains business logic understanding
- ✅ **Delta-based changes**: Document only what changes (ADDED/MODIFIED/REMOVED)
- ✅ **Brownfield-first**: Works with existing codebases
- ✅ **Progressive rigor**: Detailed specs only when needed

### Quick Start

1. **Read context**: [`openspec/project.md`](openspec/project.md)
2. **Track work**: [`openspec/tasks.md`](openspec/tasks.md)
3. **Document specs**: [`openspec/specs/`](openspec/specs/)
4. **Propose changes**: [`openspec/changes/`](openspec/changes/)

📖 **Full guide:** [openspec/README.md](openspec/README.md) | [openspec/OPENSPEC_METHODOLOGY_SUMMARY.md](openspec/OPENSPEC_METHODOLOGY_SUMMARY.md)

---

## 🎯 Skills & Subagents (AI Productivity)

Implementation of **Rules, Skills, MCPs, and Subagents** for AI-powered automation.

### Skills (Isolated Automations)

| Skill | Description | Usage |
|-------|-------------|-------|
| **rdp_connect** | Remote Desktop connection | `cd skills/rdp_connect && python main.py` |
| **ssh_connect** | Interactive SSH connection | `cd skills/ssh_connect && python main.py` |
| **mysql_connect** | MySQL connection test | `cd skills/mysql_connect && python main.py` |
| **kubernetes_debug** | K8s pod diagnostics | `cd skills/kubernetes_debug && python main.py <pod>` |

Each skill includes:
- `main.py` - Core logic
- `requirements.txt` - Isolated dependencies
- `.env.example` - Configuration template
- `README.md` - Usage documentation
- `tests/` - Test suite

### Subagents (Autonomous Orchestrators)

| Subagent | Description | Skills Orchestrated |
|----------|-------------|---------------------|
| **database_diagnostic** | Complete DB diagnostics | ssh_connect + mysql_connect + k8s_debug |

**Usage:**
```bash
python subagents/database_diagnostic_agent.py
```

### Core Concepts

- **Rules**: Governance and automation rules
- **Skills**: Single-purpose automations with isolated dependencies
- **MCPs**: Model Context Protocols for skill integration
- **Subagents**: Autonomous agents that orchestrate multiple skills

📘 **[Complete Guide: Rules, Skills, MCPs & Subagents](docs/RULES_SKILLS_MCPS_SUBAGENTS.md)**

### Templates

Create new components using templates in `skills/`:
- `TEMPLATE_RULE.md` - Rule template
- `TEMPLATE_SKILL.md` - Skill template
- `TEMPLATE_MCP.md` - MCP template
- `TEMPLATE_SUBAGENT.md` - Subagent template

---

## 🚀 Quick Start

### 1. Setup Python Environment

```bash
# Navigate to repository
cd /home/marcosgomes/Projects/ebb-platform-ia

# Create and activate venv (if not exists)
python -m venv .venv
source .venv/bin/activate

# Install dependencies for a specific skill
cd skills/kubernetes_debug
pip install -r requirements.txt
```

### 2. Configure Environment

Each skill has its own `.env`. Use `.env.example` as template:

```bash
cd skills/mysql_connect
cp .env.example .env
# Edit .env with real values
```

### 3. Run a Skill

```bash
cd skills/kubernetes_debug
python main.py ebb-account core
```

### 4. Run a Subagent

```bash
python subagents/database_diagnostic_agent.py
```

---

## 🛠️ Creating New Components

### New Skill

```bash
# Create structure
mkdir -p skills/my_skill/tests
cd skills/my_skill

# Use template
cp ../TEMPLATE_SKILL.md README.md

# Create files
touch main.py requirements.txt .env.example
```

### New Subagent

```bash
# Create file
touch subagents/my_subagent.py
chmod +x subagents/my_subagent.py

# Use template as reference
cat skills/TEMPLATE_SUBAGENT.md
```

---

## 🤖 AI Assistant Configuration

Configured for **GitHub Copilot** with custom instructions in [`.github/copilot-instructions.md`](.github/copilot-instructions.md).

Key behavioral rules:
- Never merge directly to `main` (always use PRs)
- Never apply changes directly to GKE clusters (read-only)
- GitOps modifications only in `ebb-dev`, `ebb-stg`, `ebb-prd` overlays
- All code comments in English
- Always use `southamerica-east1` region for GCP resources

---

## 📚 Documentation

- [OpenSpec Methodology](openspec/README.md)
- [Rules, Skills, MCPs & Subagents Guide](docs/RULES_SKILLS_MCPS_SUBAGENTS.md)
- [Domain Specifications](openspec/specs/)
- [Current Tasks](openspec/tasks.md)

---

## 🔐 Security

- **NEVER** commit `.env`, `.pem`, `.key`, `credentials*.yaml` files
- Always use `.env.example` with fake values
- Rotate secrets regularly
- Use Secret Manager GCP for production

---

**Last Updated**: March 16, 2026  
**Maintained by**: Marcos Gomes  
**AI Assistant**: GitHub Copilot
