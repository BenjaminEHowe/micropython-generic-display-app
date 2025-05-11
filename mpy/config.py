import ujson


class Config:
    DEFAULT_CONFIG = {
        "EINK_REFRESH_INTERVAL": 60,
        "EINK_UPDATE_SPEED": 2,
    }


    def __init__(self, filename):
        self.filename = filename
        self.load()


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
