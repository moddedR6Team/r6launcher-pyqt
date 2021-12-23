import psutil


def kill_r6():
    for proc in psutil.process_iter():
        try:
            if 'rainbowsix.exe' in proc.name().lower():
                proc.kill()
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def is_siege_running():
    for proc in psutil.process_iter():
        try:
            if 'rainbowsix.exe' in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def siege_running_loop():
    while 1:
        for proc in psutil.process_iter():
            try:
                if 'rainbowsix.exe' not in proc.name().lower():
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass


def pretty_string_size(size):
    if size < 1024:
        return f"{size} B"
    elif size < 1048576:
        return f"{round(size / 1024, 2)} KB"
    elif size < 1073741824:
        return f"{round(size / 1048576, 2)} MB"
    elif size < 1099511627776:
        return f"{round(size / 1073741824, 2)} GB"
    elif size < 1125899906842624:
        return f"{round(size / 1099511627776, 2)} TB"
