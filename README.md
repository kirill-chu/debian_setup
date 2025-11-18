### KC's configs for Debian

My setup is:
- Debian 13
- X11
- LightDM
- Qtile
- Picom
- Rofi
- Light-locker
- Blueman-applet
- nm-applet
- feh

This setup has not been completed yet.

I have several different configs for different PC:
- Desktops
- Laptops

#### Desktops
It contains only one config for my old desktop PC. It's intel based system with nvidia GPU and one monitor.

#### Laptops
It contains three configs for:
- MacBook Air 2017 (intel)
- MacBook Pro 2020 (T2, intel)
- Lenovo ThinkBook 14 G4 IAP

Laptops configs will be uploaded soon...

### Known issues
- Auto suspend. I don't want to use gnome, kde, xfce4 power managers. I have not found yet a solution for integrating qtile and logind.
- Macbook Pro 2020 (T2) - has a problem with wake up after suspending. It's a wide known problem https://github.com/t2linux/T2-Debian-and-Ubuntu-Kernel/issues/53
- There are some issues, but they are not really important for me :)

### My own solutions
#### Keyboard layout widget

It turned out that qtile's build in widget did not work properly for me. For example: I'm using rofi and two keyboard layouts 'us' and 'ru' and when I'm working with 'ru' layout and
start rofi I cannot switch to 'us' layout with qtile's build in KeyboardLayout widget. I had to close rofi, switch keyboard layout and start rofi again. I have created a simple widget which only shows a current layout and layouts switching is set up on system level.
