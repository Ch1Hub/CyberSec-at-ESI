# Audit — completeness review

This document records how each topic was reviewed before publication: what exists, what is missing, and how the material is presented. It is deliberately explicit about gaps so the archive is not mistaken for a fully graded portfolio.

## Summary

| Year | Topics | Practicals | ✅ Complete | 🟦 Code only | 🟨 Partial | 📄 Sheet only |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 4th year, S1 | 6 | 15 | 4 | 8 | 2 | 1 |
| 4th year, S2 | 8 | 42 | 21 | 15 | 2 | 4 |
| Final year | 7 | 22 | 19 | 0 | 0 | 3 |
| **Total** | **21** | **79** | **44** | **23** | **4** | **8** |

> Statuses count practicals, not files. A practical marked *complete* has a solution and a report or equivalent evidence. *Code only* means the implementation survived but no formal report did. *Partial* means an important deliverable is missing. *Sheet only* means only the assignment was archived.

## Topic-by-topic findings

### 4th year — Semester 1

| Topic | Finding | Rating |
| --- | --- | --- |
| Artificial Intelligence Fundamentals | TP6 (clustering) and TP8 (ANN) are complete with reports. TP4 has the notebooks but not the write-up. TP5 keeps only the dataset. | ★★★★☆ |
| Databases | Docker Compose setup only; no SQL report. Kept as a stub. | ★★☆☆☆ |
| Algorithmic Complexity | Three Python exercises for TD1; no write-up. | ★★☆☆☆ |
| Cryptography | TP4 and TP42 are complete file-encryption projects. The remaining TP folders are partly empty; nine zero-byte placeholders were dropped. | ★★★☆☆ |
| Network Security | The strongest topic of the semester: two working IDS prototypes, one XGBoost-based; Nmap/Nikto evidence; ACL project. Most lab reports are absent. | ★★★★☆ |
| Web Development | Complete course exercises in HTML/CSS/JS; not security material. | ★★★☆☆ |

### 4th year — Semester 2

| Topic | Finding | Rating |
| --- | --- | --- |
| Cloud Security | Lab 3 is complete (guide, execution report, full report). Lab 5 reuses the Lab 3 reports by mistake. Lab 6 is sheet-only; lab 4 was never archived. | ★★★☆☆ |
| Cybersecurity with Zeek | Labs 2, 5 and 6 contain real logs and scripts. Lab 3 is sheet-only; the week-7 and TD6 scripts are code-only. | ★★★☆☆ |
| Data Analysis | No files were archived. Kept as a named stub in the year index. | ☆☆☆☆☆ |
| DevOps | Lab 5 is fully documented; labs 1–4 and 7 contain code and manifests. Lab 6 is sheet-only. | ★★★☆☆ |
| IoT Security | Six Arduino/ESP8266 sketches; labs 4 and 5 include sheets and reports. Lab 6 is a third-party tutorial stack. | ★★★★☆ |
| OS Security | Kernel module, SUID, LinPEAS/LinEnum, mini-HIDS and n8n are all present. The empty Lab 6 placeholder is retained and explained. | ★★★★☆ |
| Web Security | The flagship: 7 SSRF scenarios, 24 SQLi/NoSQLi labs, 13 BAC labs, Keycloak IAM and a five-part DevSecOps track. All complete. | ★★★★★ |
| Wireless Security | Three complete labs with captures, scripts and reports. | ★★★★★ |

### Final year

| Topic | Finding | Rating |
| --- | --- | --- |
| AI for Cybersecurity | Three complete labs with notebooks, reports and figures. | ★★★★★ |
| Blockchain & ZKP | Three complete labs: PoW chain, Solidity security, gnark circuits. Course decks included. | ★★★★★ |
| Digital Forensics | Four complete labs with evidence bundles, disk images and reports. | ★★★★★ |
| Ethical Hacking | Labs 1, 3 and 4 are strong (including 150+ enumeration screenshots). Labs 2 and 5 are sheets only. | ★★★★☆ |
| Identity & Access Management | Lab 1 (Active Directory) is complete. Lab 4 is sheet-only. | ★★★☆☆ |
| IoT Security | Firmware extraction and the full MQTT/TLS/mTLS sequence, each with a report. | ★★★★★ |
| Malware Analysis | Three complete labs. Live samples were removed for safety; analysis artefacts remain. | ★★★★★ |

## Editorial decisions

1. **No reconstructed work.** Missing reports were not rewritten after the fact; the folder says what is missing.
2. **No duplicate repository clones.** The `lidsProject` clone of an already-public NIDS repository was removed; the two original prototypes in `network-security` remain.
3. **No vendored tool trees.** FLOSS, Cutter, readpe, Nikto, LiME, squashfs extracts and their archives were dropped; the reports and rules that reference them remain.
4. **Course sheets kept.** Assignment PDFs are kept so each solution can be read in context.
5. **Evidence kept when safe.** PCAPs, disk images, firmware dumps, Zeek logs and screenshots are retained when they contain no live malware or secrets.

## Dates

Commit dates come from the modification times of the original files, so the history follows the actual lab timeline (October 2025 → November 2026) rather than the publication date. Files that were edited during sanitisation had their original timestamps restored before committing.
