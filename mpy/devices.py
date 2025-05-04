INKY_FRAME_4 = "inky_frame_4"
INKY_PACK = "inky_pack"
PRESTO = "presto"

KNOWN_DEVICES = {
    INKY_FRAME_4: {
        "colour": True,
        "display_tech": "eink",
        "font_scale": {
            "small": 2,
            "regular": 4,
            "large": 6,
        },
        "name": "Inky Frame 4\"",
    },
    INKY_PACK: {
        "colour": False,
        "display_tech": "eink",
        "font_scale": {
            "small": 1,
            "regular": 2,
            "large": 3,
        },
        "name": "Inky Pack",
    },
    PRESTO: {
        "colour": True,
        "display_tech": "lcd",
        "font_scale": {
            "small": 2,
            "regular": 3,
            "large": 5,
        },
        "name": "Presto",
    },
}
