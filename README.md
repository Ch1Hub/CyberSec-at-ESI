# CyberSec at ESI

A two-year archive of cybersecurity coursework from the engineering cycle at **ESI SBA** (École Supérieure en Informatique, Sidi Bel Abbès, Algeria), covering the **4th year** and the **final year**.

The repository is organised by academic year, semester and topic. Every practical folder contains its own README with the assignment sheet, the deliverables that were archived, and the report where one exists. All work is the result of lab sessions and personal study between **October 2025 and November 2026**.

<p align="left">
  <img alt="topics" src="https://img.shields.io/badge/topics-21-0b7285">
  <img alt="labs" src="https://img.shields.io/badge/practicals-79-1864ab">
  <img alt="reports" src="https://img.shields.io/badge/reports-44%20complete-2b8a3e">
</p>

## Highlights

| Area | What is inside |
| --- | --- |
| **Web Security** | 7 SSRF scenarios, 24 SQL/NoSQL injection labs, 13 broken-access-control labs, IAM with Keycloak/LDAP, and a 5-part DevSecOps track. |
| **AI for Cybersecurity** | Supervised intrusion detection on UNSW-NB15, ML-versus-rules comparison, and unsupervised anomaly detection on CICIDS2017. |
| **Malware Analysis** | A real downloader chain, AgentTesla static analysis with YARA rules and entropy analysis, and a two-part final assignment. |
| **Digital Forensics** | SIFT/Autopsy timeline work, disk-image analysis, the ORION evidence bundle, and Windows event-log analysis. |
| **Blockchain & ZKP** | A proof-of-work chain in Python, Solidity reentrancy/access-control labs, and gnark zero-knowledge circuits in Go. |
| **Network Security** | Nmap/Nikto reconnaissance and two Python IDS prototypes, including an XGBoost flow classifier. |
| **OS Security** | Kernel modules, SUID escalation, host enumeration with LinPEAS/LinEnum, a Bash mini-HIDS and n8n automation. |
| **Wireless Security** | WEP internals, WEP cracking and WPA/WPA2 handshake capture with offline dictionary attacks. |

## Repository layout

```
CyberSec-at-ESI/
├── 4th-year/
│   ├── s1/
│   │   ├── ai-fundamentals/        # regression, classification, clustering, ANN
│   │   ├── databases/              # PostgreSQL / Docker
│   │   ├── complexity/             # algorithmic complexity
│   │   ├── cryptography/           # classical ciphers, AES, RSA, file encryption
│   │   ├── network-security/       # Nmap, ACLs, Zeek/tcpdump, IDS prototypes
│   │   └── web-development/        # HTML, CSS, JavaScript
│   └── s2/
│       ├── cloud-security/         # OpenStack MicroStack, Keystone
│       ├── cybersecurity-zeek/     # Zeek logs and detection scripts
│       ├── data-analysis/          # no publishable material
│       ├── devops/                 # Docker, Compose, Kubernetes, CI/CD
│       ├── iot-security/           # ESP8266, HTTP server, MQTT
│       ├── os-security/            # kernel modules, SUID, LinPEAS, n8n
│       ├── web-security/           # SSRF, SQLi, BAC, IAM, DevSecOps
│       └── wireless-security/      # WEP, WPA/WPA2
└── final-year/
    ├── ai-for-cybersecurity/       # detection engineering with ML
    ├── blockchain-zkp/             # chain, Solidity, zk-SNARKs
    ├── digital-forensics/          # disk, timeline and log forensics
    ├── ethical-hacking/            # recon, enumeration, exploitation
    ├── iam/                        # Active Directory, AAA
    ├── iot-security/               # firmware extraction, MQTT/TLS/mTLS
    └── malware-analysis/           # downloader, AgentTesla, final project
```

## Flagship repositories

Five self-contained repositories are split from this archive, with the same dated history:

| Repository | Topic | Contents |
| --- | --- | --- |
| [`web-security-labs`](https://github.com/Ch1Hub/web-security-labs) | 4th year, S2 | SSRF, SQLi/NoSQLi, broken access control, IAM, DevSecOps |
| [`ai-for-cybersecurity-labs`](https://github.com/Ch1Hub/ai-for-cybersecurity-labs) | Final year | UNSW-NB15, ML vs rules, CICIDS2017 anomaly detection |
| [`malware-analysis-labs`](https://github.com/Ch1Hub/malware-analysis-labs) | Final year | Downloader, AgentTesla, YARA, static analysis |
| [`digital-forensics-labs`](https://github.com/Ch1Hub/digital-forensics-labs) | Final year | SIFT, disk images, ORION evidence, event logs |
| [`blockchain-zkp-labs`](https://github.com/Ch1Hub/blockchain-zkp-labs) | Final year | PoW chain, Solidity security, gnark ZKP |

## Reading a lab

Each practical follows the same layout:

```
lab/
├── README.md          # objective, sheet, report links, contents, how to run
├── <assignment>.pdf   # lab sheet
├── <report>.pdf/.md   # report when one was produced
└── ...                # code, notebooks, evidence
```

The **status** shown in topic tables is:

- ✅ **Lab work archived** — sheet, solution and report (or equivalent evidence).
- 🟦 **Code archived** — implementation or scripts, usually without a formal report.
- 🟨 **Partial archive** — some deliverables were lost or never produced.
- 📄 **Assignment sheet only** — the sheet is kept for completeness; no solution was archived.

## Coursework notes

- Some labs were graded, others were not; a few folders are deliberately marked *sheet only* rather than filled with reconstructed work after the fact.
- Assignment sheets and lecture slides remain the property of ESI SBA and the respective teachers. My own code, reports and analysis are published as a portfolio.
- The archive is **sanitised**: credentials, private keys and the live malware samples have been removed. See [`SECURITY.md`](SECURITY.md) and [`OMITTED.md`](OMITTED.md).
- [`AUDIT.md`](AUDIT.md) records the completeness review of every topic.

## Responsible use

Every offensive technique here was performed against isolated, deliberately vulnerable targets in a course lab. Nothing in this repository is a target list or an invitation to test third-party systems. See [`SECURITY.md`](SECURITY.md) before running anything.

---

*Maintained by [Ch1Hub](https://github.com/Ch1Hub) — Youcef Chihab Eddine Chikhaoui.*
