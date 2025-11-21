# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import re
import subprocess
from pathlib import Path

import libqtile.resources
from libqtile import layout, qtile, hook
from libqtile.config import Click, Drag, Group, Key, Match
from libqtile.lazy import lazy
from libqtile.log_utils import logger
from libqtile.utils import guess_terminal
from libqtile.widget import backlight

# from widgets.system_keyboard_layouts import SystemKeyboardLayout
from custom_utils.screens import configure_monitors, setup_screens

mod = "mod4"
terminal = guess_terminal()
home = Path.home()
qtile_config = Path(home, ".config/qtile")
scripts_dir = Path(qtile_config, "scripts")
autostart = Path(qtile_config, "autostart.sh")

os.environ["QT_QPA_PLATFORMTHEME"] = "qt6ct"

# Workaround for current_window issue
def patch_qtile_bug():
    try:
        from libqtile.backend.x11 import core as x11_core

        original_handle_DestroyNotify = x11_core.Core.handle_DestroyNotify

        def patched_handle_DestroyNotify(self, event):
            try:
                return original_handle_DestroyNotify(self, event)
            except AttributeError as e:
                if "current_window" in str(e):
                    logger.warning("Suppressed current_window AttributeError")
                    return
                raise

        x11_core.Core.handle_DestroyNotify = patched_handle_DestroyNotify
        logger.info("Applied Qtile bug patch")
    except Exception as e:
        logger.warning(f"Could not apply Qtile patch: {e}")

# Apply
patch_qtile_bug()

@hook.subscribe.startup_once
def autostart_once():
    home = os.path.expanduser("~")
    subprocess.run(os.path.join(home, ".config", "qtile", "autostart.sh"))

@hook.subscribe.startup
def startup():
    """Startup func."""
    configure_monitors()

@hook.subscribe.screen_change
def on_screen_change(event):
    """Running when a monitor plugged/unplugged."""

    configure_monitors()
    import time
    time.sleep(1)
    qtile.cmd_reconfigure_screens()

@hook.subscribe.screens_reconfigured
def after_screens_reconfigured():
    """Callback after automatic reconfiguration screens Qtile."""
    pass


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html

    # Switch between windows
    Key([mod], "left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "n", lazy.layout.next(), desc="Move window focus to other window"),
    
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "up", lazy.layout.shuffle_up(), desc="Move window up"),
    
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "z", lazy.layout.normalize(), desc="Reset all window sizes"),
    
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], 25, lazy.window.kill(), desc="Kill focused window (mod+w)"),
    Key([mod], 41, lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window (mod+f)"),
    Key([mod], 28, lazy.window.toggle_floating(), desc="Toggle floating on the focused window (mod+t)"),
    
    # Switch focus of monitors
    Key([mod], 60, lazy.next_screen(), desc="Move focus to next monitor, (mod+period)"),
    Key([mod], 59, lazy.prev_screen(), desc="Move focus to previous monitor (mod+comma)"),

    # Multimedia keys
    # Backlight
    Key([], "XF86MonBrightnessUp", lazy.widget['backlight'].change_backlight(backlight.ChangeDirection.UP)),
    Key([], "XF86MonBrightnessDown", lazy.widget['backlight'].change_backlight(backlight.ChangeDirection.DOWN)),
    # Volume
    Key([], "XF86AudioLowerVolume", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%+")),
    Key([], "XF86AudioMute", lazy.spawn("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle")),
  
    # Tools
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], 27, lazy.spawn("rofi -show drun -show-icons"), desc="Spawn a dmenu (mod+r)"),
    Key([mod], 43, lazy.spawn("alacritty -e htop"), desc="Launch htop (mod+h)"),
    Key([mod], 46, lazy.spawn("loginctl lock-session"), desc="Locking you screen (mod+l)"),
    Key([mod, "shift"], 42, lazy.spawn("flameshot gui"), desc="Take a screenshot (mod+sift+g)"),
    # Start VMs
    Key([mod, "control"], 39, lazy.spawn(f"{scripts_dir}/rofi_vm_launcher.sh"), desc="Start rofi menu (mod+csstrl+s)"),
    # Connect to ... via rdp
    Key([mod], 40, lazy.spawn(f"{str(scripts_dir)}/rdp_connector.py"), desc="Run xfreerdp3 connect menu, (mod+d)"),

    # Qtile management
    Key([mod, "control"], 27, lazy.reload_config(), desc="Reload the config (mod+ctrl+r)"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


# groups = [Group(i) for i in "123456789"]
groups = [
    Group("1", label="cmd"),
    Group("2", label="web", matches=[Match(wm_class=re.compile(r"^(chromium)$"))]),
    Group("3", label="dev"),
    Group("4", label="chats"),
    Group("5", label="mm", matches=[Match(wm_class=re.compile(r"^(yandex.ru__music)$"))]),
    Group("6", label="rdp", matches=[Match(wm_class=re.compile(r"^(org.remmina.Remmina)$|^(xfreerdp)$"))]),
    Group("7", label="email", matches=[Match(wm_class=re.compile("^(org.gnome.Evolution)$"))]),
]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    # layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    layout.Bsp(
        border_focus=["#8f3d3d"],
        border_focus_stack=["#d75f5f", "#8f3d3d"],
        border_on_single=True,
        border_width=2,
        margin=8
    ),
    layout.Max(border_focus=["#8f3d3d"], margin=8, border_width=2),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="sans",
    fontsize=14,
    padding=2,
)
extension_defaults = widget_defaults.copy()

logo = os.path.join(os.path.dirname(libqtile.resources.__file__), "logo.png")

screens = setup_screens()

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),     # gitk
        Match(wm_class="makebranch"),       # gitk
        Match(wm_class="maketag"),          # gitk
        Match(wm_class="ssh-askpass"),      # ssh-askpass
        Match(wm_class="pavucontrol"),      # pavucontrol
        Match(wm_class="display-im7.q16"),  # ImageMagick, preview in Thunar
        Match(title="branchdialog"),        # gitk
        Match(title="pinentry"),            # GPG key password entry
        Match(title="Qalculate!"),          # Qalculate!
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
focus_previous_on_window_remove = False
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
