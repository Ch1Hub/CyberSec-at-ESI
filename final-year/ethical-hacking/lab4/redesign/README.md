# Lab 04 — Redesigned report

Author: **Chikhaoui Youcef Chihab Eddine**

## Files

- `report.html` — full source of the redesigned report (A4, 11 pages).
- `assets/` — the seven evidence screenshots. `fig04-gvm-check.png` has the Kali
  prompt hostname changed to `Ch1Hub`; `fig04-prompt-detail.png` is the zoomed
  prompt used as an inset.

## Build

```bash
google-chrome --headless=new --disable-gpu --no-sandbox \
  --no-pdf-header-footer \
  --print-to-pdf=../Lab_04_Vulnerability_Analysis_Report_Redesigned.pdf \
  --virtual-time-budget=10000 \
  "file://$PWD/report.html"
```

The checked-in PDF was post-processed with PyMuPDF to set the author metadata
and section bookmarks.
