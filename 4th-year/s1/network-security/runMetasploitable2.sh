#!/bin/bash

sudo virsh list --all
sudo virsh start Metasploitable2
sudo virsh vncdisplay Metasploitable2
virt-viewer --connect qemu:///system Metasploitable2 &
