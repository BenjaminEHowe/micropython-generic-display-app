import ujson


class Config:
    def __init__(self, filename):
        self.filename = filename
        self.load()


    def get(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return None


    def load(self):
        with open(self.filename) as f:
            self.data = ujson.load(f)
