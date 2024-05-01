from dronekit import connect as dronekit_connect, VehicleMode
from pymavlink import mavutil
import time

class Connect:
    def __init__(self, connection_string, baud=57600, wait_ready=True):
        self.connection_string = connection_string
        self.baud = baud
        self.wait_ready = wait_ready
        self.vehicle = None

    def connect_vehicle(self):
        # Establish connection to the vehicle
        self.vehicle = dronekit_connect(self.connection_string, baud=self.baud, wait_ready=self.wait_ready)
        print("Vehicle connected.")

        # Calibrate and set initial mode
        self.calibrate_vehicle()
        self.set_rtl_mode()
        return self.vehicle

    def calibrate_vehicle(self):
        # This method simulates sending a calibration command to the vehicle
        print("Calibrating vehicle. Ensure the vehicle is stationary.")
        self.vehicle.send_mavlink(self.vehicle.message_factory.command_long_encode(
            0, 0,  # target system, target component
            mavutil.mavlink.MAV_CMD_PREFLIGHT_CALIBRATION,  # command
            0,     # confirmation
            1, 0, 0, 0, 0, 0, 0  # parameters 1-7
        ))

    def set_rtl_mode(self):
        # Set vehicle to RTL mode
        self.vehicle.mode = VehicleMode("RTL")
        print("Vehicle set to Return to Launch (RTL) mode.")


