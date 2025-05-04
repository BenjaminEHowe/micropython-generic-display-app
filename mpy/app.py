import machine
import ubinascii

import devices


class App:
    def __init__(self, device_type):
        if device_type not in devices.KNOWN_DEVICES:
            raise Exception(f"Device \"{device_type}\" not recognised!")
        self.device = devices.KNOWN_DEVICES[device_type]
        self.device["type"] = device_type

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
        width, height = self.display.get_bounds()
        x_spacing = width // 50
        y_spacing = height // 50
        x_border = x_spacing
        y_border = y_spacing
        if device_type == devices.INKY_PACK:
            x_border = 0
            y_border = 0

        self.display_clear()
        
        hello_y_pos = y_border
        self.display.text(f"Hello, {self.device['name']}!", x_border, hello_y_pos, scale=self.device["font_scale"]["regular"])
        board_id_title_y_pos = hello_y_pos + (FONT_HEIGHT_BITMAP8 * self.device["font_scale"]["regular"]) + y_spacing

        self.display.text("Board ID:", x_border, board_id_title_y_pos, scale=self.device["font_scale"]["regular"])
        board_id = ubinascii.hexlify(machine.unique_id()).decode()
        board_id_y_pos = board_id_title_y_pos + (FONT_HEIGHT_BITMAP8 * self.device["font_scale"]["regular"]) + y_spacing
        self.display.text(board_id, x_spacing * 3, board_id_y_pos, scale=self.device["font_scale"]["large"])

        created_scale = self.device["font_scale"]["small"]
        created_text = "Created by Benjamin Howe"
        created_x_pos = width - self.display.measure_text(created_text, created_scale) - x_border
        created_y_pos = height - (FONT_HEIGHT_BITMAP8 * created_scale) - y_border
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


EINK_BW_BLACK = 0
EINK_BW_WHITE = 15
EINK_COLOUR_BLACK = 0
EINK_COLOUR_WHITE = 1
FONT_HEIGHT_BITMAP8 = 8
RGB_BLACK = (0, 0, 0)
RGB_ORANGE = (255, 204, 102)
