import gc
import logging
import time


class Hello:
    def __init__(
        self,
        board_id,
        boot_time,
        helpers,
        micropython_version,
        name,
    ):
        self.board_id = board_id
        self.boot_time = boot_time
        self.micropython_version = micropython_version
        self.name = name
        helpers["logger"].info("Hello started successfully")
        helpers["gc"]() # pretend that we're preparing for an operation that requires lots of memory


    def uptime_string_calculate(
        self,
        current_time=None,
    ):
        def plural_simple_maybe(
            unit,
            string,
        ):
            if unit == 1:
                return f"{unit} {string}"
            else:
                return f"{unit} {string}s"


        def string_generate(
            major,
            major_name,
            minor_per_major,
            minor,
            minor_name,
        ):
            minor = minor - (major * minor_per_major)
            major_unit_string = plural_simple_maybe(major, major_name)
            if minor:
                return major_unit_string + ", " + plural_simple_maybe(minor, minor_name)
            else:
                return major_unit_string


        if current_time == None:
            current_time = time.time()
        seconds = current_time - self.boot_time
        minutes = seconds // 60
        hours = minutes // 60
        days = hours // 24
        if days:
            return string_generate(days, "day", 24, hours, "hour")
        if hours:
           return string_generate(hours, "hour", 60, minutes, "minute")
        if minutes:
            return string_generate(minutes, "minute", 60, seconds, "second")
        if seconds:
            return plural_simple_maybe(seconds, "second")
        return "0 seconds"
