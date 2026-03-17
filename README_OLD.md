# EBB Platform IA - Automation & Intelligence Layer

Central repository for AI-powered automation, orchestration, and documentation for Ebury Brazil operations.

This repository provides the **intelligence layer** above the business domains (located in `/Ebury-Brazil/`), implementing Skills, Subagents, Rules, MCPs, and OpenSpec methodology for spec-driven development.

## 🗂️ Workspace Structure

```
/home/marcosgomes/Projects/
├── ebb-platform-ia/            # THIS REPOSITORY
│   ├── openspec/               # Spec-Driven Development methodology
│   ├── skills/                 # AI automation skills
│   ├── subagents/              # Autonomous orchestration agents
│   ├── docs/                   # Documentation & guides
│   └── pendencias/             # Task tracking
│
└── Ebury-Brazil/               # BUSINESS DOMAINS REPOSITORY
    ├── ebb-client-journey/     # Customer journey, onboarding, compliance
    ├── ebb-money-flows/        # Payments, Pix, reconciliation
    ├── ebb-fx/                 # Foreign exchange
    ├── ebb-treasury/           # Treasury operations
    ├── ebb-platform/           # Infrastructure & IaC
    ├── ebb-ebury-connect/      # Ebury Connect integration
    └── ebb-bigdata/            # Data pipelines

```

## 📍 ebb-platform-ia/ (This Repository)

```
ebb-platform-ia/
```
ebb-platform-ia/
├── .github/                    # GitHub Actions & Copilot config
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
│   └── TEMPLATE_*.md           # Templates
├── subagents/                  # Autonomous Orchestrators
│   ├── database_diagnostic_agent.py
│   └── README.md
├── docs/                       # Documentation
│   └── RULES_SKILLS_MCPS_SUBAGENTS.md
└── README.md                   # This file
```

## 📍 Ebury-Brazil/ (Business Domains)

Located at: `/home/marcosgomes/Projects/Ebury-Brazil/`

```
Ebury-Brazil/
├── ebb-client-journey/         # Customer Journey Domain
│   ├── apps/
│   │   ├── temis/              # Core Temis platform
│   │   └── temis-registration-config-data-keys-salesforce/
│   └── gitops/                 # 30+ GitOps repositories
│
├── ebb-money-flows/            # Money Flows Domain
│   ├── apps/
│   │   ├── ebb-bexs-bacen-adapter/
│   │   ├── ebb-bexs-compliance/
│   │   ├── ebb-bexs-notification/
│   │   ├── ebb-bexs-statement/
│   │   ├── ebb-conciliacao/
│   │   └── ebb-pix-spi/
│   └── gitops/
│
├── ebb-fx/                     # Foreign Exchange Domain
│   └── forex-provider/
│
├── ebb-treasury/               # Treasury Domain
│   ├── ebb-treasury-configs-gitops/
│   ├── ebb-tree-compliance/
│   ├── ebb-tree-consumer/
│   ├── ebb-tree-producer/
│   └── ebb-tree-provider-mock/
│
├── ebb-platform/               # Platform & Infrastructure
│   ├── cicd/                   # CI/CD pipelines
│   ├── ebury-blueprints/       # Project templates
│   ├── engineering/            # Engineering tools
│   ├── iac/                    # Infrastructure as Code (19 projects)
│   ├── modules/                # Terraform modules
│   ├── templates/              # Service templates
│   └── tools/                  # DevOps utilities
│
├── ebb-ebury-connect/          # Ebury Connect Integration
│
└── ebb-bigdata/                # Data & Analytics
```

## 🎯 Business Domains Overview

| Domain | Apps | GitOps | Description |
|--------|------|--------|-------------|
| **client-journey** | 2 | 30+ | Onboarding, Compliance, Fraud, Risk |
| **money-flows** | 9+ | Multiple | Payments, Pix, Bacen, Reconciliation |
| **fx** | 1 | - | Foreign Exchange operations |
| **treasury** | 5 | - | Treasury & liquidity management |
| **platform** | - | - | Infrastructure, IaC, CI/CD |
| **ebury-connect** | - | - | Ebury platform integration |
| **bigdata** | - | - | Data pipelines & analytics |

## 🎯 Business Domains

| Domain | Description | Key Services |
|--------|-------------|--------------|
| **clientjourney** | Onboarding, Risk Assessment, Compliance, Fraud Detection | Temis suite (BFF, Bureau, Compliance, Fraud, Onboarding, Registration) |
| **fx** | Foreign Exchange trading and operations | Forex providers and adapters |
| **moneyflows** | Money movement, reconciliation, Bacen reporting | Pix, SPI, Account management, Bacen adapters |
| **platform** | Infrastructure, DevOps, and engineering tooling | ArgoCD, Terraform modules, CI/CD templates |
| **treasury** | Treasury and liquidity management | Tree compliance, producers, consumers |
| **webpayments** | Online payment capture and routing | Payment processors, notification adapters |

### 📑 Domain Index

<details>
<summary><b>clientjourney/</b> - Customer Journey & Compliance</summary>

#### Apps
- `temis/` - Core Temis platform
- `temis-registration-config-data-keys-salesforce/` - Salesforce integration config

#### GitOps (30 repositories)
**EBB Services:**
- `ebb-temis-bff-gitops/` - Backend for Frontend
- `ebb-temis-bureau-gitops/`, `ebb-temis-bureau-data-integrator-gitops/` - Bureau services
- `ebb-temis-compliance-gitops/`, `ebb-temis-compliance-action-gitops/`, `ebb-temis-compliance-screening-gitops/` - Compliance suite
- `ebb-temis-fraud-gitops/` - Fraud detection
- `ebb-temis-onboarding-engine-gitops/` - Onboarding orchestration
- `ebb-temis-registration-gitops/` - Customer registration
- `ebb-temis-risk-gitops/` - Risk assessment
- And 20+ more services...

**Specifications:** [openspec/specs/clientjourney.md](openspec/specs/clientjourney.md)
</details>

<details>
<summary><b>fx/</b> - Foreign Exchange</summary>

#### Apps
- `forex-provider/` - FX rate provider integration

**Specifications:** [openspec/specs/fx.md](openspec/specs/fx.md)
</details>

<details>
<summary><b>moneyflows/</b> - Money Movement & Reconciliation</summary>

#### Apps
- `ebb-bexs-*/` - Bexs platform integrations
- `ebb-pix-spi/` - Pix payment system
- `ebb-account/` - Account management
- Bacen adapters and reconciliation services

#### GitOps
- Multiple GitOps repositories for money flow services

**Specifications:** [openspec/specs/moneyflows.md](openspec/specs/moneyflows.md)
</details>

<details>
<summary><b>platform/</b> - Infrastructure & Engineering</summary>

#### Structure
- `cicd/` - CI/CD pipelines and templates
- `ebury-blueprints/` - Project templates and blueprints
- `engineering/` - Engineering tools and utilities
- `iac/` - Infrastructure as Code (19 Terraform/Terragrunt projects)
  - `ebb-iac-resource/` - Main resource definitions
  - `ebb-gke-shared/` - Shared GKE configurations
  - `ebb-iac-network/` - Network infrastructure
  - `ebb-iac-iam/` - IAM roles and service accounts
  - And 15+ more IaC projects
- `modules/` - Reusable Terraform modules
- `templates/` - Service and deployment templates
- `tools/` - DevOps and automation tools

**Specifications:** [openspec/specs/platform.md](openspec/specs/platform.md)
</details>

<details>
<summary><b>treasury/</b> - Treasury Operations</summary>

#### Apps & GitOps
- `ebb-treasury-configs-gitops/` - Treasury configurations
- `ebb-tree-compliance/` - Tree compliance service
- `ebb-tree-consumer/` - Tree consumer
- `ebb-tree-producer/` - Tree producer
- `ebb-tree-provider-mock/` - Tree provider mock

**Specifications:** [openspec/specs/treasury.md](openspec/specs/treasury.md)
</details>

<details>
<summary><b>webpayments/</b> - Web Payment Processing</summary>

#### Apps
- Payment capture applications
- Pricing engines
- Routing services

#### GitOps
- Payment processor GitOps configurations
- Notification adapter deployments

**Specifications:** [openspec/specs/webpayments.md](openspec/specs/webpayments.md)
</details>

<details>
<summary><b>data/</b> - Data Pipelines & Airflow</summary>

#### Structure
- `ebb-airflow-dags/` - Airflow DAGs for data pipelines
  - ETL processes
  - Data integration jobs
  - Scheduled data operations
- `helm_apache_airflow/` - Airflow Helm charts

</details>

<details>
<summary><b>openspec/</b> - Spec-Driven Development</summary>

#### Structure
- `specs/` - Stable domain specifications (6 domains)
- `changes/` - Active change specifications (delta specs)
- `archive/` - Completed change history
- `tasks.md` - Current task tracking
- `project.md` - Portfolio overview

**Methodology:** [OpenSpec Guide](openspec/README.md)
</details>

<details>
<summary><b>skills/</b> - AI Automation Skills</summary>

#### Available Skills
- `rdp_connect/` - Remote Desktop connection
- `ssh_connect/` - SSH connection
- `mysql_connect/` - MySQL database test
- `kubernetes_debug/` - K8s pod diagnostics
- `firestore_query/` - Firestore queries
- `k8s_pod_test/` - K8s pod testing

#### Templates
- `TEMPLATE_RULE.md` - Rule template
- `TEMPLATE_SKILL.md` - Skill template
- `TEMPLATE_MCP.md` - MCP template
- `TEMPLATE_SUBAGENT.md` - Subagent template

**Guide:** [Rules, Skills, MCPs & Subagents](docs/RULES_SKILLS_MCPS_SUBAGENTS.md)
</details>

<details>
<summary><b>subagents/</b> - Autonomous Agents</summary>

#### Available Subagents
- `database_diagnostic_agent.py` - Complete DB diagnostics orchestration

**Guide:** [Subagents README](subagents/README.md)
</details>

<details>
<summary><b>tools/</b> - General Utilities</summary>

#### Structure
- `firestore-test/` - Firestore testing utilities

</details>

## 📋 OpenSpec Methodology

This portfolio follows **OpenSpec**, a lightweight spec-driven development approach that ensures:

- ✅ **Continuous context**: AI assistant maintains business logic understanding
- ✅ **Delta-based changes**: Document only what changes (ADDED/MODIFIED/REMOVED)
- ✅ **Brownfield-first**: Works with existing codebases
- ✅ **Progressive rigor**: Detailed specs only when needed

### Quick Start with OpenSpec

1. **Read context**: Start with [`openspec/project.md`](openspec/project.md)
2. **Track work**: Maintain [`openspec/tasks.md`](openspec/tasks.md) as you work
3. **Document specs**: Write domain specifications in [`openspec/specs/`](openspec/specs/)
4. **Propose changes**: Create delta specs in [`openspec/changes/`](openspec/changes/) before major work

For detailed methodology, see:
- [`openspec/README.md`](openspec/README.md) - Workflow and structure
- [`openspec/OPENSPEC_METHODOLOGY_SUMMARY.md`](openspec/OPENSPEC_METHODOLOGY_SUMMARY.md) - Complete guide

## 🤖 AI Assistant Configuration

The workspace is configured for **Antigravity**, the GitHub Copilot assistant with custom instructions in [`.github/copilot-instructions.md`](.github/copilot-instructions.md).

Key behavioral rules include:
- Never merge directly to `main` (always use PRs)
- Never apply changes directly to GKE clusters (read-only operations only)
- GitOps modifications only in `ebb-dev`, `ebb-stg`, `ebb-prd` overlays
- All code comments must be in English
- Always use `southamerica-east1` region for GCP resources

## 🔧 Legacy Files (Deprecated)

The following files have been deprecated and consolidated into `.github/copilot-instructions.md`:
- ⚠️ `.clinerules` - Legacy AI instructions
- ⚠️ `.agent/workflows/overlay-rule.md` - Legacy workflow rules

These files remain for backward compatibility but should not be edited.

## 📚 Documentation

- [OpenSpec Configuration](openspec/config.yaml) - Domain definitions
- [Project Overview](openspec/project.md) - Portfolio architecture
- [Current Tasks](openspec/tasks.md) - Work in progress
- [Domain Specifications](openspec/specs/) - Per-domain technical specs

## 🎯 Skills & Subagents (AI Productivity)

This workspace implements **Rules, Skills, MCPs, and Subagents** concepts for AI-powered automation and productivity.

### Skills (Isolated Automations)

| Skill | Description | Usage |
|-------|-------------|-------|
| **rdp_connect** | Remote Desktop connection | `cd skills/rdp_connect && python main.py` |
| **ssh_connect** | Interactive SSH connection | `cd skills/ssh_connect && python main.py` |
| **mysql_connect** | MySQL connection test | `cd skills/mysql_connect && python main.py` |
| **kubernetes_debug** | K8s pod diagnostics | `cd skills/kubernetes_debug && python main.py <pod>` |

Each skill has:
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

- **Rules**: Governance and automation rules (see `skills/TEMPLATE_RULE.md`)
- **Skills**: Single-purpose automations with isolated dependencies
- **MCPs**: Model Context Protocols for skill integration (see `skills/TEMPLATE_MCP.md`)
- **Subagents**: Autonomous agents that orchestrate multiple skills (see `skills/TEMPLATE_SUBAGENT.md`)

📘 **[Complete Guide: Rules, Skills, MCPs & Subagents](docs/RULES_SKILLS_MCPS_SUBAGENTS.md)** - Detailed explanation of concepts, integration patterns, and usage examples

### Creating New Components

**New Skill:**
```bash
mkdir -p skills/my_skill/tests
cd skills/my_skill
cp ../TEMPLATE_SKILL.md README.md
# Edit main.py, requirements.txt, .env.example
```

**New Subagent:**
```bash
touch subagents/my_subagent.py
chmod +x subagents/my_subagent.py
cat skills/TEMPLATE_SUBAGENT.md  # Use as reference
```

## 🚀 Getting Started

1. Review the [project overview](openspec/project.md) to understand the portfolio
2. Check [current tasks](openspec/tasks.md) for active work
3. Read domain specifications in [`openspec/specs/`](openspec/specs/) for the area you're working on
4. Follow [OpenSpec workflow](openspec/README.md) for making changes

---

**Last Updated**: March 15, 2026  
**Maintained by**: Marcos Gomes  
**AI Assistant**: Antigravity (GitHub Copilot)
