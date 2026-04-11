# Lab 1 Execution Report - MicroStack on libvirt

## 1. Final outcome

Lab setup is complete and operational.

- **Controller/Compute VM**: `openstack1` (libvirt)
- **VM resources**: 4 vCPU, 8 GB RAM, 50 GB virtual disk (thin qcow2)
- **Ubuntu**: 22.04.5 LTS
- **Management IP**: `192.168.122.10/24`
- **MicroStack**: installed and initialized as single-node control+compute
- **Services active**: Keystone, Nova, Neutron, Glance, Horizon, Cinder volume backend
- **Test instance**: `my-first-vm` (`ACTIVE`)
- **Test volume**: `my-volume` attached to `my-first-vm` (`/dev/vdb`)

---

## 2. Why this design worked with low disk space

You asked for a 50 GB VM but host disk was limited.  
Solution used:

- **Thin-provisioned qcow2** disk:
  - VM sees 50 GB virtual capacity
  - Host consumes only what is actually written

This satisfied lab requirements without allocating 50 GB physically upfront.

---

## 3. Step-by-step solving process (what was done)

## Step 1 - Host/libvirt assessment

Checked:

- host free disk
- libvirt daemon state
- existing VMs/networks/pools
- ISO locations

Key commands:

```bash
df -h /
virsh --connect qemu:///system list --all
virsh --connect qemu:///system net-list --all
virsh --connect qemu:///system pool-list --all
find /home/chihab -type f -iname 'ubuntu-*.iso'
```

## Step 2 - Ubuntu VM provisioning (`openstack1`)

Created VM using Ubuntu cloud image + cloud-init:

- hostname set to `openstack1`
- SSH key injected
- 4 vCPU / 8 GB RAM / 50 GB thin disk

Key commands:

```bash
sudo curl -L https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img \
  -o /var/lib/libvirt/images/openstack1-base-jammy.img

sudo qemu-img create -f qcow2 -F qcow2 \
  -b /var/lib/libvirt/images/openstack1-base-jammy.img \
  /var/lib/libvirt/images/openstack1.qcow2 50G

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

## Step 3 - Network stabilization

Initial boot was reachable, then static IP was applied per lab style:

- disabled cloud-init network rewrites
- netplan static config applied
- fixed netplan file permissions

Final network:

- `enp1s0: 192.168.122.10/24`
- gateway `192.168.122.1`

Key commands:

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

## Step 4 - Ubuntu prep + snap

Updated VM and ensured snapd:

```bash
sudo cloud-init status --wait
sudo apt update
sudo apt upgrade -y
sudo apt install -y snapd
sudo systemctl enable --now snapd
snap version
```

## Step 5 - MicroStack install/init

Installed MicroStack and initialized single-node control plane:

```bash
sudo snap install microstack --beta --classic
sudo microstack init --auto --control
```

Then validated:

```bash
sudo snap services microstack
sudo microstack.openstack endpoint list --service keystone
sudo microstack.openstack image list
sudo microstack.openstack flavor list
```

## Step 6 - First VM creation

Created OpenStack keypair and launched first instance with CLI:

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

## Step 7 - Cinder backend fix + volume attach

Default run had no active block backend for lab volume attach.  
Re-initialized with loop-backed Cinder LVM:

```bash
sudo microstack.init --auto --control \
  --setup-loop-based-cinder-lvm-backend \
  --loop-device-file-size 10
```

Then:

```bash
sudo microstack.openstack volume create --size 1 my-volume
sudo microstack.openstack server add volume my-first-vm my-volume
sudo microstack.openstack volume list
```

## Step 8 - Reliability improvement

Enabled autostart for `openstack1`:

```bash
sudo virsh --connect qemu:///system autostart openstack1
```

---

## 4. Issues faced, root causes, and fixes

| Issue | Symptom | Root cause | Fix |
|---|---|---|---|
| Wrong VM IP used initially | SSH negotiation failed (`ssh-rsa,ssh-dss`) | Connected to old `Metasploitable2` lease, not `openstack1` | Matched libvirt interface MAC to DHCP lease, used correct IP |
| Cloud-init NIC mismatch at first attempt | No IP assigned to expected interface | Interface naming assumption was too strict | Rebuilt VM cloud-init network matching `en*` |
| Netplan warning | `Permissions ... too open` | Netplan file mode too permissive | `chmod 600` then `netplan apply` |
| `microstack.launch` failure | Tried writing under `/home/root/...` | Environment/home-path behavior in this snap context | Used `microstack.openstack server create` directly |
| Keypair import failure (`/tmp/mykey.pub`) | File not found from snap side | Path/context mismatch during command chain | Created keypair fully via OpenStack CLI (`keypair create mykey`) |
| Volume attach failed (`volume in error`) | Cinder volume stayed in `error` | Cinder loop/LVM backend not enabled in first init | Re-ran init with `--setup-loop-based-cinder-lvm-backend`, recreated volume |
| OpenStack CLI command mismatch | `server volume list` unsupported | Client version command set differs | Used `server add volume`, `server show`, and `volume list/show` |

---

## 5. What went right

1. Host had enough cleaned disk to proceed safely.
2. Thin-provisioned 50 GB VM met lab size requirement without overconsuming host storage.
3. Hardware virtualization (`/dev/kvm`) available and detected by MicroStack.
4. MicroStack initialization completed successfully with all core services active.
5. Compute, networking, image, identity, and storage paths were validated with real resources.

---

## 6. Explicit commands to showcase the lab (demo script)

Run from host:

```bash
# VM is running and autostart-enabled
sudo virsh --connect qemu:///system dominfo openstack1 | egrep 'Name:|State:|Autostart:'

# Enter controller VM
ssh -i /home/chihab/.ssh/id_ed25519 chihab@192.168.122.10
```

Run inside `openstack1`:

```bash
# 1) Get admin password for Horizon/API usage
sudo snap get microstack config.credentials.keystone-password

# 2) Core services
sudo snap services microstack | egrep 'keystone|glance|neutron|nova|horizon|cinder-volume'

# 3) Endpoint and resources
sudo microstack.openstack endpoint list --service keystone
sudo microstack.openstack image list
sudo microstack.openstack flavor list
sudo microstack.openstack network list
sudo microstack.openstack subnet list
sudo microstack.openstack router list

# 4) Instance + volume proof
sudo microstack.openstack server list
sudo microstack.openstack server show my-first-vm | egrep 'status|addresses|flavor|image|vm_state'
sudo microstack.openstack volume list
sudo microstack.openstack volume show my-volume

# 5) Capacity
sudo microstack.openstack hypervisor stats show
```

---

## 7. Full OpenStack usage guide for next labs

## 7.1 Identity/project basics

```bash
sudo microstack.openstack project list
sudo microstack.openstack user list
sudo microstack.openstack role list
```

Create project/user and grant role:

```bash
sudo microstack.openstack project create lab2-project
sudo microstack.openstack user create --password 'REDACTED_LAB_PASSWORD' lab2-user
sudo microstack.openstack role add --project lab2-project --user lab2-user member
```

## 7.2 Images and flavors

```bash
sudo microstack.openstack image list
sudo microstack.openstack flavor list
```

Upload custom cloud image:

```bash
wget https://cloud-images.ubuntu.com/focal/current/focal-server-cloudimg-amd64.img
sudo microstack.openstack image create \
  --file focal-server-cloudimg-amd64.img \
  --disk-format qcow2 \
  --container-format bare \
  --public ubuntu-20.04
```

## 7.3 Networking

```bash
sudo microstack.openstack network list
sudo microstack.openstack subnet list
sudo microstack.openstack router list
sudo microstack.openstack security group list
sudo microstack.openstack security group rule list default
```

Add ping + SSH rules:

```bash
sudo microstack.openstack security group rule create --proto icmp default
sudo microstack.openstack security group rule create --proto tcp --dst-port 22 default
```

## 7.4 Compute lifecycle

```bash
sudo microstack.openstack server create --image cirros --flavor m1.tiny --network test --key-name mykey vm2
sudo microstack.openstack server list
sudo microstack.openstack server show vm2
sudo microstack.openstack server stop vm2
sudo microstack.openstack server start vm2
sudo microstack.openstack server reboot vm2
sudo microstack.openstack server delete vm2
```

## 7.5 Storage lifecycle

```bash
sudo microstack.openstack volume create --size 2 data-vol
sudo microstack.openstack volume list
sudo microstack.openstack server add volume my-first-vm data-vol
sudo microstack.openstack volume show data-vol
sudo microstack.openstack server remove volume my-first-vm data-vol
sudo microstack.openstack volume delete data-vol
```

## 7.6 Observability and troubleshooting

```bash
sudo snap services microstack
sudo snap logs microstack.nova-compute -n 100
sudo snap logs microstack.neutron-api -n 100
sudo snap logs microstack.cinder-volume -n 100
sudo microstack.openstack hypervisor stats show
sudo microstack.openstack server show <vm-name>
```

## 7.7 Recovery patterns

Reinitialize core setup:

```bash
sudo microstack init --auto --control
```

Re-enable loop-backed Cinder:

```bash
sudo microstack.init --auto --control \
  --setup-loop-based-cinder-lvm-backend \
  --loop-device-file-size 10
```

---

## 8. Important notes for future labs

1. This environment uses **NAT network (`192.168.122.0/24`)** under libvirt default network.
2. If your next lab requires LAN access from external devices, switch to bridged networking and adapt netplan accordingly.
3. Loop-backed Cinder backend is fine for lab/testing, not production.
4. Keep VM disk thin-provisioned to preserve host storage.
5. Always validate with `server list`, `volume list`, and `snap services microstack` before submission/demo.

---

## 9. Quick next-lab checklist

```bash
# inside openstack1
sudo snap services microstack | grep active
sudo microstack.openstack server list
sudo microstack.openstack volume list
sudo microstack.openstack network list
sudo microstack.openstack hypervisor stats show
```

If all commands return healthy output, the platform is ready for the next TP.
