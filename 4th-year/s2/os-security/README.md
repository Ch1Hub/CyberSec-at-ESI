# Operating System Security

Linux security from the inside: memory corruption, kernel modules, SUID escalation, host enumeration, a mini-HIDS, backups and automation.

**Level:** 4th year — semester 2  
**Tools:** C, Bash, Linux, LinPEAS, LinEnum, n8n

> Labs 1–5, 4.1 and the n8n lab are substantial; the empty lab 6 placeholder is noted.

## Labs

| Lab | What it covers | Status |
| --- | --- | --- |
| [Lab 1 — Memory corruption and shared objects](tp/lab1/) | Buffer-overflow demonstration, a minimal syscall program and a shared-library hijack exercise. | ✅ Lab work archived |
| [Lab 2 — Linux kernel module](tp/lab2/) | Loadable kernel module exposing a /proc entry, plus an SSH client used to trigger it. | 🟦 Code archived |
| [Lab 3 — SUID privilege escalation](tp/lab3/) | SUID helper demonstrating how an unchecked system() call yields a root shell. | 🟦 Code archived |
| [Lab 4 — Linux privilege escalation enumeration](tp/lab4/) | LinPEAS, LinEnum and linux-exploit-suggester runs against a vulnerable target, with the lab sheet. | ✅ Lab work archived |
| [Lab 4.1 — Mini host IDS](tp/lab4.1/) | Bash mini-HIDS with event-provocation scripts for monitoring file and process activity. | 🟦 Code archived |
| [Lab 5 — Backup strategy](tp/lab5/) | Full and incremental backup exercise with restored data sets. | 🟦 Code archived |
| [Lab 6 — Automation assignment](tp/lab6/) | Empty placeholder; the documented work is in the n8n lab below. | 📄 Assignment sheet only |
| [Lab 6 — n8n security automation](tp/lab62/) | Complete n8n setup and verification guide for the security-automation assignment. | ✅ Lab work archived |

## Additional material

| Path | Type |
| --- | --- |
| [lessons/](lessons/) | Directory (7 files) |
| [tp/](tp/) | Directory (38 files) |

---
*Part of the [CyberSec at ESI](../../../README.md) archive.*
