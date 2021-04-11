TO_FILE = False  # Whether log to file. Setup str path (or pathlib.Path) of file
#   with .log suffix (create if not exist). Print to console then doesn't work
AROUND = "auto"  # Separate logs with ===== and line breaks for better visibility.
#   If 'auto', then if TO_FILE = True, then AROUND = False, if TO_FILE = False, AROUND = True.
COLOR = "auto"  # Whether colorize results - mostly python syntax in tracebacks. If _TO_FILE is configured, colorize is ignored.


# Do not edit, internal variables
__DEBUG = 1
