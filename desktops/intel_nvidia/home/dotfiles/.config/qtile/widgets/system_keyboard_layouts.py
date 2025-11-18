"""
This solution for those who don't use any input method frameworks (IMF/IM) line ibus, fcitx, uim etc.
However if you need to use several keyboard layouts and you don't like how standard widget works,
for example: I'm using rofi and two keyboard layouts 'us' and 'ru' and when I'm working with 'ru' layout and
start rofi I cannot switch to 'us' layout with qtile's standard KeyboardLayout widget.

Perhaps a workaround exists to resolve this issue, but I could not find it.

Because of that I made this solution. I tried to write it like qtile's standard widget.

requirements utils: setxkbmap, xset.

You should setup switching layouts on system level. After that switching layouts starts working in rofi window
and this solution will only show current keyboard layout.

The work of this solution based on parsing LED mask: 00000000. You can use 'get_led_mask.py' script from ../scripts directory
to detect which bits responsible for switching layouts in your system, just run it and switching.

"""

from abc import ABCMeta, abstractmethod
from subprocess import check_output

from libqtile.log_utils import logger
from libqtile.widget import base


class _BaseSystemLayoutBackend(metaclass=ABCMeta):
    def __init__(self, qtile=None):
        """
        This handles getting the keyboard layout with the appropriate util.
        """

    @abstractmethod
    def get_keyboard(self) -> str:
        """
        Return the currently used keyboard layout as a string

        Examples: "us", "ru".  In case of error returns "unknown".
        """

    @abstractmethod
    def get_available_layouts(self) -> str:
        """
        Return the available keyboard layouts as a list

        Examples: ["us", "ru"].  In case of error returns ["unknown"].
        """



class _SystemBackend(_BaseSystemLayoutBackend):
    """
    Default utils are:
    xset - for getting and parsing LED bits.
    setxkbmap - for getting current layouts.
    """

    layout_command = "xset -q"
    layouts_command = "setxkbmap -query"
    layouts = None

    def get_keyboard(self, group_led_bits) -> str:
        """Detecting current layout"""

        try:
            led_mask = self.get_led_mask()
            if led_mask is None:
                return self.layouts[0] if self.layouts else "unknown"
            
            # Detect the group by bit
            group = 0
            for i, bit in enumerate(group_led_bits):
                if led_mask & (1 << bit):
                    group |= (1 << i)
            # group = 1 if (led_mask & (1 << group_led_bits)) else 0
            

            if group < len(self.layouts):
                return self.layouts[group]
            else:
                return self.layouts[0]
                
        except Exception as e:
            logger.error(f"Layout detecting error: {e}")
            return self.layouts[0] if self.layouts else "unknown"

    def get_available_layouts(self) -> list[str]:
        """Getting list of keyboard layouts"""

        try:
            result = check_output(self.layouts_command.split(" ")).decode()

            for line in result.split("\n"):
                if line.startswith('layout:'):
                    layouts = line.split(':')[1].strip().split(',')
                    self.layouts = layouts
                    return layouts
        except Exception as e:
            logger.error(f"Getting layouts error: {e}")
        
        return ["unknown"]

    def get_led_mask(self) -> int | None:
        """Getting current LED mask"""
        
        try:
            result = check_output(self.layout_command.split(" ")).decode()

            for line in result.split('\n'):
                if 'LED mask' in line:
                    mask_str = line.split('LED mask:')[1].strip()
                    clean_mask = mask_str.replace(' ', '')
                    return int(clean_mask, 16)
                    
        except Exception as e:
            logger.error(f"Getting LED mask error: {e}")
        
        return None


class SystemKeyboardLayout(base.InLoopPollText):
    """
    Widget for displaying the current keyboard layout

    This widget was tested only in X11.
    """

    defaults = [
        ("update_interval", 1, "Update time in seconds."),
        (
            "display_map",
            {},
            "Custom display of layout. Key should be in format "
            "'layout variant'. For example: "
            "{'us': 'us', 'lt sgs': 'sgs', 'ru phonetic': 'ru'}",
        ),
        (
            "group_led_bits", [12], 
            "LED mask bit for layouts. One bit is enough for two layouts."
            "However, if you use more than two layouts, you shold use more bits."
            "You can detect which bits are used for layouts by run the script 'get_led_mask.py' and switching your layouts."
        ),
    ]

    def __init__(self, **config):
        base.InLoopPollText.__init__(self, **config)
        self.add_defaults(SystemKeyboardLayout.defaults)

    def _configure(self, qtile, bar):
        base.InLoopPollText._configure(self, qtile, bar)

        self.system_backend = _SystemBackend()
        self.system_backend.get_available_layouts()


    def poll(self):
        keyboard = self.system_backend.get_keyboard(self.group_led_bits)
        if keyboard in self.display_map.keys():
            return self.display_map[keyboard]
        return keyboard.upper()

if __name__ == "__main__":
    system_backend = _SystemBackend()
    system_backend.get_available_layouts()
    print(system_backend.get_keyboard([12]))
