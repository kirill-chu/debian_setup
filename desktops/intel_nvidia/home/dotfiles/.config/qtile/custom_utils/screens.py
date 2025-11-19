"""
These functions help to work with two monitors.
When second was plugged it becomes available immediately.

These functions were tested only with laptops with one extra plugged monitor.
If you use desktop PC with two monitors probably you should make some extra changes.


Author: kirill-chu <nefka2006@yandex.ru>

"""

import subprocess
from pathlib import Path

from libqtile import bar, widget
from libqtile.config import Screen

from widgets.system_keyboard_layouts import SystemKeyboardLayout

DATE_FORMAT = "%d-%m-%Y %a %H:%M"

home = Path.home()
icon_path = Path(home, ".local/share/icons/hicolor/48x48/apps")

def create_primary_bar():
    """The panel for main monitor."""

    return bar.Bar([
        widget.CurrentLayoutIcon(),
        widget.GroupBox(
            highlight_method="line",
            this_current_screen_border="#ff5555",
            this_screen_border="#50fa7b",
            other_current_screen_border="#f1fa8c",
            other_screen_border="#44475a",
        ),
        widget.WindowName(),
        widget.LaunchBar(
            progs=[(f"{icon_path}/yandex_music.png","chromium --profile-directory='Default' --app='https://yandex.ru/music'", "Yandex Music")]
        ),
        widget.Sep(
            linewidth=5,
            foreground = "#000000",
        ),
        SystemKeyboardLayout(
            display_map={'us': 'EN', 'ru': 'RU'},
            group_led_bits=[12],
        ),
        widget.TextBox(
            text = '|',
            font = "Ubuntu Mono",
            foreground = "#44475a",
            padding = 2,
            fontsize = 14
        ),
        widget.Volume(
            fmt=' {}',
            step=5,
            volume_app="pavucontrol"
        ),
        widget.Sep(
            linewidth=5,
            foreground = "#000000",
        ),
        widget.Systray(),
        widget.Clock(format=DATE_FORMAT),
    ], 24)

def create_secondary_bar():
    """The panel for extra monitor."""

    return bar.Bar([
        widget.CurrentLayoutIcon(),
        widget.GroupBox(
            highlight_method='line',
            this_current_screen_border='#ff5555',
            this_screen_border='#50fa7b',
            other_current_screen_border='#f1fa8c',
            other_screen_border='#44475a',
        ),
        widget.WindowName(),
        widget.LaunchBar(
            progs=[(f"{icon_path}/yandex_music.png","chromium --profile-directory='Default' --app='https://yandex.ru/music'", "Yandex Music")]
        ),
        widget.Sep(
            linewidth=5,
            foreground = "#000000",
        ),
        SystemKeyboardLayout(
            display_map={'us': 'EN', 'ru': 'RU'},
            group_led_bits=[12],
        ),
        widget.TextBox(
            text = '|',
            font = "Ubuntu Mono",
            foreground = "#44475a",
            padding = 2,
            fontsize = 14
        ),
        widget.Sep(
            linewidth=5,
            foreground = "#000000",
        ),
        widget.Clock(format=DATE_FORMAT),
    ], 24)

def setup_screens():
    """Dynamicaly setting up the connected screens."""

    screens = []
    # Checking connected screens
    try:
        result = subprocess.run(["xrandr"], capture_output=True, text=True)
        xrandr_output = result.stdout

        # Checking trully connected monitors
        monitors = []
        for line in xrandr_output.split("\n"):
            if " connected" in line:
                monitor_name = line.split()[0]
                monitors.append(monitor_name)
        
        # Create screen for each connected monitor
        for i, monitor in enumerate(monitors):
            if i == 0:
                screens.append(Screen(
                    top=create_primary_bar(),
                ))
            else:
                screens.append(Screen(
                    top=create_secondary_bar(),
                ))
    except Exception as e:
        # Fallback: ceate only one screen if something went wrong
        screens.append(Screen(top=create_primary_bar()))
    
    return screens

def configure_monitors():
    """Setting up monitors by via xrandr."""

    try:
        result = subprocess.run(["xrandr", "--query"], capture_output=True, text=True)
        lines = result.stdout.split("\n")

        connected = []
        for line in lines:
            if " connected" in line:
                monitor = line.split()[0]
                connected.append(monitor)
        if len(connected) == 1:
            subprocess.run([
                "xrandr", "--output", connected[0], "--auto", "--primary",
                "--output", "HDMI-1", "--off",
                "--output", "HDMI-2", "--off",
                "--output", "DP-1", "--off"
            ])
        elif len(connected) >= 2:
            laptop = next((m for m in connected if "eDP" in m or "LVSD" in m), connected[0])
            external = next((m for m in connected if m != laptop), connected[1])
            subprocess.run([
                "xrandr",
                "--output", laptop, "--auto", "--primary", "--pos", "0x0",
                "--output", external, "--auto", "--right-of", laptop
            ])
    except Exception as e:
        print(f"Error configuring monitors: {e}")


