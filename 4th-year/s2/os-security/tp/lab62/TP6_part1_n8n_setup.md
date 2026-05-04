# TP6 - Part 1 (n8n) Setup Report

## Scope
Completed **only Part 1 (n8n)** of the lab: automated file integrity monitoring workflow.

## Prerequisites
Verified/used on host:

- Docker engine available and running
- Port `5678` available for n8n UI
- Persistent workspace: `/home/chihab/Documents/cys2CS/s2/opSysSec/tp/lab62/n8n-lab`

## n8n Deployment
Created a persistent n8n service with Docker:

```bash
docker run -d \
  --name n8n-tp6 \
  --restart unless-stopped \
  -p 5678:5678 \
  -e NODES_EXCLUDE='[]' \
  -e N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=false \
  -e N8N_USER_MANAGEMENT_DISABLED=true \
  -e N8N_SECURE_COOKIE=false \
  -e N8N_DIAGNOSTICS_ENABLED=false \
  -v /home/chihab/.n8n:/home/node/.n8n \
  -v /home/chihab/Documents/cys2CS/s2/opSysSec/tp/lab62/n8n-lab:/files \
  -v /etc/passwd:/host/etc/passwd:ro \
  n8nio/n8n
```

Result:

- n8n editor reachable at `http://localhost:5678`
- Container persists across reboot (`restart policy: unless-stopped`)
- n8n data persists in `/home/chihab/.n8n`

## Part 1 Workflow Implemented
Workflow file created:

- `n8n-lab/file-integrity-monitoring-workflow.json`

Workflow name:

- `TP6 - File Integrity Monitoring Alert`

Nodes implemented:

1. **Schedule Trigger** (`everyMinute`)
2. **Execute Command - Hash File** (`sha256sum /files/fim_target.txt | awk '{print $1}'`)
3. **Function - Compare Hash** (stores previous hash in workflow static data and sets `alert=true/false`)
4. **IF - Alert?** (`alert == true`)
5. **Execute Command - Write Alert** (appends alert line to `/files/fim_alert.log`)
6. **No Alert** (no-op false branch)

Workflow was imported and activated in n8n.

## Runtime/Test Artifacts
Created/used files:

- `n8n-lab/fim_target.txt` (monitored test file)
- `n8n-lab/fim_alert.log` (alerts output)

Validated behavior:

1. First scheduled execution establishes baseline hash (`alert=false`)
2. After modifying `fim_target.txt`, next execution detects hash drift
3. Alert is written to `fim_alert.log` with old/new hashes

Example alert line:

```text
[2026-05-04T13:12:07+00:00] ALERT: /files/fim_target.txt changed old=0a027f824bb26705d45af73ea0babad4d407ba9d40e949b36a39a67c4b20d740 new=6d3d40f12065817238a9e5c26e1a937763e40ebe8002438c7cee398bcd707b7e
```

## Notes for strict `/etc/passwd` target
If you want the exact lab target file instead of the safe demo file, update node **Execute Command - Hash File** to:

```bash
sha256sum /host/etc/passwd | awk '{print $1}'
```

(`/etc/passwd` is already mounted read-only as `/host/etc/passwd` inside the container.)
