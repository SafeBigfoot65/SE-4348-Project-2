import threading

_log_file = None
_lock = threading.Lock()
_path = None


def init(path='log.txt'):
    global _log_file, _path
    _path = path
    # open in append mode; do not clear yet
    _log_file = open(_path, 'a')

# Log a message to the output file
def log(msg: str):
    global _log_file
    if _log_file is None:
        init()
    line = str(msg)
    with _lock:
        _log_file.write(line + '\n')
        _log_file.flush()


def clear():
    # Clear the current log file and reopen in append mode (happens at bank opening)
    global _log_file, _path
    with _lock:
        if _log_file is not None:
            _log_file.close()
        # truncate
        _log_file = open(_path, 'w')
        _log_file.close()
        _log_file = open(_path, 'a')

# Close the log file after use
def close():
    global _log_file
    with _lock:
        if _log_file is not None:
            _log_file.close()
            _log_file = None
