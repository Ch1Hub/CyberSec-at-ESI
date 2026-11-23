# Omitted material

Everything below existed in the original course folders but is **not** published. Each entry says why, so the archive can be audited against the source.

## 1. Live malware and dangerous binaries

| Omitted | Reason |
| --- | --- |
| `agentTesla.exe`, `agentTesla_stage2.dll` | Live malware. Hashes, YARA rules, disassembly and reports are kept instead. |
| `windows11-setup_11_45288.exe` and extracted Windows 11 payloads/resources | Live stage-2 payload and dropper resources. |
| Mirai ELF sample (`3cdafb9a…d188.elf`, 150 KB) | Live Linux malware. The YARA rule, `readelf` output, DIE report and Mirai table decoder script are kept. |
| `payload_binary`, `yb.exe`, `rp.exe`, `lfd.cmd`, `*.scr` | Compiled/obfuscated payloads from the malware labs. The benign `payload.c` and `c2_server.py` simulators are kept. |
| Other `.exe`/`.dll`/`.scr` files under `malware-analysis/lab2` | Unpacked or extracted components of the same sample. |

Hashes and analysis artefacts are preserved in `final-year/malware-analysis/`.

## 2. Large virtual machines and raw datasets

| Omitted | Size | Reason |
| --- | ---: | --- |
| `Windows Server 2022 dc01.vmdk` | 11.3 GB | Virtual disk for the ethical-hacking AD lab. Beyond GitHub limits. The `.vmx`/`.vmsd` descriptors and all screenshots/reports are kept. |
| Raw CICIDS2017 CSVs (`cic_ids2017/`) | 1.2 GB | Eight raw capture-derived CSVs. The curated feature set (`cicids2017_curated.csv`), the notebook and the report are kept. |
| `archive (1).zip` | 240 MB | Duplicate archive of the CICIDS data. |
| FLOSS 3.1.1 bundle and ZIP | 40 MB+ | Third-party tool; downloadable upstream. |
| Cutter 2.5.0 AppImage | 131 MB | Third-party reverse-engineering tool. |
| LIiME, readpe, Nikto, Cutter source trees, `squashfs-root/` | 100 MB+ | Vendored tools and extracted filesystems. |
| `msfinstall` | 6 KB | Installer script for Metasploit; not original work. |

## 3. Secrets and private keys

| Omitted / redacted | Reason |
| --- | --- |
| `ethicalHack/restore-vms.sh` | Contained a plaintext local `sudo` password. Removed entirely. |
| `ethicalHack/lab3/context.txt`, `vms-connect.txt` | Operator notes with host and credential details. |
| `ethicalHack/lab3/lab_screens/2026-10-25-*.txt` | Terminal transcript containing the same password. The screenshots from the session are kept. |
| `iam/lab1/session-ses_*.md` | Full assistant session transcript, not coursework. |
| `.env` files and `.env/` virtualenvs | Environment secrets and vendored Python environments. |
| IoT lab `*.key` files (CA, broker, ESP01, rogue CA) | Private keys for the mTLS lab. The certificates and the procedure to regenerate them remain. |
| Keycloak client secrets, LDAP bind password, Flask session key | Replaced with `REDACTED_*` placeholders. |
| Ganache private keys and mnemonic | Redacted in `ganache.log` and the Lab 2 report. |
| Wi-Fi SSID/password, SSH demo password, OpenStack/Mongo lab passwords | Redacted or replaced with placeholders. |

## 4. Dependency, cache and build junk

`node_modules/`, `__pycache__/`, `.ipynb_checkpoints/`, `.pytest_cache/`, `.mypy_cache/`, Python virtualenvs (`venv/`, `.venv/`, `.env/`), compiled `.pyc`/`.pyo`, `.DS_Store`, `Thumbs.db`.

## 5. Unreadable or duplicate material

| Omitted | Reason |
| --- | --- |
| `databases/tp1/data/dbconfig/XE/` | Root-owned Oracle configuration files, unreadable to the user; database data files are not part of the deliverable. |
| `network-security/tp3/report.txt` | Root-owned file that could not be read; the ACL project sources are kept. |
| `network-security/lidsProject/` | Clone of the already-public [`intrusion-detection-system-using-ML`](https://github.com/Chihab0/intrusion-detection-system-using-ML) repository. The two original prototypes (`lids`, `l-ids`) are kept. |
| Empty placeholder folders | `web-development/flutter/`, `cybersecurity-zeek/dw8/`, `data-analysis/td1/`, `network-security/lab7/`, `network-security/td2/`, and many zero-byte cryptography placeholders. Keeping empty directories added no information. |

## 6. What was intentionally kept

- Assignment sheets and lecture slides, for context.
- Benign lab binaries written for the course (`payload.c`, `c2_server.py`, the vulnerable SUID helper, the kernel module, the mini-HIDS).
- Harmless build outputs from the OS-security labs (`a.out`, `exe3.so`, `fake.so`).
- Synthetic evidence: `suspect_disk.img` (64 MB), `ORION_Disk_Image.dd` (34 MB), firmware dumps, packet captures, Zeek logs and 150+ enumeration screenshots.
- Reports in every available format (PDF, DOCX, Markdown, HTML) rather than converting or discarding them.

## 7. Copyright note

Lab sheets, lecture slides and third-party tutorials remain the property of ESI SBA and their authors. They are included only as the context needed to read the solutions. The code, reports and analysis produced by the author are published as a study portfolio.
