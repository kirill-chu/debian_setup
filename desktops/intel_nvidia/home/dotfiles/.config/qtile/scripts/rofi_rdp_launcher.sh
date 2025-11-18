#!/usr/bin/env bash

rdp_connection="$HOME/.config/qtile/scripts/vm_win11_rdp.sh"

# Show menu
SELECTED_USER=$(echo -e ".\\username\nadministrator\nguest\nother" | rofi -dmenu -p "👤 Select user for RDP:")

if [ -n "$SELECTED_USER" ]; then
    if [ "$SELECTED_USER" = "other" ]; then
        # Starting without username
        $rdp_connection
    else
        # Starting with username
	echo $rdp_connection
        $rdp_connection "$SELECTED_USER"
    fi
fi
