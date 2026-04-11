# Lab 1 Detailed Guide - OpenStack MicroStack (Single Node)

## 1) What this lab teaches (key concepts)

By doing this lab, you will learn:

1. **Private cloud fundamentals**: how to deploy an OpenStack-based private cloud on one machine.
2. **MicroStack architecture**: how MicroStack packages OpenStack services in a Snap for fast setup.
3. **Core OpenStack services**:
   - **Keystone** (identity/authentication)
   - **Nova** (compute/VM lifecycle)
   - **Neutron** (networking)
   - **Glance** (image catalog)
   - **Cinder** (block storage)
   - **Horizon** (web dashboard)
4. **Infrastructure preparation**: VM sizing, virtualization options, hostname, static IP, and network setup.
5. **Cloud initialization flow**: how `microstack init --auto --control` bootstraps all services.
6. **Admin access and operations**: retrieving credentials, accessing Horizon, and validating running services.
7. **Instance lifecycle management** with CLI:
   - launch, list, show, start/stop, pause/resume, reboot
8. **Cloud resources management**:
   - images, flavors, keypairs, volumes, networks, router/subnet
9. **Operational troubleshooting**: diagnosing failed init, unavailable dashboard, and stuck VM builds.

---

## 2) Lab prerequisites

## 2.1 Hardware and VM prerequisites

Prepare one Ubuntu VM (or physical host) as a **single-node Controller + Compute**.

- **CPU**: 4 vCPUs
- **RAM**: 16 GB
- **Disk**: 50 GB
- **Network**: Bridged adapter (VMnet0)
- **OS**: Ubuntu 22.04 LTS

Recommended identity/network values used in the lab:

- Hostname: `openstack1`
- Domain: `esi.dz`
- Static IP: `192.168.1.10/24`
- Gateway: `192.168.1.1`
- DNS: `8.8.8.8`

## 2.2 VMware settings

In VM settings, ensure:

- **Virtualize Intel VT-x/EPT or AMD-V/RVI** = Enabled
- **Virtualize IOMMU (VT-d / AMD-Vi)** = Enabled
- Ubuntu 22.04 ISO is attached for install

## 2.3 Software prerequisites

- `snapd` installed and running
- internet access to Snap Store (or proper proxy configured)
- `sudo` privileges

---

## 3) Detailed lab steps with explanation

## Step A - System preparation

### A.1 Set hostname

```bash
sudo hostnamectl set-hostname openstack1
bash
```

Why: OpenStack components and network services rely on stable host identity.

### A.2 Update packages and install Snap support

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install snapd -y
sudo systemctl enable snapd
sudo systemctl start snapd
```

Why: Ensures dependency freshness and Snap runtime availability.

### A.3 Configure static IP (Netplan)

Edit:

```bash
sudo nano /etc/netplan/00-installer-config.yaml
```

Suggested content:

```yaml
network:
  version: 2
  ethernets:
    ens33:
      dhcp4: no
      addresses: [192.168.1.10/24]
      gateway4: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8]
```

Apply and verify:

```bash
sudo netplan apply
ip addr show
```

Why: A cloud controller must keep a predictable management IP.

---

## Step B - Install MicroStack

Check Snap works:

```bash
snap version
```

Install MicroStack:

```bash
sudo snap install microstack --beta --classic
```

Verify:

```bash
snap list microstack
```

Why: MicroStack bundles core OpenStack services in one package for single-node deployment.

---

## Step C - Initialize OpenStack services

Run automatic single-node initialization:

```bash
sudo microstack init --auto --control
```

Expected: Keystone, Glance, Nova, Neutron, Cinder, and default networking are configured.

Retrieve admin password:

```bash
sudo snap get microstack config.credentials.keystone-password
```

Check services status:

```bash
sudo snap services microstack
```

Why: Initialization creates the working cloud control plane.

---

## Step D - Access Horizon dashboard

Discover endpoint:

```bash
sudo microstack.openstack endpoint list --service keystone
```

Usually open:

- `http://10.20.20.1/` (internal default)
- or `http://192.168.1.10/` (bridged VM IP)

Login:

- Domain: `admin_domain`
- Username: `admin`
- Password: value returned by `snap get ...keystone-password`

Why: Horizon gives a GUI to manage all cloud resources.

---

## Step E - Create and manage instances

### E.1 List images and flavors

```bash
sudo microstack.openstack image list
sudo microstack.openstack flavor list
```

### E.2 Create SSH keypair for VM access

```bash
ssh-keygen -t rsa -b 2048
sudo microstack.openstack keypair create --public-key ~/.ssh/id_rsa.pub mykey
```

### E.3 Launch first VM

Quick method:

```bash
sudo microstack launch cirros --name my-first-vm
```

Explicit method:

```bash
sudo microstack.openstack server create \
  --image cirros \
  --flavor m1.tiny \
  --key-name mykey \
  --network test \
  my-first-vm
```

List VMs:

```bash
sudo microstack.openstack server list
```

Show VM details/IP:

```bash
sudo microstack.openstack server show my-first-vm
sudo microstack.openstack server show my-first-vm | grep addresses
```

SSH example (Cirros default credentials):

```bash
ssh cirros@<vm-ip>
# password: REDACTED_LAB_PASSWORD
```

---

## Step F - VM lifecycle operations

```bash
sudo microstack.openstack server start my-first-vm
sudo microstack.openstack server stop my-first-vm
sudo microstack.openstack server reboot my-first-vm
sudo microstack.openstack server pause my-first-vm
sudo microstack.openstack server unpause my-first-vm
sudo microstack.openstack server suspend my-first-vm
sudo microstack.openstack server resume my-first-vm
```

Extra checks:

```bash
sudo microstack.openstack server volume list my-first-vm
sudo microstack.openstack port list --server my-first-vm
```

Why: Demonstrates full operational control of compute instances.

---

## Step G - Advanced CLI tasks

### G.1 Upload custom image (Glance)

```bash
wget https://cloud-images.ubuntu.com/focal/current/focal-server-cloudimg-amd64.img
sudo microstack.openstack image create \
  --file focal-server-cloudimg-amd64.img \
  --disk-format qcow2 \
  --container-format bare \
  --public \
  ubuntu-20.04
sudo microstack.openstack image list
```

### G.2 Create and attach volume (Cinder)

```bash
sudo microstack.openstack volume create --size 10 my-volume
sudo microstack.openstack server add volume my-first-vm my-volume
```

### G.3 Inspect network resources (Neutron)

```bash
sudo microstack.openstack network list
sudo microstack.openstack router list
sudo microstack.openstack subnet list
```

### G.4 Check node capacity/usage

```bash
sudo microstack.openstack hypervisor stats show
```

Why: Confirms cloud resource consumption and available capacity.

---

## 4) Validation checklist (what must be true)

- MicroStack snap is installed and listed.
- `microstack init` completed without interruption.
- All MicroStack services are `active`.
- Horizon is reachable via browser.
- You can authenticate as `admin`.
- At least one VM (`my-first-vm`) reaches `ACTIVE`.
- You can list networks/images/flavors using CLI.
- Volume creation and attach command succeed.

---

## 5) Troubleshooting quick commands

If init fails:

```bash
sudo snap remove microstack
sudo snap install microstack --beta --classic
sudo microstack init --auto --control
```

If dashboard is inaccessible:

```bash
sudo microstack.openstack endpoint list
sudo snap services microstack
sudo snap logs microstack.horizon
```

If VM is stuck in BUILD:

```bash
sudo microstack.openstack server show my-first-vm
sudo snap logs microstack.nova-conductor
sudo snap logs microstack.nova-compute
```

---

## 6) Final learning outcome

After this lab, you are able to deploy a functional private cloud on one node, access it via Horizon and CLI, and perform core cloud operations across compute, image, networking, identity, and storage services.
