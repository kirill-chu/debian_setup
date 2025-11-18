#!/usr/bin/env bash

# Static IP VM
VM_IP="192.168.122.5"

# Function is asking creds through Rofi
get_credentials() {
    if [ $# -eq 0 ]; then
        # If starterd without args - asking both
        USERNAME=$(rofi -dmenu -p "👤 Username for $VM_IP:" -lines 0)
        [ -z "$USERNAME" ] && exit 1
        
        PASSWORD=$(rofi -dmenu -password -p "🔒 Password for $USERNAME:" -lines 0)
        [ -z "$PASSWORD" ] && exit 1
    else
        # If firts args exists asking password
        USERNAME="$1"
        PASSWORD=$(rofi -dmenu -password -p "🔒 Password for $USERNAME:" -lines 0)
        [ -z "$PASSWORD" ] && exit 1
    fi
    
    # Return
    echo "$USERNAME"
    echo "$PASSWORD"
}

# Getting creds
if [ $# -eq 1 ]; then
    # If first args exists
    CREDENTIALS=$(get_credentials "$1")
else
    # Without args
    CREDENTIALS=$(get_credentials)
fi

# Retrieving username and password
USERNAME=$(echo "$CREDENTIALS" | head -n1)
PASSWORD=$(echo "$CREDENTIALS" | tail -n1)

# Notify about connecting
dunstify -t 3000 "RDP Connection" "🔄 Connecting to $VM_IP as $USERNAME..."

# Connecting via xfreerdp3
echo "Trying RDP connection to $VM_IP with user: $USERNAME" > /tmp/rdp_debug.log

# Option 1: Sending a password via a temp file
# {
#     TMP_PASS=$(mktemp)
#     echo "$PASSWORD" > "$TMP_PASS"
#     xfreerdp3 /u:"$USERNAME" /v:"$VM_IP" /p:"$(cat "$TMP_PASS")" -grab-keyboard /dynamic-resolution &
#     RDP_PID=$!
#     wait $RDP_PID
#     RDP_EXIT_CODE=$?
#     rm -f "$TMP_PASS"

    # Checking connection results
#     if [ $RDP_EXIT_CODE -eq 0 ]; then
#         dunstify -u normal "RDP Connection" "✅ Successfully connected to $VM_IP"
#     else
#         dunstify -u critical "RDP Connection" "❌ Failed to connect to $VM_IP (Code: $RDP_EXIT_CODE)"
#     fi

#     exit $RDP_EXIT_CODE
# } &


# Option 2: Sending a password via stdin
{
    echo "$PASSWORD" | xfreerdp3 /u:"$USERNAME" /v:"$VM_IP" /from-stdin -grab-keyboard /dynamic-resolution &
    RDP_PID=$!
    wait $RDP_PID

    RDP_EXIT_CODE=$?

    # Checking connection results
    if [ $RDP_EXIT_CODE -eq 0 ]; then
        dunstify -u normal "RDP Connection" "✅ Successfully connected to $VM_IP"
    else
        dunstify -u critical "RDP Connection" "❌ Failed to connect to $VM_IP (Code: $RDP_EXIT_CODE)"
    fi

    exit $RDP_EXIT_CODE

} &



CONNECTION_PID=$!

# Notify about started process
dunstify -t 2000 "RDP Connection" "🔌 RDP connection started (PID: $CONNECTION_PID)"

# Option 2: Sending a password via stdin
# echo "$PASSWORD" | xfreerdp3 /u:"$USERNAME" /v:"$VM_IP" /p:stdin -grab-keyboard /dynamic-resolution /cert-ignore

# Checking connection results
# if [ $RDP_EXIT_CODE -eq 0 ]; then
#     dunstify -u normal "RDP Connection" "✅ Successfully connected to $VM_IP"
# else
#     dunstify -u critical "RDP Connection" "❌ Failed to connect to $VM_IP (Code: $RDP_EXIT_CODE)"
# fi
