import machine
import os
import time
import ubinascii

import devices

from config import Config
from hello import Hello


class App:
    def __init__(self):
        def draw_display():
            def display_clear():
                self.display.set_pen(self.pen_bg)
                self.display.clear()
                self.display.set_pen(self.pen_fg)


            def display_update():
                if self.eink_variable_update_speed:
                    if self.eink_update_count % EINK_UPDATE_REFRESH_INTERVAL == 0:
                        self.display.set_update_speed(EINK_UPDATE_SPEED_SLOW)
                    else:
                        self.display.set_update_speed(EINK_UPDATE_SPEED_FAST)
                    self.eink_update_count += 1
                if self.device["type"] == devices.PRESTO:
                    self.presto.update()
                else:
                    self.display.update()


            display_clear()
            
            hello_y_pos = self.y_border
            self.display.text(f"Hello, {self.hello.name}!", self.x_border, hello_y_pos, scale=self.device["font_scale"]["regular"])

            board_id_title_y_pos = hello_y_pos + (FONT_HEIGHT_BITMAP8 * self.device["font_scale"]["regular"]) + self.y_spacing
            self.display.text("Board ID:", self.x_border, board_id_title_y_pos, scale=self.device["font_scale"]["regular"])
            board_id_y_pos = board_id_title_y_pos + (FONT_HEIGHT_BITMAP8 * self.device["font_scale"]["regular"]) + self.y_spacing
            self.display.text(self.hello.board_id, self.x_spacing * 3, board_id_y_pos, scale=self.device["font_scale"]["large"])

            system_uptime_title_y_pos = board_id_y_pos + (FONT_HEIGHT_BITMAP8 * self.device["font_scale"]["large"]) + self.y_spacing
            self.display.text("System uptime:", self.x_spacing, system_uptime_title_y_pos, scale=self.device["font_scale"]["regular"])
            system_uptime_y_pos = system_uptime_title_y_pos + (FONT_HEIGHT_BITMAP8 * self.device["font_scale"]["regular"]) + self.y_spacing
            self.display.text(self.hello.uptime_string_calculate(), self.x_spacing * 3, system_uptime_y_pos, scale=self.device["font_scale"]["regular"])

            created_scale = self.device["font_scale"]["small"]
            created_text = "Created by Benjamin Howe"
            created_x_pos = self.width - self.display.measure_text(created_text, created_scale) - self.x_border
            created_y_pos = self.height - (FONT_HEIGHT_BITMAP8 * created_scale) - self.y_border
            self.display.text(created_text, created_x_pos, created_y_pos, scale=created_scale)

            mp_version_scale = self.device["font_scale"]["small"]
            mp_version_text = f"MicroPython version: v{self.hello.micropython_version}"
            mp_version_xpos = self.width - self.display.measure_text(mp_version_text, mp_version_scale) - self.x_border
            mp_version_ypos = created_y_pos - self.y_spacing - (FONT_HEIGHT_BITMAP8 * created_scale)
            self.display.text(mp_version_text, mp_version_xpos, mp_version_ypos, scale=mp_version_scale)

            display_update()


        def draw_display_maybe():
            should_draw_display = False
            now_ticks_ms = time.ticks_ms()
            if self.display_last_draw_tms == None:
                should_draw_display = True
            else:
                time_elapsed = time.ticks_diff(now_ticks_ms, self.display_last_draw_tms)
                if time_elapsed > self.display_refresh_ms:
                    should_draw_display = True
            if should_draw_display:
                draw_display()
                self.display_last_draw_tms = now_ticks_ms


        def set_device():
            device_type = self.config.get("DEVICE_TYPE")
            if device_type not in devices.KNOWN_DEVICES:
                raise Exception(f"Device \"{device_type}\" not recognised!")
            self.device = devices.KNOWN_DEVICES[device_type]
            self.device["type"] = device_type

            self.display_refresh_ms = 1000 // 30 # 30 FPS (target!)
            if self.device["display_tech"] == "eink":
                if self.device["colour"]:
                    # colour devices take approximately 40 seconds to refresh
                    self.display_refresh_ms = 300 * 1000
                else:
                    # b&w devices are generally pretty quick to refresh
                    self.display_refresh_ms = 60 * 1000


        def set_dimensions():
            self.width, self.height = self.display.get_bounds()
            self.x_spacing = self.width // 50
            self.y_spacing = self.height // 50
            self.x_border = self.x_spacing
            self.y_border = self.y_spacing
            if self.device["type"] == devices.INKY_PACK:
                self.x_border = 0
                self.y_border = 0


        def set_display():
            if self.device["type"] == devices.INKY_FRAME_4:
                from picographics import PicoGraphics, DISPLAY_INKY_FRAME_4
                self.display = PicoGraphics(DISPLAY_INKY_FRAME_4)
            elif self.device["type"] == devices.INKY_PACK:
                from picographics import PicoGraphics, DISPLAY_INKY_PACK
                self.display = PicoGraphics(DISPLAY_INKY_PACK)
            elif self.device["type"] == devices.PRESTO:
               from presto import Presto
               self.presto = Presto(full_res=True)
               self.display = self.presto.display


        def set_eink_refresh_interval():
            try:
                self.display.set_update_speed(0)
                self.eink_variable_update_speed = True
                self.eink_update_count = 0
            except ValueError:
                self.eink_variable_update_speed = False


        def set_pens():
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


        self.config = Config(filename="config.json")
        set_device()
        self.hello = Hello(
            board_id=ubinascii.hexlify(machine.unique_id()).decode(),
            boot_time=time.time(),
            micropython_version=os.uname().release,
            name=self.device["name"],
        )
        set_display()
        self.display.set_font("bitmap8")
        set_eink_refresh_interval()
        set_pens()
        set_dimensions()
        self.display_last_draw_tms = None
        while True:
            draw_display_maybe()


EINK_BW_BLACK = 0
EINK_BW_WHITE = 15
EINK_COLOUR_BLACK = 0
EINK_COLOUR_WHITE = 1
EINK_UPDATE_REFRESH_INTERVAL = 60
EINK_UPDATE_SPEED_FAST = 2
EINK_UPDATE_SPEED_SLOW = 0
FONT_HEIGHT_BITMAP8 = 8
RGB_BLACK = (0, 0, 0)
RGB_ORANGE = (255, 204, 102)
