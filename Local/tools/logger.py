import re

class Logger(object):
        DEBUG, NOTE, WARNING, ERROR, CRITICAL = list(range(0,5))
        BASECOLOR, BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = list(range(29,38))
        LEVELNAMES = {
            DEBUG   : "DEBUG",
            NOTE    : "NOTE",
            WARNING : "WARNING",
            ERROR   : "ERROR",
            CRITICAL: "CRITICAL",
        }

        COLORS = {
            DEBUG   : CYAN,
            NOTE    : BASECOLOR,
            WARNING : YELLOW,
            ERROR   : RED,
            CRITICAL: RED,
        }

        BLD = '\033[1;%dm'
        STD = '\033[%dm'
        RST = '\033[0m'

        colored = True

        def __init__(self, debug_level, debug_colored):
            self.debugle = debug_level
            self.colored = debug_colored

        def disable_color(self):
            self.colored = False

        def colorize(self, levelno, msg):
            '''Remove extra spaces'''
            msg = self.squeeze(msg)
            color = self.COLORS[levelno]
            levelname = self.LEVELNAMES[levelno]
            if self.colored and color is not None and levelname is not None:
                level = "".join([self.BLD % color, levelname, self.RST])
                msg = "".join([self.STD % color, msg, self.RST])
                return "%s: %s" % (level, msg)

            return msg

        def debug(self, msg):
            if (self.debugle <= self.DEBUG):
                print(self.colorize(self.DEBUG, msg))

        def note(self, msg):
            if (self.debugle <= self.NOTE):
                print(self.colorize(self.NOTE, msg))

        def warn(self, msg):
            if (self.debugle <= self.WARNING):
                print(self.colorize(self.WARNING, msg))

        def error(self, msg):
            print(self.colorize(self.ERROR, msg))

        def critical(self, msg):
            print(self.colorize(self.CRITICAL, msg))

        def squeeze(self, value: str, replace=" ") -> str:
            """Replce multiple space with one"""
            return re.sub(r"[\x00-\x20]+", replace, value).strip()
