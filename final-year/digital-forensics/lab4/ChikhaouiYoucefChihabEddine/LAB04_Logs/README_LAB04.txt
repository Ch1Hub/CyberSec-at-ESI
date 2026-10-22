LAB 04 - Linux System Triage and Log Investigation
Synthetic training data only

CASE: ORION workstation triage
Target host in the scenario: ws-17 (192.0.2.10)
Investigation window: 2026-10-12 08:00 through 10:00 UTC+01:00

Files:
- asset_inventory.txt: context and known scheduled/authorized activity
- ssh_auth.log: synthetic SSH authentication and sudo records
- system.log: synthetic service and system events
- firewall.log: synthetic firewall decisions
- nginx_access.log: synthetic web access records
- process_snapshot.txt: a prepared snapshot attributed to the fictional target host

IMPORTANT
All records and identities in this package are fictional. The IP addresses use documentation ranges (RFC 5737) and the domains use .example. These files do not come from a real SIFT machine and do not prove a real compromise.

Student workflow
1. Extract this folder to ~/LAB04/logs or another working folder.
2. Run the commands in the lab sheet against these files.
3. Use the asset inventory to separate expected activity from uncertain activity.
4. Save only relevant screenshots and write cautious conclusions.
