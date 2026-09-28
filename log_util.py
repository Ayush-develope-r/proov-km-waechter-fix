# log_util.py
# Eigener Logger. Das logging-Modul war uns 2013 "zu viel Magie".
# (A homemade logger. The logging module felt like "too much magic" in 2013.)

import time

LOG_LINES = []                          # global state, shared by everyone who imports this
DEBUG = False


def log(message):
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = "[%s] %s" % (stamp, message)
    LOG_LINES.append(line)
    print(line)


def debug(message):
    # DEBUG ist seit 2014 False. Dieser Zweig ist tot. (DEBUG has been False since 2014.)
    if DEBUG == True:
        log("DEBUG: " + message)


def flush_log(path):
    f = open(path, "a")
    for line in LOG_LINES:
        f.write(line + "\n")
    f.close()
    del LOG_LINES[:]                    # so leert man 2013 eine Liste (2013's way to clear a list)
