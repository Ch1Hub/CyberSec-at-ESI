# Lab 1 Full Report (Lab-Only) - OpenStack MicroStack on libvirt

## 1. Scope of this report

This report is dedicated **only** to Lab 1 (MicroStack private cloud setup).  
It documents the complete solving path from initial constraints to final validated deployment.

---

## 2. Lab objective

Deploy and validate a single-node OpenStack private cloud (MicroStack) with:

- Controller/Compute node in one Ubuntu VM
- Working core OpenStack services (Keystone, Nova, Neutron, Glance, Horizon, Cinder)
- At least one instance and one attached block volume

---

## 3. Initial constraints and starting point

### 3.1 Constraints

- Host disk space was limited and previously near saturation.
- Lab expected a 50 GB VM disk.
- Virtualization stack used: **libvirt/virsh** (not VMware).

### 3.2 Decisions taken

To satisfy the 50 GB lab requirement without exhausting host storage:

- Used a **thin-provisioned qcow2** disk of 50 GB virtual size.
- Backed VM disk from Ubuntu cloud image to speed deployment.

Result: VM sees 50 GB, host uses only consumed blocks.

---

## 4. Environment baseline (host and virtualization)

Verified:

- `virsh`, `virt-install`, `qemu-img` installed
- libvirt network `default` active (NAT)
- storage pools available (`images`, `vms`)
- Ubuntu ISO present in lab directory

Representative commands:

```bash
df -h /
virsh --connect qemu:///system list --all
virsh --connect qemu:///system net-list --all
virsh --connect qemu:///system pool-list --all
find /home/chihab -type f -iname 'ubuntu-*.iso'
```

---

## 5. Full detailed solving path

## Phase A - VM provisioning

### A.1 Created base image + thin 50G disk

```bash
sudo curl -L https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img \
  -o /var/lib/libvirt/images/openstack1-base-jammy.img

sudo qemu-img create -f qcow2 -F qcow2 \
  -b /var/lib/libvirt/images/openstack1-base-jammy.img \
  /var/lib/libvirt/images/openstack1.qcow2 50G
```

### A.2 Defined VM with cloud-init

- Name: `openstack1`
- vCPU: 4
- RAM: 8192 MB
- Network: libvirt `default`
- Import mode from cloud image

```bash
sudo virt-install --connect qemu:///system \
  --name openstack1 --memory 8192 --vcpus 4 --cpu host-passthrough \
  --import \
  --disk path=/var/lib/libvirt/images/openstack1.qcow2,format=qcow2,bus=virtio \
  --network network=default,model=virtio \
  --os-variant ubuntu22.04 \
  --graphics none --console pty,target_type=serial \
  --cloud-init user-data=/home/chihab/vms/openstack1/user-data.yaml,meta-data=/home/chihab/vms/openstack1/meta-data.yaml,network-config=/home/chihab/vms/openstack1/network-config.yaml \
  --noautoconsole
```

---

## Phase B - Early networking/debug corrections

### B.1 Wrong IP target identified and corrected

Initial SSH attempts hit a different VM (`Metasploitable2`) with legacy SSH host key algorithms.  
We mapped MAC addresses to leases to isolate `openstack1` correctly.

```bash
sudo virsh --connect qemu:///system domiflist openstack1
sudo virsh --connect qemu:///system net-dhcp-leases default
```

### B.2 Cloud-init NIC naming mismatch

First network-config assumption was too narrow.  
Fix: set cloud-init network match to `en*`, recreate VM, re-lease IP.

### B.3 Static management IP configured

After SSH was stable, set static IP for controller behavior:

- `192.168.122.10/24`
- gateway `192.168.122.1`

```bash
echo 'network: {config: disabled}' | sudo tee /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg
sudo tee /etc/netplan/01-openstack-static.yaml >/dev/null <<'EOF'
network:
  version: 2
  ethernets:
    enp1s0:
      dhcp4: no
      addresses: [192.168.122.10/24]
      routes:
        - to: default
          via: 192.168.122.1
      nameservers:
        addresses: [8.8.8.8, 1.1.1.1]
EOF
sudo chmod 600 /etc/netplan/01-openstack-static.yaml
sudo netplan generate
sudo netplan apply
```

---

## Phase C - Ubuntu preparation

Ensured cloud-init completion, updates, and snap runtime:

```bash
sudo cloud-init status --wait
sudo apt update
sudo apt upgrade -y
sudo apt install -y snapd
sudo systemctl enable --now snapd
snap version
```

Kernel upgrade required reboot; VM was rebooted and access restored.

---

## Phase D - MicroStack installation and initialization

### D.1 Installed MicroStack snap

```bash
sudo snap install microstack --beta --classic
snap list microstack
```

### D.2 Ran first initialization

```bash
sudo microstack init --auto --control
```

Observed successful staging:

- RabbitMQ + MySQL startup
- Keystone bootstrap
- Nova DB migrations
- Neutron configuration
- Glance setup and cirros image
- Cinder service setup

### D.3 Core service checks

```bash
sudo snap services microstack
sudo microstack.openstack endpoint list --service keystone
sudo microstack.openstack image list
sudo microstack.openstack flavor list
```

---

## Phase E - Instance creation path

### E.1 `microstack.launch` path failed

`microstack.launch` attempted to create keys under `/home/root/...` and failed in this environment.  
Switched to direct OpenStack CLI flow.

### E.2 OpenStack-native instance creation

```bash
sudo microstack.openstack keypair create mykey > ~/mykey.pem
chmod 600 ~/mykey.pem

sudo microstack.openstack server create \
  --image cirros \
  --flavor m1.tiny \
  --key-name mykey \
  --network test \
  my-first-vm

sudo microstack.openstack server list
sudo microstack.openstack server show my-first-vm
```

Result: `my-first-vm` reached `ACTIVE` on network `test`.

---

## Phase F - Volume backend issue and final storage fix

### F.1 First volume attempt failed

Volume entered error state and attach failed because loop-backed Cinder LVM backend was not enabled in the initial run.

### F.2 Re-initialized with loop-backed Cinder LVM

```bash
sudo microstack.init --auto --control \
  --setup-loop-based-cinder-lvm-backend \
  --loop-device-file-size 10
```

After this:

- `microstack.cinder-volume` became active
- Volume lifecycle worked

### F.3 Recreated and attached volume successfully

```bash
sudo microstack.openstack volume create --size 1 my-volume
sudo microstack.openstack server add volume my-first-vm my-volume
sudo microstack.openstack volume list
sudo microstack.openstack volume show my-volume
```

Result: `my-volume` status `in-use`, attached to `my-first-vm` (`/dev/vdb`).

---

## 6. Problems encountered, with root cause and solved action

| Problem | Root cause | Solved action |
|---|---|---|
| SSH negotiation error against discovered IP | IP belonged to another VM (`Metasploitable2`) | Mapped `openstack1` MAC to DHCP lease, used correct IP |
| Initial no-lease behavior for `openstack1` | Cloud-init network interface naming mismatch | Recreated VM with network match `en*` |
| Netplan security warning | Netplan file too permissive | Set mode `600` and re-applied |
| `microstack.launch` failed (`/home/root`) | Snap environment path behavior | Used `microstack.openstack server create` path |
| Keypair import via temp path failed | Path/context mismatch in chained commands | Created keypair directly in OpenStack |
| Volume attachment failed (`error` state) | Cinder loop/LVM backend disabled on first init | Re-ran init with loop-backed Cinder flags and recreated volume |
| One CLI command mismatch from guide | Client command set differs (`server volume list`) | Used supported `server add/remove volume`, `volume list/show` |

---

## 7. Final validated state (Lab 1 completion proof)

### 7.1 Infrastructure

- VM `openstack1`: running, autostart enabled
- Static IP: `192.168.122.10`
- Root FS in VM: healthy usage

### 7.2 OpenStack control plane

Active and validated:

- Keystone
- Nova API + Nova compute
- Neutron API
- Glance API
- Horizon
- Cinder volume service (active after backend fix)

### 7.3 Workload resources

- Server: `my-first-vm` -> `ACTIVE`
- Volume: `my-volume` -> `in-use` and attached to server

---

## 8. Explicit command set to demonstrate the completed lab

From host:

```bash
sudo virsh --connect qemu:///system dominfo openstack1 | egrep 'Name:|State:|Autostart:'
ssh -i /home/chihab/.ssh/id_ed25519 chihab@192.168.122.10
```

Inside `openstack1`:

```bash
# Credentials (retrieve, do not hardcode in reports)
sudo snap get microstack config.credentials.keystone-password

# Core services
sudo snap services microstack | egrep 'keystone|glance|neutron|nova|horizon|cinder-volume'

# Endpoint + cloud resources
sudo microstack.openstack endpoint list --service keystone
sudo microstack.openstack image list
sudo microstack.openstack flavor list
sudo microstack.openstack network list
sudo microstack.openstack subnet list
sudo microstack.openstack router list

# Instance and attached volume proof
sudo microstack.openstack server list
sudo microstack.openstack server show my-first-vm | egrep 'status|addresses|flavor|image|vm_state'
sudo microstack.openstack volume list
sudo microstack.openstack volume show my-volume

# Capacity check
sudo microstack.openstack hypervisor stats show
```

---

## 9. Conclusion (Lab 1 only)

Lab 1 objectives were completed end-to-end under disk constraints by using thin-provisioned virtualization and targeted troubleshooting.  
The single-node MicroStack cloud is operational, validated with a running instance and attached block volume, and ready for live demonstration of this lab.
