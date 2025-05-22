import ujson


class Config:
    DEFAULT_CONFIG = {
        "EINK_REFRESH_INTERVAL": 60,
        "EINK_UPDATE_SPEED": 2,
        "LOG_LIMIT": 100,
        "NTP_HOST": "time.cloudflare.com",
        "NTP_INTERVAL_HOURS": 4,
        "WIFI_DEBUG_SHOW_HOSTNAME": False,
        "WIFI_DEBUG_SHOW_IP": False,
        "WIFI_DEBUG_SHOW_MAC": False,
        "WIFI_DEBUG_SHOW_SSID": True,
        "WIFI_DEBUG_SUCCESS_SECS": 3,
    }

    SENSITIVE_CONFIG = [
        "WIFI_PASSWORD",
    ]


    def __init__(self, filename):
        self.filename = filename
        self.load()


    def export(self):
        redacted_data = self.data
        for key in self.SENSITIVE_CONFIG:
            if key in redacted_data:
                redacted_data[key] = "***"
        return {
            "default": self.DEFAULT_CONFIG,
            "user": redacted_data,
        }


    def get(self, key):
        if key in self.data:
            return self.data[key]
        elif key in self.DEFAULT_CONFIG:
            return self.DEFAULT_CONFIG[key]
        else:
            return None


    def load(self):
        with open(self.filename) as f:
            self.data = ujson.load(f)
