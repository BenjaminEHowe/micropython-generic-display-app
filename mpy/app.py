import machine
import time
import ubinascii

import devices


class App:
    def __init__(self, device_type):
        if device_type not in devices.KNOWN_DEVICES:
            raise Exception(f"Device \"{device_type}\" not recognised!")
        self.device = devices.KNOWN_DEVICES[device_type]
        self.device["type"] = device_type

        self.boot_time = time.time()

        if device_type == devices.INKY_FRAME_4:
            from picographics import PicoGraphics, DISPLAY_INKY_FRAME_4
            self.display = PicoGraphics(DISPLAY_INKY_FRAME_4)
        elif device_type == devices.INKY_PACK:
            from picographics import PicoGraphics, DISPLAY_INKY_PACK
            self.display = PicoGraphics(DISPLAY_INKY_PACK)
        elif device_type == devices.PRESTO:
           from presto import Presto
           self.presto = Presto(full_res=True)
           self.display = self.presto.display

        if not self.device["colour"]:
            self.pen_fg = EINK_BW_BLACK
            self.pen_bg = EINK_BW_WHITE
        else:
            if self.device["display_tech"] == "lcd":
                self.pen_fg = self.display.create_pen(*RGB_ORANGE)
                self.pen_bg = self.display.create_pen(*RGB_BLACK)
            elif self.device["display_tech"] == "eink":
                self.pen_fg = EINK_COLOUR_BLACK
                self.pen_bg = EINK_COLOUR_WHITE

        self.display.set_font("bitmap8")
        self.width, self.height = self.display.get_bounds()
        self.x_spacing = self.width // 50
        self.y_spacing = self.height // 50
        self.x_border = self.x_spacing
        self.y_border = self.y_spacing
        if device_type == devices.INKY_PACK:
            self.x_border = 0
            self.y_border = 0

        self.timers = {}
        self.draw_display(None)
        screen_refresh_seconds = 1
        if self.device["display_tech"] == "eink":
            if self.device["colour"]:
                # colour devices take approximately 40 seconds to refresh
                screen_refresh_seconds = 360
            else:
                # b&w devices are generally pretty quick to refresh
                screen_refresh_seconds = 60
        self.timers["draw_display"] = machine.Timer(period=screen_refresh_seconds*1000, callback=self.draw_display)


    def draw_display(self, timer):
        self.display_clear()
        
        hello_y_pos = self.y_border
        self.display.text(f"Hello, {self.device['name']}!", self.x_border, hello_y_pos, scale=self.device["font_scale"]["regular"])

        board_id_title_y_pos = hello_y_pos + (FONT_HEIGHT_BITMAP8 * self.device["font_scale"]["regular"]) + self.y_spacing
        self.display.text("Board ID:", self.x_border, board_id_title_y_pos, scale=self.device["font_scale"]["regular"])
        board_id = ubinascii.hexlify(machine.unique_id()).decode()
        board_id_y_pos = board_id_title_y_pos + (FONT_HEIGHT_BITMAP8 * self.device["font_scale"]["regular"]) + self.y_spacing
        self.display.text(board_id, self.x_spacing * 3, board_id_y_pos, scale=self.device["font_scale"]["large"])

        system_uptime_title_y_pos = board_id_y_pos + (FONT_HEIGHT_BITMAP8 * self.device["font_scale"]["large"]) + self.y_spacing
        self.display.text("System uptime:", self.x_spacing, system_uptime_title_y_pos, scale=self.device["font_scale"]["regular"])
        system_uptime_y_pos = system_uptime_title_y_pos + (FONT_HEIGHT_BITMAP8 * self.device["font_scale"]["regular"]) + self.y_spacing
        self.display.text(uptime_string_calculate(self.boot_time, time.time()), self.x_spacing * 3, system_uptime_y_pos, scale=self.device["font_scale"]["regular"])

        created_scale = self.device["font_scale"]["small"]
        created_text = "Created by Benjamin Howe"
        created_x_pos = self.width - self.display.measure_text(created_text, created_scale) - self.x_border
        created_y_pos = self.height - (FONT_HEIGHT_BITMAP8 * created_scale) - self.y_border
        self.display.text(created_text, created_x_pos, created_y_pos, scale=created_scale)

        self.display_update()


    def display_clear(self):
        self.display.set_pen(self.pen_bg)
        self.display.clear()
        self.display.set_pen(self.pen_fg)


    def display_update(self):
        if self.device["type"] == devices.PRESTO:
            self.presto.update()
        else:
            self.display.update()


def plural_simple_if_reqd(unit, string):
    if unit == 1:
        return f"{unit} {string}"
    else:
        return f"{unit} {string}s"


def uptime_string_calculate(boot_time, current_time):
    seconds = current_time - boot_time
    minutes = seconds // 60
    hours = minutes // 60
    days = hours // 24
    if days:
        return uptime_string_generate(days, "day", 24, hours, "hour")
    if hours:
       return uptime_string_generate(hours, "hour", 60, minutes, "minute")
    if minutes:
        return uptime_string_generate(minutes, "minute", 60, seconds, "second")
    if seconds:
        return plural_simple_if_reqd(seconds, "second")
    return "0 seconds"


def uptime_string_generate(major_unit, major_unit_name, minor_unit_per_major, minor_unit, minor_unit_name):
    minor_unit = minor_unit - (major_unit * minor_unit_per_major)
    major_unit_string = plural_simple_if_reqd(major_unit, major_unit_name)
    if minor_unit:
        return major_unit_string + ", " + plural_simple_if_reqd(minor_unit, minor_unit_name)
    else:
        return major_unit_string


EINK_BW_BLACK = 0
EINK_BW_WHITE = 15
EINK_COLOUR_BLACK = 0
EINK_COLOUR_WHITE = 1
FONT_HEIGHT_BITMAP8 = 8
RGB_BLACK = (0, 0, 0)
RGB_ORANGE = (255, 204, 102)
