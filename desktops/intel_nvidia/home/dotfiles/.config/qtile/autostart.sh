#!/usr/bin/bash

setxkbmap -layout "us,ru" -option grp:win_space_toggle
nm-applet &
picom --daemon &
blueman-applet &
feh --bg-scale ~/Pictures/wallpapers/cyberpunk-hd-wallpaper.jpg
