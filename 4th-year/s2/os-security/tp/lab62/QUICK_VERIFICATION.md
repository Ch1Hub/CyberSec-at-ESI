# Quick Verification Guide - TP6 Part 1 (n8n) ✅

## Status: FULLY OPERATIONAL

The n8n File Integrity Monitoring workflow is **installed, running, and verified working**.

---

## 🚀 How to Verify It's Working

### Method 1: Check Container is Running (30 seconds)

```bash
docker ps | grep n8n-tp6
```

**Expected Output:**
```
989fccc0a735   n8nio/n8n   "tini -- /docker-ent…"   Up 46 minutes   0.0.0.0:5678->5678/tcp   n8n-tp6
```

✅ **Status: RUNNING**

---

### Method 2: Access n8n Web UI (Interactive)

```bash
# Open in your browser:
http://localhost:5678
```

**You should see:**
- n8n dashboard
- Left sidebar with workflows
- Workflow: **"TP6 - File Integrity Monitoring Alert"** listed

✅ **Status: ACCESSIBLE**

---

### Method 3: Test File Modification Detection (3 minutes)

**Step 1:** Modify the monitored file
```bash
echo "TEST: $(date)" >> /home/chihab/Documents/cys2CS/s2/opSysSec/tp/lab62/n8n-lab/fim_target.txt
```

**Step 2:** Wait for next scheduled execution (~65 seconds)
```bash
# The workflow runs automatically every minute
sleep 65
```

**Step 3:** Check if alert was logged
```bash
cat /home/chihab/Documents/cys2CS/s2/opSysSec/tp/lab62/n8n-lab/fim_alert.log | tail -1
```

**Expected Output:**
```
[2026-05-04T14:00:55+00:00] ALERT: /files/fim_target.txt changed old=6d3d40f12065817238a9e5c26e1a937763e40ebe8002438c7cee398bcd707b7e new=cea7eab5b5c35b77189c563cd0c4a9aa7e74bdf55b587265b9f51f9ce204ed77
```

✅ **Status: WORKING** - File changes detected and logged

---

### Method 4: Verify Workflow Status in Logs (Instant)

```bash
docker logs n8n-tp6 2>&1 | tail -20
```

**Look for:**
```
Activated workflow "TP6 - File Integrity Monitoring Alert" (ID: tp6-fim-001)
```

✅ **Status: ACTIVATED**

---

### Method 5: Check All Files Are Present

```bash
ls -la /home/chihab/Documents/cys2CS/s2/opSysSec/tp/lab62/n8n-lab/
```

**Expected Files:**
```
-rw-r--r--  file-integrity-monitoring-workflow.json    (Workflow definition)
-rw-r--r--  fim_target.txt                             (Monitored file)
-rw-r--r--  fim_alert.log                              (Alert log)
```

✅ **Status: ALL FILES PRESENT**

---

## 📊 What You'll See

### Current Alert Log (Sample)
```
[2026-05-04T13:12:07+00:00] ALERT: /files/fim_target.txt changed old=0a027f824bb26705d45af73ea0babad4d407ba9d40e949b36a39a67c4b20d740 new=6d3d40f12065817238a9e5c26e1a937763e40ebe8002438c7cee398bcd707b7e
[2026-05-04T14:00:55+00:00] ALERT: /files/fim_target.txt changed old=6d3d40f12065817238a9e5c26e1a937763e40ebe8002438c7cee398bcd707b7e new=cea7eab5b5c35b77189c563cd0c4a9aa7e74bdf55b587265b9f51f9ce204ed77
```

Each line shows:
- **Timestamp:** When the change was detected
- **Old Hash:** SHA256 of previous file state
- **New Hash:** SHA256 of current file state

---

## 🔍 Workflow Architecture

```
┌─────────────────────────┐
│ Schedule Trigger        │  (Every 1 minute)
│ (Cron: everyMinute)     │
└──────────┬──────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│ Execute Command - Hash File              │
│ Command: sha256sum /files/fim_target.txt │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│ Function - Compare Hash                  │
│ Compares current hash with stored hash   │
│ Sets: alert = true/false                 │
└──────────┬───────────────────────────────┘
           │
           ▼ (IF alert == true)
┌──────────────────────────────────────────┐
│ Execute Command - Write Alert            │
│ Appends to: /files/fim_alert.log        │
└──────────────────────────────────────────┘
```

---

## 🛠️ Maintenance Commands

### View n8n Logs
```bash
docker logs n8n-tp6 -f --tail 50
```

### Restart n8n
```bash
docker restart n8n-tp6
```

### View Container Status
```bash
docker inspect n8n-tp6 --format='{{.State.Status}}'
```

### Check Port Usage
```bash
netstat -tlnp | grep 5678
# or
lsof -i :5678
```

### Reset Alert Log (Caution!)
```bash
rm /home/chihab/Documents/cys2CS/s2/opSysSec/tp/lab62/n8n-lab/fim_alert.log
touch /home/chihab/Documents/cys2CS/s2/opSysSec/tp/lab62/n8n-lab/fim_alert.log
```

---

## ✅ Verification Checklist

- [x] Docker is installed and running
- [x] n8n container is deployed and running
- [x] Port 5678 is accessible
- [x] Workflow "TP6 - File Integrity Monitoring Alert" is created
- [x] Workflow is activated in n8n
- [x] Cron trigger configured (every 1 minute)
- [x] File monitoring nodes are configured
- [x] Alert logging is functional
- [x] File changes are detected and logged
- [x] Documentation is complete

**ALL CHECKS PASSED ✅**

---

## 📚 Full Documentation

For detailed setup information, see: **`IMPLEMENTATION_COMPLETE.md`**

This includes:
- Complete architecture
- Node-by-node workflow details
- Troubleshooting guide
- Adaptation for `/etc/passwd` target
