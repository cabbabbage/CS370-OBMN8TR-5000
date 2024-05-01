from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time

class demo:
    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.set_rtl_mode()
        self.vehicle.close()

    def calibrate_accelerometer(self):
        print("Calibrating accelerometer. Ensure the drone is stationary.")
        self.vehicle.send_mavlink(self.vehicle.message_factory.command_long_encode(
            0, 0,    # target system, target component
            mavutil.mavlink.MAV_CMD_PREFLIGHT_CALIBRATION, # command
            0,       # confirmation
            1, 0, 0, 0, 0, 0, 0  # param 1, 2, 3, 4, 5, 6, 7
        ))

    def arm_and_takeoff(self, aTargetAltitude):
        while not self.vehicle.is_armable:
            print(" Waiting for vehicle to initialise...")
            time.sleep(1)

        self.vehicle.mode = VehicleMode("GUIDED")
        self.vehicle.armed = True

        while not self.vehicle.armed:
            print(" Waiting for arming...")
            time.sleep(1)

        print("Taking off!")
        self.vehicle.simple_takeoff(aTargetAltitude)

        while True:
            print(" Altitude: ", self.vehicle.location.global_relative_frame.alt)
            if self.vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
                print("Reached target altitude")
                break
            time.sleep(1)

    def goto_location(self, lat, lon, alt):
        print(f"Going to latitude: {lat}, longitude: {lon}, altitude: {alt}")
        location = LocationGlobalRelative(lat, lon, alt)
        self.vehicle.simple_goto(location)

    def set_rtl_mode(self):
        print("Setting Return to Launch mode.")
        self.vehicle.mode = VehicleMode("RTL")

def go(self):
    try:
        self.calibrate_accelerometer()
        self.arm_and_takeoff(10)  # Target altitude of 10 meters
        self.goto_location(latitude_A, longitude_A, 10)  # Point A
        time.sleep(30)
        self.goto_location(latitude_B, longitude_B, 10)  # Point B
        time.sleep(30)
        self.goto_location(latitude_C, longitude_C, 10)  # Point C
        time.sleep(30)
        self.set_rtl_mode()
        return "All good"
    except Exception as e:
        return f"An error occurred: {str(e)}"

        

# Usage
# vehicle = connect('your_connection_string', wait_ready=True)
# drone_controller = DroneController(vehicle)
