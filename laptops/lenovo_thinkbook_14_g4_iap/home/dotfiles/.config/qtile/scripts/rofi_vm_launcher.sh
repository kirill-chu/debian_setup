#!/usr/bin/env bash


# Getting list of VM names
VMS=$(virsh --connect qemu:///system list --all --name | grep -v '^$')

# Showing rofi menu and remembering selection
SELECTED=$(echo "$VMS" | rofi -dmenu -p "🖥 Start VM:")

# If selected run the main script
if [ -n "$SELECTED" ]; then
    dunstify -a rofi "VM Selector" "VM $SELECTED selected $(pwd)"
    .config/qtile/scripts/start_vm.sh "$SELECTED"
fi
