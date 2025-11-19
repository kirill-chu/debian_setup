#!/usr/bin/bash


setxkbmap -layout "us,ru" -option grp:win_space_toggle
nm-applet &
blueman-applet &
picom --daemon &
feh --bg-scale ~/Pictures/wallpapers/cyberpunk-hd-wallpaper.jpg
light-locker --lock-on-suspend --lock-on-lid --lock-after-screensaver=60 &
