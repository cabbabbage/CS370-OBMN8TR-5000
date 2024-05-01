import socket
import threading
from drone_functions.demo import demo
from drone_functions.connect import Connect
import time

class Control(threading.Thread):
    def __init__(self, server_address, server_port, log, drone_connection_string):
        super().__init__()
        self.target_alt = 10
        self.server_address = server_address
        self.server_port = server_port
        self.log = log
        self.responses = []
        self.waiting_responses = []
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_address, self.server_port))
        self.running = True
        connector = Connect(drone_connection_string)
        self.connection = connector.connect_vehicle()
        self.drone = demo(self.connection)
        self.current_thread = None
        self.paused_thread = None
        self.list_of_commands = ["RE", "FU", "RU", "CSU", "TO", "AR", "DA", "GT", "SA", "LN", "LH", "HV"]
        print("Client coms active")

    def run(self):
        try:
            while self.running:
                data = self.client_socket.recv(1024).decode('utf-8')
                if data:
                    self.process_data(data)
                else:
                    # Handle possible disconnection or error
                    print("No data received. Checking connection...")
                    time.sleep(1)
        finally:
            self.close()

    def process_data(self, data):
        print(f"Received data: {data}")
        parts = data.split('%')
        command = parts[0]
        id = parts[1]
        args = parts[2:] if len(parts) > 2 else []

        if command in ["HV", "SA", "FU"] and self.current_thread and self.current_thread.is_alive():

            print("Pausing current process for", command)
            self.paused_thread = self.current_thread

        command_method = self.get_command_method(command, id, args)
        if command_method:
            self.current_thread = threading.Thread(target=command_method)
            self.current_thread.start()

    def get_command_method(self, command, id, args):
        command_methods = {
            "FU": lambda: self.drone.handle_file_upload(args[0], id),
            "RU": lambda: self.drone.run_uploaded_mission(id),
            "CSU": lambda: self.drone.handle_demo(id),
            "TO": lambda: self.drone.takeoff(id) if not self.drone.armed else None,
            "AR": lambda: self.drone.arm(id) if not self.drone.location.global_relative_frame.alt > 0 else None,
            "DA": lambda: self.drone.disarm(id) if self.drone.location.global_relative_frame.alt == 0 else None,
            "GT": lambda: self.drone.go_to(id, args[0]) if self.drone.location.global_relative_frame.alt > 0 else None,
            "SA": lambda: self.drone.set_alt(id, args[0]) if self.drone.location.global_relative_frame.alt > 0 else None,
            "LN": lambda: self.drone.land_now(id) if self.drone.location.global_relative_frame.alt > 0 else None,
            "LH": lambda: self.drone.land_home(id) if self.drone.location.global_relative_frame.alt > 0 else None,
            "HV": lambda: self.drone.hover(id) if self.drone.location.global_relative_frame.alt > 0 else None
        }
        return command_methods.get(command)

    def handle_command(self, command_function):
        response = command_function() 
        if response:
            self.transmit(response)  
        if self.pause_command:
            self.resume()

    def transmit(self, content):
        to_send = "%".join(content)
        try:
            self.client_socket.sendall(to_send.encode('utf-8'))
            self.log.write(content + ["Transmitted"])
        except IOError as e:
            print(e)
            self.log.write(content + ["Transmitted", str(e)])

    def resume(self):
        if self.paused_thread:
            print("Resuming paused process.")
            self.paused_thread.start()
            self.paused_thread = None

    def close(self):
        print("Closing socket and stopping thread.")
        self.running = False
        if self.current_thread and self.current_thread.is_alive():
            self.current_thread.join()
        self.client_socket.close()








