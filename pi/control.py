import socket
import threading
from Log import Log  # Assuming Log class has been defined as shown previously
from drone_functions.demo import demo
from drone_functions.connect import Connect
from dronekit import VehicleMode, LocationGlobalRelative
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
        self.drone = connector.connect_vehicle()
        self.current_thread = None
        print("Client coms active")

    def transmit(self, content):
        to_send = "%".join(content)
        try:
            self.client_socket.sendall(to_send.encode('utf-8'))
            if content[2] is None:
                self.waiting_responses.append(content)
            logContent = content + ["Transmitted"]
            self.log.write(logContent)
        except IOError as e:
            print(e)
            logContent = content + ["Transmitted", str(e)]
            self.log.write(logContent)

    def process_data(self, data):
        print(f"Received data: {data}")
        parts = data.split('%')
        command = parts[0]

        # Handle resuming from a paused state
        if command == "RE" and self.paused_thread:
            print("Resuming paused process.")
            self.current_thread = self.paused_thread
            self.paused_thread = None
            self.pause_command = None
            self.current_thread.start()
            return

        # Check and handle the command for pausing
        if self.current_thread and self.current_thread.is_alive():
            if command in ["HV", "SA"]:  # Only pause for these commands
                print("Pausing current process.")
                self.pause_command = command
                self.paused_thread = self.current_thread
            else:
                self.current_thread.join()

        # Conditional execution based on vehicle state
        if command == "CSU":
            self.current_thread = threading.Thread(target=lambda: self.handle_demo(parts[1]))
        elif command == "TO" and not self.drone.armed:
            self.current_thread = threading.Thread(target=lambda: self.takeoff(parts[1]))
        elif command == "AR" and not self.drone.location.global_relative_frame.alt > 0:
            self.current_thread = threading.Thread(target=lambda: self.arm(parts[1]))
        elif command == "DA" and self.drone.location.global_relative_frame.alt == 0:
            self.current_thread = threading.Thread(target=lambda: self.disarm(parts[1]))
        elif command == "GT" and self.drone.location.global_relative_frame.alt > 0:
            self.current_thread = threading.Thread(target=lambda: self.go_to(parts[1], parts[2]))
        elif command == "SA" and self.drone.location.global_relative_frame.alt > 0:
            self.current_thread = threading.Thread(target=lambda: self.set_alt(parts[1], parts[2]))
        elif command in ["LN", "LH"] and self.drone.location.global_relative_frame.alt > 0:
            if command == "LN":
                self.current_thread = threading.Thread(target=lambda: self.land_now(parts[1]))
            elif command == "LH":
                self.current_thread = threading.Thread(target=lambda: self.land_home(parts[1]))
        elif command == "HV" and self.drone.location.global_relative_frame.alt > 0:
            self.current_thread = threading.Thread(target=lambda: self.hover(parts[1]))

    def handle_demo(self, id):
        func = demo(self.drone)
        val = func.go()
        self.finalize_response(id, val)

    def arm(self, id):
        try:
            print("Arming motors")
            # Vehicle should not be armed until it is armable
            while not self.drone.is_armable:
                print(" Waiting for vehicle to become armable...")
                time.sleep(1)

            self.drone.mode = VehicleMode("GUIDED")  # Set the drone to GUIDED mode
            self.drone.armed = True

            while not self.drone.armed:
                print(" Waiting for arming...")
                time.sleep(1)

            val = "heck yeah"
        except Exception as e:
            val = f"Arming failed: {str(e)}"
        finally:
            self.finalize_response(id, val)

    def takeoff(self, id, target_altitude= 10):
        target_altitude = self.target_alt
        # Ensure the vehicle is armed before attempting to take off
        if not self.drone.armed:
            self.arm()

        try:
            print("Taking off!")
            self.drone.simple_takeoff(target_altitude)  # Take off to target altitude

            # Wait until the vehicle reaches a safe height before returning the function
            while True:
                print(f" Altitude: {self.drone.location.global_relative_frame.alt:.2f}")
                # Check if the drone is at least 95% of the target altitude
                if self.drone.location.global_relative_frame.alt >= target_altitude * 0.95:
                    print("Reached target altitude")
                    val = "blasting"
                    break
                time.sleep(1)
        except Exception as e:
            val = f"Takeoff failed: {str(e)}"
        finally:
            self.finalize_response(id, val)

    def kill(self, id):
        # Emergency stop - this method should be used with caution
        try:
            print("Killing motors (Emergency Stop)")
            self.drone.mode = VehicleMode("LAND")  # Land is safer than stopping motors mid-air
            val = "Kill Success"
        except Exception as e:
            val = f"Kill failed: {str(e)}"
        finally:
            self.finalize_response(id, val)
    
    def hover(self, id):
        try:
            print("Hovering at current location.")
            # Instruct the drone to hold its current position
            current_location = self.drone.location.global_frame
            self.drone.simple_goto(current_location)
            val = "Hover Success"
        except Exception as e:
            val = f"Hover failed: {str(e)}"
        finally:
            self.finalize_response(id, val)

    def disarm(self, id):
        # Disarm the drone, make sure it's landed or not flying
        try:
            print("Disarming")
            if self.drone.mode != 'GUIDED' and self.drone.armed:
                self.drone.disarm()
                val = "Disarm Success"
            else:
                val = "Disarm Failed: Not safe to disarm"
        except Exception as e:
            val = f"Disarm failed: {str(e)}"
        finally:
            self.finalize_response(id, val)

    def go_to(self, id, location_str):
        # Split the location string and go to the specified location
        try:
            lat, lon = map(float, location_str.split(','))
            print(f"Going to latitude: {lat}, longitude: {lon}")
            location = LocationGlobalRelative(lat, lon, self.drone.location.global_relative_frame.alt)
            self.drone.simple_goto(location)
            val = "GoTo Success"
        except Exception as e:
            val = f"GoTo failed: {str(e)}"
        finally:
            self.finalize_response(id, val)

    def land_now(self, id):
        # Command the drone to land at the current location
        try:
            print("Landing Now")
            self.drone.mode = VehicleMode("LAND")
            val = "Land Now Success"
        except Exception as e:
            val = f"Land now failed: {str(e)}"
        finally:
            self.finalize_response(id, val)

    def land_home(self, id):
        # Command the drone to return to the launch (home) location and land
        try:
            print("Returning to Launch")
            self.drone.mode = VehicleMode("RTL")
            val = "Land Home Success"
        except Exception as e:
            val = f"Land home failed: {str(e)}"
        finally:
            self.finalize_response(id, val)

    def set_alt(self, id, altitude):
        try:
            current_location = self.drone.location.global_relative_frame
            target_location = LocationGlobalRelative(current_location.lat, current_location.lon, float(altitude))
            print(f"Setting altitude to {altitude} meters")
            self.drone.simple_goto(target_location)
            val = "Set Altitude Success"
        except Exception as e:
            val = f"Set altitude failed: {str(e)}"
        finally:
            self.finalize_response(id, val)


    def finalize_response(self, id, val):
        response = ["R", id, val]
        self.transmit(response)


    def close(self):
        self.running = False
        if self.current_thread and self.current_thread.is_alive():
            self.current_thread.join()
        self.client_socket.close()

# Usage would remain the same as previously described
