import datetime
import os


class Logger:
    def __init__(self, log_folder, enable_log_file):
        time = datetime.datetime.now()
        self.file_path = os.path.join(log_folder, f"\\{time.strftime('%Y-%d-%m-%H-%M-%S')}.log")

        self.INFO = "INFO"
        self.WARNING = "WARNING"
        self.ERROR = "ERROR"

        self.enable_log_file = enable_log_file

    def log(self, log_level, message):
        message = f"{datetime.datetime.now().strftime('%Y-%d-%m %H:%M:%S')} | [{log_level}] | {message}"
        print(message)
        if self.enable_log_file:
            log_file = open(self.file_path, 'a')
            log_file.write(f"{message}\n")
            log_file.close()
