#!/usr/bin/bash

# restart_picom() {
#     echo "$(date): Restarting picom after suspend/unlock" >> /tmp/picom-debug.log
#    sleep 1
#     pkill picom || true
#     sleep 1
#     picom -b &
# }


setxkbmap -layout "us,ru" -option grp:win_space_toggle
nm-applet &
picom --daemon &
blueman-applet &
feh --bg-scale ~/Pictures/wallpapers/cyberpunk-hd-wallpaper.jpg

# Монитор системных событий suspend/resume
# dbus-monitor --system "type='signal',interface='org.freedesktop.login1.Manager',member='PrepareForSleep'" | while read -r line; do
#     if echo "$line" | grep -q "false"; then
#	# dm-tool lock
#	# dm-tool switch-to-greeter
#         echo "$(date): System resumed from suspend" >> /tmp/picom-debug.log
#         restart_picom
# 	dm-tool switch-to-greeter
#     fi
# done &

