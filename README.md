<div align="center">

<img src="https://capsule-render.vercel.app/api?type=cylinder&color=0:0d1117,40:0E5484,100:062e52&height=200&section=header&text=Chetan%20Biranje&fontSize=50&fontColor=ffffff&fontAlignY=45&animation=fadeIn&desc=DevSecOps%20Engineer%20%7C%20AppSec%20%7C%20Bug%20Hunter&descAlignY=68&descColor=58a6ff&descSize=16" width="100%"/>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=13&duration=2500&pause=800&color=58a6ff&center=true&vCenter=true&multiline=true&repeat=true&width=700&height=55&lines=shadex%40kali%3A~%24+cat+pipeline.yaml+%7C+grep+%22security%22;%E2%86%92+SAST+%7C+SCA+%7C+Secrets+%7C+DAST+%7C+Container+%7C+IaC+%E2%86%92+SHIFT+LEFT" />

<br/>

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/chetanbiranje)
[![HackerOne](https://img.shields.io/badge/HackerOne-494649?style=for-the-badge&logo=hackerone&logoColor=white)](https://hackerone.com/chetanbiranje)
[![Bugcrowd](https://img.shields.io/badge/Bugcrowd-F26822?style=for-the-badge&logo=bugcrowd&logoColor=white)](https://bugcrowd.com/chetanbiranje)
[![Email](https://img.shields.io/badge/ProtonMail-8B89CC?style=for-the-badge&logo=protonmail&logoColor=white)](mailto:chetanbiranje@proton.me)
[![Portfolio](https://img.shields.io/badge/Portfolio-000000?style=for-the-badge&logo=replit&logoColor=white)](https://ChetanBiranje.replit.app)

</div>

---

## `$ cat identity.yaml`

```yaml
apiVersion: devsecops/v1
kind: Engineer
metadata:
  name: Chetan Biranje
  handles: [Chetan-Biranje, mr-Shadex]
  location: Pune, Maharashtra, India
  education: BCA @ D.Y. Patil University (2025–2028)

spec:
  current_roles:
    - title: Cyber Security Analyst
      org: ElevanceSkills
      since: Apr 2026
    - title: Full-Stack Developer (AppSec)
      org: AI4See Private Ltd
      since: Dec 2025

  focus_areas:
    - DevSecOps Pipeline Hardening (SAST · SCA · DAST · Secrets · IaC)
    - Web & API Penetration Testing (OWASP Top 10 · API Top 10)
    - Android Mobile Security (JADX · MobSF · Frida)
    - Bug Bounty — HackerOne · Bugcrowd · Intigriti

  notable: "WAF bypass on staging.valmo.in → Acknowledged by Meesho Security Team"
```

---

## `$ kubectl describe pipeline secure-ci-cd`

```
NAME: secure-ci-cd  |  STAGES: 8  |  STATUS: Running ✓

┌─────────────────────────────────────────────────────────────────────────┐
│                      DEVSECOPS CI/CD PIPELINE                           │
│                                                                         │
│  [1]        [2]       [3]        [4]       [5]       [6]    [7]  [8]   │
│  SAST   →  SCA   →  Secrets →  DAST   →  Container→ IaC → Sign→ Deploy│
│  Semgrep   pip-      Gitleaks   OWASP     Trivy      tfsec  Cosign      │
│  Bandit    audit     detect-    ZAP       Snyk       Check-             │
│  CodeQL    Safety    secrets               scan      kov                │
│                                                                         │
│  Security debt reduced ~40% · Vuln surface reduced ~30%                │
└─────────────────────────────────────────────────────────────────────────┘
```

**Tools per stage:**

| Stage | Tool | What it catches |
|---|---|---|
| SAST | Semgrep · Bandit · CodeQL | Code-level vulns, insecure patterns |
| SCA | pip-audit · Safety · npm audit | Vulnerable dependencies |
| Secrets | Gitleaks · detect-secrets | Hardcoded keys, tokens, creds |
| DAST | OWASP ZAP | Runtime vulns — XSS, SQLi, auth |
| Container | Trivy · Snyk | CVEs in base images & packages |
| IaC | tfsec · Checkov | Terraform / Ansible misconfigs |
| Sign | Cosign | Supply chain integrity |
| Deploy | Least-privilege IAM | Zero standing privileges |

---

## `$ terraform show infrastructure.tf`

```hcl
# Production Infrastructure — AI4See
resource "aws_eks_cluster" "prod" {
  # Kubernetes on EKS — CIS Level 2 hardened via Ansible
  # Least-privilege IAM roles per workload
  # S3 with encryption-at-rest + bucket policies
  # Docker containers hardened — non-root, read-only FS
}

# Security Posture
# ├── IAM: Zero standing admin privileges
# ├── Networking: Private subnets, SGs, NACLs
# ├── Secrets: AWS Secrets Manager (no env vars)
# └── Logging: CloudTrail + GuardDuty enabled
```

---

## `$ ls -la repositories/ --devsecops`

| Repository | Description | Stack |
|---|---|---|
| [⚙️ DevSecOps Learning Lab](https://github.com/Chetan-Biranje/devsecops-learning-lab) | 8-stage CI/CD · EKS via Terraform · Ansible CIS L2 · SAST/DAST | Flask · K8s · Terraform · Ansible |
| [🚦 Secure CI/CD Pipeline](https://github.com/Chetan-Biranje/secure-pipeline) | Least-privilege pipeline · SAST · SCA · secrets gates blocking insecure builds | GitHub Actions |
| [🔐 PySecUtils](https://github.com/Chetan-Biranje/python-security-utilities) | 17 security classes · AES-256-GCM · JWT · 40+ tests · PyPI-ready | Python |
| [🔍 Security Recon Toolkit](https://github.com/Chetan-Biranje/security-recon-toolkit) | 7-module CLI · subdomain enum · JS secrets · CVE lookup · HTML reports | Python |
| [🛡️ Threat Modeling Notes](https://github.com/Chetan-Biranje/threat-modeling-notes) | STRIDE templates · OWASP ASVS checklists · worked examples | Markdown |
| [🔎 Bug Bounty Recon Scripts](https://github.com/Chetan-Biranje/bug-bounty-recon-scripts) | Subdomain enum · JS analysis · API discovery · IDOR finder | Python · Bash |
| [🗺️ 365 Days AppSec Roadmap](https://github.com/Chetan-Biranje/365DaysOfApplicationSecurityRoadmap) | Day-by-day roadmap · 200+ free resources · 7 phases | Open Source |

---

## `$ cat toolchain.conf --category=devsecops`

<div align="center">

![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=flat-square&logo=terraform&logoColor=white)
![Ansible](https://img.shields.io/badge/Ansible-EE0000?style=flat-square&logo=ansible&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-FF9900?style=flat-square&logo=amazon-aws&logoColor=white)
![Semgrep](https://img.shields.io/badge/Semgrep-1E90FF?style=flat-square&logoColor=white)
![Bandit](https://img.shields.io/badge/Bandit-3776AB?style=flat-square&logo=python&logoColor=white)
![OWASP ZAP](https://img.shields.io/badge/OWASP_ZAP-00549E?style=flat-square&logo=owasp&logoColor=white)
![Trivy](https://img.shields.io/badge/Trivy-1904DA?style=flat-square&logoColor=white)
![Gitleaks](https://img.shields.io/badge/Gitleaks-F05032?style=flat-square&logo=git&logoColor=white)
![Burp Suite](https://img.shields.io/badge/Burp_Suite-FF6633?style=flat-square&logoColor=white)
![Nuclei](https://img.shields.io/badge/Nuclei-00BCD4?style=flat-square&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-4EAA25?style=flat-square&logo=gnu-bash&logoColor=white)

</div>

---

## `$ ./recon.sh --show bug-bounty-findings`

> Verified findings — no unconfirmed claims listed.

```
[ACKNOWLEDGED] WAF Bypass — staging.valmo.in          → Meesho Security Team ✓
[VALID]        IDOR / Broken Object-Level Auth          → HackerOne ✓
[VALID]        JWT Algorithm Confusion                   → Intigriti ✓
[VALID]        Broken Access Control                     → Bugcrowd ✓
[VALID]        SSRF — Internal API Endpoint Exposure     → Intigriti ✓
[VALID]        Business Logic — Checkout Bypass          → HackerOne ✓
[ACTIVE]       CVE-2025-55182 surface on OpenAI assets   → In progress
```

**Active programs:** Meesho · DoorDash · Platacard · Flipkart · Myntra · Robinhood

---

## `$ github-stats --user Chetan-Biranje`

<div align="center">

<img src="https://github-readme-streak-stats.herokuapp.com/?user=Chetan-Biranje&theme=github-dark-blue&hide_border=true&background=0d1117&ring=0E5484&fire=58a6ff&currStreakLabel=0E5484&sideLabels=58a6ff&dates=4a6a80" />

<br/>

<img src="https://github-readme-stats.vercel.app/api?username=Chetan-Biranje&show_icons=true&theme=github_dark&bg_color=0d1117&title_color=0E5484&icon_color=58a6ff&text_color=8b949e&hide_border=true&include_all_commits=true" height="155"/>
<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=Chetan-Biranje&layout=compact&theme=github_dark&bg_color=0d1117&title_color=0E5484&text_color=8b949e&hide_border=true&langs_count=6" height="155"/>

</div>

---

## `$ cat frameworks.conf`

| Security Framework | Purpose |
|---|---|
| OWASP Top 10 · API Top 10 | Web & API vuln reference |
| OWASP ASVS | Application security verification |
| STRIDE | Threat modeling |
| CVSS v3.1 | Vulnerability severity scoring |
| CIS Benchmarks | Server & container hardening |
| Zero-Trust | Network & IAM architecture |

---

## `$ cat certifications.txt`

```
✓ Linux Fundamentals              — TCM Security
✓ Application Security Training  — DevTown
✓ SOC Analyst                    — USLA
✓ Dark Web Operations             — USLA
✓ Cybersecurity Simulation        — Commonwealth Bank
✓ Shields Up: Cybersecurity       — AIG
✓ Cyber Job Simulation            — Deloitte Australia
✓ Microsoft AI Classroom          — Microsoft
✓ Node.js + Express + MongoDB     — Udemy
```

---

<div align="center">

```
╔══════════════════════════════════════════════════════════════════╗
║  [ OPEN TO ]                                                     ║
║  DevSecOps Engineer · Application Security Engineer              ║
║  Pipeline Security · Shift-Left Security Implementation          ║
║  Bug Bounty Collaborations · Security Research                   ║
╚══════════════════════════════════════════════════════════════════╝
```

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:062e52,100:0E5484&height=100&section=footer" width="100%"/>

</div>
