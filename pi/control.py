import socket
import threading
from Log import Log  # Assuming Log class has been defined as shown previously

class control(threading.Thread):
    def __init__(self, server_address, server_port, log, drone):
        super().__init__()
        self.server_address = server_address
        self.server_port = server_port
        self.log = log
        self.responses = []
        self.waiting_responses = []
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_address, self.server_port))
        self.running = True
        self.drone = drone
        print("Client coms active")

    def run(self):
        try:
            while self.running:
                data = self.client_socket.recv(1024)
                if data:
                    self.log.write([data.decode('utf-8')])
                    self.process_data(data.decode('utf-8'))
                else:
                    break
        finally:
            self.client_socket.close()

    def process_data(self, data):
        # Example processing function
        print(f"Received data: {data}")
        self.responses.append(data.split())

    def send_data(self, data):
        self.client_socket.sendall(data.encode('utf-8'))

    def close(self):
        self.running = False
        self.client_socket.close()

