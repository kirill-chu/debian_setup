#!/usr/bin/env bash

# Checking args
if [ $# -eq 0 ]; then
    dunstify -u critical "VM Manager" "❌ You did not enter the VM name."
    exit 1
fi

VM_NAME="$1"

# Starting VM
dunstify -t 3000 "VM Manager" "🔄 Starting $VM_NAME..."
if virsh --connect qemu:///system start "$VM_NAME" 2>/dev/null; then
    dunstify -u normal "VM Manager" "✅ $VM_NAME was started successfully"
else
    # Checkign status
    VM_STATUS=$(virsh --connect qemu:///system  domstate "$VM_NAME" 2>/dev/null)
    case "$VM_STATUS" in
        "running")
            dunstify -u low "VM Manager" "ℹ️ $VM_NAME has been already started."
            ;;
        "")
            dunstify -u critical "VM Manager" "❌ VM $VM_NAME does not exists!"
            ;;
        *)
            dunstify -u critical "VM Manager" "❌ Starting error $VM_NAME (Status: $VM_STATUS)"
            ;;
    esac
fi
