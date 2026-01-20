# Network Security Labs - Complete Commands & Concepts Guide

## Table of Contents
1. [Lab 1: Introduction (Kali + Metasploitable2)](#lab-1-introduction)
2. [Lab 2: Authentication in Practice](#lab-2-authentication)
3. [Lab 3: Access Control & ACLs](#lab-3-access-control--acls)
4. [Lab 4: Network Traffic Analysis (Wireshark/tcpdump)](#lab-4-network-traffic-analysis)
5. [Lab 5: Vulnerability Detection & Audit](#lab-5-vulnerability-detection--audit)
6. [Lab 6: OpenSSH Security](#lab-6-openssh-security)
7. [Lab 7: PKI & Digital Certificates](#lab-7-pki--digital-certificates)
8. [Lab 8: Advanced Firewall (UFW & nftables)](#lab-8-advanced-firewall)
9. [Lab 9: IDS/IPS with Suricata](#lab-9-idsips-with-suricata)

---

## Lab 1: Introduction

### Concepts
- **Network Discovery**: Finding active hosts on a network
- **Port Scanning**: Identifying open services on target machines
- **Traffic Capture**: Recording network packets for analysis

### Commands

#### Startup & Network Check
```bash
# Check IP address
ip a
ifconfig

# System info
uname -a
whoami
```

#### Discovery & Scanning
```bash
# Connectivity test
ping -c 4 <IP_TARGET>

# ARP discovery
sudo netdiscover -i <interface>
arp-scan --localnet

# Nmap scanning
nmap -sC -sV -p 1-1000 <IP> -oN nmap_quick.txt    # Quick scan with scripts
nmap -p 80 --script=http-enum <IP>                 # HTTP enumeration
nmap -p 80 -sV --script=http-title <IP>            # HTTP title detection
nmap -T4 -sC -sV <IP>                              # Faster scan
```

#### Service Interaction
```bash
# FTP connection
ftp <IP>
# Use: anonymous login, ls, quit

# HTTP interaction
curl -I http://<IP>           # Get HTTP headers
curl http://<IP>/ > index.html
```

#### Traffic Capture
```bash
# Capture HTTP traffic
sudo tcpdump -i <interface> port 80 -w tp1_http.pcap

# Open in Wireshark, filter: http
```

---

## Lab 2: Authentication

### Concepts
- **Asymmetric Encryption (GPG)**: Public/private key pairs for secure communication
- **Password Hashing**: Converting passwords to fixed-length digests
- **Brute-Force Attacks**: Automated password guessing
- **Firewall Protection**: Blocking malicious IPs

### Commands

#### GPG Encryption
```bash
# Generate keypair
gpg --full-generate-key

# Export public key
gpg --armor --export "Name" > pub.asc

# Transfer key
scp pub.asc user@<IP>:/path/

# Import public key
gpg --import pub.asc
gpg --list-keys
gpg --fingerprint "Name"

# Encrypt file
gpg --encrypt --recipient "Name" --armor -o encrypted.asc message.txt

# Decrypt file
gpg --decrypt encrypted.asc > decrypted.txt
```

#### SSH Service
```bash
sudo service ssh start
```

#### Password Cracking (John the Ripper)
```bash
# Create hash file and crack with wordlist
john --wordlist=/path/to/wordlist hashes.txt
```

#### Brute-Force with Hydra
```bash
# Create password list
echo -e "password1\npassword2\nmsfadmin" > passlist.txt

# Attack FTP
hydra -l msfadmin -P passlist.txt ftp://<IP> -t 4
```

#### Block Attacker with iptables
```bash
# Block IP
sudo iptables -A INPUT -s <ATTACKER_IP> -j DROP

# Verify
sudo iptables -L
```

---

## Lab 3: Access Control & ACLs

### Concepts
- **Unix Permissions**: Read(4), Write(2), Execute(1) for Owner/Group/Others
- **ACLs**: Fine-grained access control beyond traditional permissions
- **SUID/SGID**: Special permission bits for privilege escalation
- **Principle of Least Privilege**: Minimum necessary permissions

### Commands

#### User & Group Management
```bash
# Create users
sudo useradd alice
sudo useradd bob

# Create groups
sudo groupadd dev
sudo groupadd design

# Add user to group
sudo usermod -aG dev bob

# View users/groups
cat /etc/passwd
cat /etc/group
```

#### Basic Permissions
```bash
# View permissions
ls -l file.txt
ls -ld directory/

# Change permissions (symbolic)
chmod u+rwx,g+r,o-rwx file.txt

# Change permissions (numeric)
chmod 740 file.txt    # rwx r-- ---

# Change owner
sudo chown alice file.txt

# Change group
sudo chgrp dev file.txt

# Change both
sudo chown alice:dev file.txt
```

#### ACL Commands
```bash
# Install ACL
sudo apt install acl -y

# Set ACL for user
setfacl -m u:bob:rw file.txt

# Set ACL for group
setfacl -m g:dev:rx directory/

# Set default ACL (inheritance)
setfacl -d -m u:bob:rw directory/

# View ACLs
getfacl file.txt

# Remove ACL
setfacl -x u:bob file.txt

# Remove all ACLs
setfacl -b file.txt
```

#### Directory Creation
```bash
mkdir -p /home/user/tp_acl/
chmod 750 /home/user/tp_acl/
```

---

## Lab 4: Network Traffic Analysis

### Concepts
- **Packet Capture**: Recording network traffic for analysis
- **BPF (Berkeley Packet Filter)**: Filter language for capture tools
- **TCP 3-Way Handshake**: SYN → SYN-ACK → ACK
- **Clear-text Protocols**: FTP, Telnet expose credentials

### tcpdump Commands

```bash
# Basic capture
sudo tcpdump -i eth0

# Save to file
sudo tcpdump -i eth0 -w capture.pcap

# Read capture file
tcpdump -r capture.pcap

# Detailed output (no DNS resolution)
sudo tcpdump -nn -vvv -i eth0

# Limit packet count
sudo tcpdump -i eth0 -c 50

# Capture filters
sudo tcpdump -i eth0 host 192.168.56.101
sudo tcpdump -i eth0 src 192.168.56.101
sudo tcpdump -i eth0 dst 192.168.56.101
sudo tcpdump -i eth0 tcp port 80
sudo tcpdump -i eth0 udp port 53
sudo tcpdump -i eth0 'tcp port 21 or tcp port 23'
sudo tcpdump -i eth0 not arp

# Rotating captures (10MB files, max 5)
sudo tcpdump -i eth0 -C 10 -W 5 -w capture.pcap

# Compressed capture
sudo tcpdump -i eth0 -w - | gzip > capture.pcap.gz
```

### Wireshark Display Filters

| Filter | Description |
|--------|-------------|
| `ip.addr == 192.168.56.101` | All traffic involving IP |
| `tcp.port == 80` | HTTP traffic |
| `dns` | DNS packets |
| `ftp or telnet` | Unencrypted protocols |
| `tcp.analysis.retransmission` | TCP retransmissions |
| `http.request.method == "GET"` | HTTP GET requests |

### Wireshark Tips
- **Follow Stream**: Right-click packet → Follow → TCP Stream
- **Find Packet**: Ctrl+F (search string/hex/display filter)
- **Export Filtered**: File → Export Specified Packets → Displayed

---

## Lab 5: Vulnerability Detection & Audit

### Concepts
- **Vulnerability Scanning**: Automated detection of security weaknesses
- **Web Application Scanning**: Finding misconfigurations in web servers
- **System Auditing**: Checking local security configurations
- **SUID Binaries**: Potential privilege escalation vectors

### Nmap Advanced Scanning
```bash
# Network discovery
nmap -sn 192.168.56.0/24

# Service version detection
nmap -sV -sC -T4 <IP>

# Vulnerability scripts
nmap --script vuln <IP>

# OS detection
nmap -O <IP>

# Aggressive scan
nmap -A -Pn -p22,80,139,445 <IP>
```

### Nikto (Web Scanner)
```bash
# Simple scan
nikto -h http://<IP>

# Specific port
nikto -h <IP>:8080

# HTTPS
nikto -h https://<IP>

# Save report
nikto -h <IP> -o report.html -Format html
nikto -h <IP> -o report.txt -Format txt

# Verbose output
nikto -h <IP> -Display V

# Custom User-Agent
nikto -h <IP> -useragent "MyAgent/1.0"
```

### Lynis (System Audit)
```bash
# Full audit
sudo lynis audit system

# Quick audit
sudo lynis audit system --quick

# Specific test group
sudo lynis audit system --tests-from-group authentication

# Non-interactive
sudo lynis audit system --cronjob

# Logs: /var/log/lynis.log, /var/log/lynis-report.dat
```

### Network Monitoring
```bash
# Show listening ports
sudo ss -tulnp
sudo netstat -tulnp

# Network files
sudo lsof -i -P -n

# Top processes by memory
ps aux --sort=-%mem | head -n 15
```

### Firewall (UFW)
```bash
sudo ufw status
sudo ufw enable
sudo ufw default deny incoming
sudo ufw allow ssh
```

### SUID Analysis
```bash
# Find all SUID binaries
sudo find / -perm -4000 -type f 2>/dev/null

# Examine binary
file /path/to/binary
ldd /path/to/binary 2>/dev/null
strings /path/to/binary | head -n 40
```

---

## Lab 6: OpenSSH Security

### Concepts
- **SSH Key Authentication**: More secure than passwords
- **SSH Hardening**: Reducing attack surface
- **Fail2ban**: Automatic IP blocking after failed attempts

### Installation & Setup
```bash
# Check if installed
dpkg -l | grep openssh

# Install
sudo apt install -y openssh-server

# Enable and start
sudo systemctl enable ssh
sudo systemctl start ssh
systemctl status ssh
```

### Connection
```bash
ssh username@<server_ip>
ssh -p 2222 username@<server_ip>    # Custom port
```

### Configuration File: `/etc/ssh/sshd_config`

```bash
# Backup before editing
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak.$(date +%F_%T)
sudo nano /etc/ssh/sshd_config
```

#### Key Directives
| Directive | Example | Description |
|-----------|---------|-------------|
| `Port` | 2222 | Custom port (avoid 22) |
| `PermitRootLogin` | no | Disable root SSH |
| `PasswordAuthentication` | no | Disable password login |
| `PubkeyAuthentication` | yes | Enable key auth |
| `PermitEmptyPasswords` | no | Block empty passwords |
| `MaxAuthTries` | 3 | Limit attempts |
| `LoginGraceTime` | 30 | Timeout for login |
| `AllowUsers` | user1 user2 | Whitelist users |
| `DenyUsers` | guest test | Blacklist users |
| `LogLevel` | VERBOSE | Enhanced logging |

```bash
# Restart after changes
sudo systemctl restart ssh
```

### SSH Key Authentication
```bash
# Generate key pair (on client)
ssh-keygen -t rsa -b 4096 -C "user@server"

# Copy to server
ssh-copy-id -p 666 user@<server_ip>

# Connect without password
ssh -p 666 user@<server_ip>
```

### Additional Hardening
```bash
# In sshd_config
PermitUserEnvironment no
X11Forwarding no
```

### Firewall & Fail2ban
```bash
# UFW
sudo apt install -y ufw
sudo ufw allow 2222/tcp
sudo ufw enable

# Fail2ban
sudo apt install -y fail2ban
sudo systemctl enable --now fail2ban
```

#### Fail2ban Config (`/etc/fail2ban/jail.conf`)
```ini
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 600
```

### Log Monitoring
```bash
sudo tail -n 20 /var/log/auth.log
sudo grep "Failed password" /var/log/auth.log
```

---

## Lab 7: PKI & Digital Certificates

### Concepts
- **Certificate Authority (CA)**: Trusted entity that issues certificates
- **X.509 Certificates**: Standard format for public key certificates
- **CSR (Certificate Signing Request)**: Request for certificate issuance
- **TLS/HTTPS**: Encrypted web communication

### PKI Directory Structure
```bash
mkdir -p ~/PKI/{certs,crl,newcerts,private}
chmod 700 ~/PKI/private
touch ~/PKI/index.txt
echo 1000 > ~/PKI/serial
```

### OpenSSL Configuration
Edit `/etc/ssl/openssl.cnf` under `[ CA_default ]`:
```
dir = /root/PKI
certificate = $dir/certs/ca.cert.pem
private_key = $dir/private/ca.key.pem
```

### Create Certificate Authority
```bash
# Generate CA private key
openssl genrsa -aes256 -out ~/PKI/private/ca.key.pem 4096
chmod 400 ~/PKI/private/ca.key.pem

# Create CA certificate
openssl req -x509 -new -key ~/PKI/private/ca.key.pem \
  -sha256 -days 3650 -out ~/PKI/certs/ca.cert.pem
```

### Create Server Certificate
```bash
# Generate server private key
openssl genrsa -out server.key.pem 2048
sudo chown root:www-data server.key.pem
sudo chmod 640 server.key.pem

# Generate CSR
openssl req -new -key server.key.pem -out server.csr.pem

# Sign with CA
openssl ca -in server.csr.pem -out server.cert.pem -days 825 -notext

# Verify certificate
openssl verify -CAfile ~/PKI/certs/ca.cert.pem server.cert.pem

# View certificate details
openssl x509 -in server.cert.pem -noout -text
```

### Apache HTTPS Setup
```bash
# Install Apache
sudo apt install apache2

# Enable SSL
sudo a2enmod ssl
sudo systemctl restart apache2
```

#### Configure `/etc/apache2/sites-available/default-ssl.conf`
```apache
SSLEngine on
SSLCertificateFile /path/to/server.cert.pem
SSLCertificateKeyFile /path/to/server.key.pem
SSLCACertificateFile /path/to/ca.cert.pem
```

```bash
# Enable site
sudo a2ensite default-ssl.conf
sudo systemctl reload apache2

# Test
curl -v https://localhost
curl -vk https://localhost    # Skip certificate verification
```

### Certificate Revocation
```bash
# Revoke certificate
openssl ca -revoke server.cert.pem

# Generate CRL
openssl ca -gencrl -out ~/PKI/crl/ca.crl.pem
```

---

## Lab 8: Advanced Firewall

### Concepts
- **UFW**: User-friendly iptables frontend
- **nftables**: Modern Linux firewall framework (replaces iptables)
- **Stateful Filtering**: Tracking connection states
- **Rate Limiting**: Preventing brute-force attacks

### UFW Commands
```bash
# Enable/Disable
sudo ufw enable
sudo ufw disable

# Status
sudo ufw status numbered

# Allow/Deny ports
sudo ufw allow 22/tcp
sudo ufw deny 80/tcp
sudo ufw allow 8080/tcp

# Allow from specific IP
sudo ufw allow from 192.168.1.100

# Block ICMP
sudo ufw deny proto icmp from any

# Delete rule
sudo ufw delete <rule_number>

# Reset
sudo ufw reset
```

### nftables Commands

#### Setup
```bash
sudo apt install nftables -y
sudo systemctl enable nftables
sudo systemctl start nftables
```

#### Basic Operations
```bash
# List all rules
sudo nft list ruleset

# Backup rules
sudo nft list ruleset > backup.nft

# Flush all rules
sudo nft flush ruleset
```

#### Create Firewall Structure
```bash
# Create table
sudo nft add table inet filter

# Create input chain with DROP policy
sudo nft add chain inet filter input '{
  type filter hook input priority 0;
  policy drop;
}'
```

#### Common Rules
```bash
# Allow loopback
sudo nft add rule inet filter input iif lo accept

# Allow established connections (stateful)
sudo nft add rule inet filter input ct state established,related accept

# Allow SSH
sudo nft add rule inet filter input tcp dport 22 accept

# Allow HTTP/HTTPS
sudo nft add rule inet filter input tcp dport 80 accept
sudo nft add rule inet filter input tcp dport 443 accept

# Allow port range
sudo nft add rule inet filter input tcp dport 5000-5050 accept

# Block specific IP
sudo nft add rule inet filter input ip saddr 192.168.1.100 drop
```

#### Rate Limiting (Anti Brute-Force)
```bash
sudo nft add rule inet filter input tcp dport 22 ct state new \
  limit rate 10/minute accept
```

#### Logging
```bash
# Log dropped packets
sudo nft add rule inet filter input limit rate 5/second \
  log prefix "FIREWALL_DROP: "

# View logs
sudo journalctl -f
```

---

## Lab 9: IDS/IPS with Suricata

### Concepts
- **IDS (Intrusion Detection System)**: Monitors and alerts on threats
- **IPS (Intrusion Prevention System)**: Blocks detected threats
- **Signature-based Detection**: Pattern matching against known threats
- **Custom Rules**: User-defined detection patterns

### Installation
```bash
sudo apt update
sudo apt install suricata -y

# Identify network interface
ip a

# Update rule sets
sudo suricata-update
sudo systemctl restart suricata
```

### Running Suricata (IDS Mode)
```bash
# Stop service and run manually
sudo systemctl stop suricata
sudo suricata -c /etc/suricata/suricata.yaml -i eth0
```

### Log Files
- `/var/log/suricata/eve.json` - JSON formatted events
- `/var/log/suricata/fast.log` - Quick alert log
- `/var/log/suricata/stats.log` - Statistics

```bash
# Monitor alerts
sudo tail -f /var/log/suricata/fast.log
```

### Rule Syntax
```
action protocol src_ip src_port -> dst_ip dst_port (options)
```

#### Rule Components
| Part | Description | Example |
|------|-------------|---------|
| action | What to do | `alert`, `drop`, `pass` |
| protocol | Network protocol | `tcp`, `udp`, `icmp`, `http` |
| src/dst | Source/Destination | `any`, `192.168.1.0/24` |
| msg | Alert message | `msg:"Attack Detected";` |
| content | Pattern to match | `content:"malware";` |
| sid | Signature ID (unique) | `sid:1000001;` |
| rev | Revision number | `rev:1;` |

### Custom Rules

#### Create Rule File
```bash
nano /etc/suricata/rules/custom.rules
```

#### Example Rules
```bash
# Detect HTTP access to example.com
alert http any any -> any any (msg:"Example.com Access Detected"; \
  content:"example.com"; sid:1000001; rev:1;)

# Detect ICMP ping
alert icmp any any -> any any (msg:"ICMP Echo Request Detected"; \
  itype:8; sid:2000001; rev:1;)

# Detect SSH brute-force
alert tcp any any -> any 22 (msg:"SSH Brute Force Attempt"; \
  flow:to_server; threshold:type both,track by_src,count 5,seconds 60; \
  sid:2000002; rev:1;)

# Detect suspicious User-Agent
alert http any any -> any any (msg:"Suspicious User-Agent"; \
  http.user_agent; content:"sqlmap"; nocase; sid:2000003; rev:1;)

# Detect executable download
alert http any any -> any any (msg:"EXE Download Detected"; \
  content:".exe"; http.uri; sid:2000004; rev:1;)

# Detect SQL injection
alert http any any -> any any (msg:"SQL Injection Attempt"; \
  content:"' OR '1'='1"; nocase; sid:2000005; rev:1;)

# Detect SYN scan
alert tcp any any -> any any (msg:"Possible Port Scan"; \
  flags:S; threshold:type both,track by_src,count 20,seconds 10; \
  sid:2000006; rev:1;)
```

### Enable Custom Rules
Edit `/etc/suricata/suricata.yaml`:
```yaml
rule-files:
  - /etc/suricata/rules/custom.rules
```

```bash
# Restart Suricata
sudo systemctl restart suricata
```

### Testing
```bash
# Generate traffic to test rules
curl http://example.com
ping <target_ip>
curl http://testmyids.com
```

---

## Quick Reference Tables

### Common Ports
| Port | Service | Protocol |
|------|---------|----------|
| 21 | FTP | TCP |
| 22 | SSH | TCP |
| 23 | Telnet | TCP |
| 25 | SMTP | TCP |
| 53 | DNS | TCP/UDP |
| 80 | HTTP | TCP |
| 443 | HTTPS | TCP |
| 445 | SMB | TCP |
| 3306 | MySQL | TCP |

### Nmap Scan Types
| Flag | Type | Description |
|------|------|-------------|
| `-sS` | SYN Scan | Stealthy, half-open |
| `-sT` | TCP Connect | Full connection |
| `-sU` | UDP Scan | UDP ports |
| `-sV` | Version | Service detection |
| `-sC` | Scripts | Default scripts |
| `-O` | OS | OS detection |
| `-A` | Aggressive | All detection |
| `-T4` | Timing | Faster scan |
| `-Pn` | No Ping | Skip host discovery |

### File Permissions (Numeric)
| Number | Permission |
|--------|------------|
| 7 | rwx (read+write+execute) |
| 6 | rw- (read+write) |
| 5 | r-x (read+execute) |
| 4 | r-- (read only) |
| 0 | --- (no permission) |

---

*Generated from Lab PDFs - Network Security Course*
