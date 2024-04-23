import os
import datetime

class Log:
    def __init__(self):
        directory = "logs"
        if not os.path.exists(directory):
            os.makedirs(directory)
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"Client_log_{current_time}.csv"
        self.log_file_path = os.path.join(directory, file_name)
        self.file = open(self.log_file_path, 'w')

    def write(self, row_data):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.file.write(f"{timestamp}, {' '.join(row_data)}\n")
        self.file.flush()

    def close(self):
        self.file.close()
