import logging


class LogHandler(logging.Handler):
    history = []


    def __init__(self, history_limit):
        self.history_limit = history_limit


    def emit(self, record):
        log_message = f"{record.ct} [{record.levelname}] {record.message}"
        print(log_message)
        self.history.append(log_message)
        if len(self.history) > self.history_limit:
            del self.history[0]
