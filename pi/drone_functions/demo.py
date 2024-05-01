from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time

class demo:
    def __init__(self, vehicle):
        self.drone = vehicle
        self.set_rtl_mode()
        self.drone.close()

    def calibrate_accelerometer(self):
        print("Calibrating accelerometer. Ensure the drone is stationary.")
        self.drone.send_mavlink(self.drone.message_factory.command_long_encode(
            0, 0,    # target system, target component
            mavutil.mavlink.MAV_CMD_PREFLIGHT_CALIBRATION, # command
            0,       # confirmation
            1, 0, 0, 0, 0, 0, 0  # param 1, 2, 3, 4, 5, 6, 7
        ))

    def arm_and_takeoff(self, aTargetAltitude):
        while not self.drone.is_armable:
            print(" Waiting for vehicle to initialise...")
            time.sleep(1)

        self.drone.mode = VehicleMode("GUIDED")
        self.drone.armed = True

        while not self.drone.armed:
            print(" Waiting for arming...")
            time.sleep(1)

        print("Taking off!")
        self.drone.simple_takeoff(aTargetAltitude)

        while True:
            print(" Altitude: ", self.drone.location.global_relative_frame.alt)
            if self.drone.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
                print("Reached target altitude")
                break
            time.sleep(1)

    def goto_location(self, lat, lon, alt):
        print(f"Going to latitude: {lat}, longitude: {lon}, altitude: {alt}")
        location = LocationGlobalRelative(lat, lon, alt)
        self.drone.simple_goto(location)

    def set_rtl_mode(self):
        print("Setting Return to Launch mode.")
        self.drone.mode = VehicleMode("RTL")

    def go(self, id):
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
            val = "All good"
        except Exception as e:
            val =  f"An error occurred: {str(e)}"
        finally:
            return self.finalize_response(id, val)


    def finalize_response(self, id, val):
        response = ["R", id, val]
        return(response)


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
            return self.finalize_response(id, val)

    def handle_file_upload(self, file_content, id):
        # Save the content to a file
        with open(self.mission_file_path, 'w') as file:
            file.write(file_content)
        self.finalize_response(id, "File Upload Success")

    def run_uploaded_mission(self, id):
        # Check if the mission file exists and is valid
        if os.path.exists(self.mission_file_path):
            with open(self.mission_file_path, 'r') as file:
                commands = file.readlines()

            # Clear existing commands (if any)
            self.drone.commands.clear()
            self.drone.commands.download()
            self.drone.commands.wait_ready()

            # Interpret and execute commands
            for cmd in commands:
                parsed_cmd = cmd.strip().split(',')
                command_type = parsed_cmd[0]

                if command_type == "TAKEOFF":
                    # Example: TAKEOFF,10
                    altitude = float(parsed_cmd[1])
                    self.drone.simple_takeoff(altitude)
                    print(f"Executing TAKEOFF to {altitude} meters")
                elif command_type == "GOTO":
                    # Example: GOTO,34.123,-118.123,20
                    lat = float(parsed_cmd[1])
                    lon = float(parsed_cmd[2])
                    alt = float(parsed_cmd[3])
                    point = LocationGlobalRelative(lat, lon, alt)
                    self.drone.simple_goto(point)
                    print(f"Going to point: {lat}, {lon}, {alt}")
                elif command_type == "LAND":
                    self.drone.mode = VehicleMode("LAND")
                    print("Executing LAND")

                # Additional commands like setting modes, changing parameters, etc., could also be added
                time.sleep(1)  # Small delay to avoid overwhelming the command queue

            # Upload all commands to the vehicle
            self.drone.commands.upload()
            self.finalize_response(id, "Mission Run Success")
        else:
            self.finalize_response(id, "Mission File Not Found")

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
            return self.finalize_response(id, val)

    def kill(self, id):
        # Emergency stop - this method should be used with caution
        try:
            print("Killing motors (Emergency Stop)")
            self.drone.mode = VehicleMode("LAND")  # Land is safer than stopping motors mid-air
            val = "please don't do this man"
        except Exception as e:
            val = f"Kill failed: {str(e)}"
        finally:
            return self.finalize_response(id, val)
    
    def hover(self, id):
        try:
            print("Hovering at current location.")
            # Instruct the drone to hold its current position
            current_location = self.drone.location.global_frame
            self.drone.simple_goto(current_location)
            val = "chillin"
        except Exception as e:
            val = f"Hover failed: {str(e)}"
        finally:
            return self.finalize_response(id, val)

    def disarm(self, id):
        # Disarm the drone, make sure it's landed or not flying
        try:
            print("Disarming")
            if self.drone.mode != 'GUIDED' and self.drone.armed:
                self.drone.disarm()
                val = "heck yeah"
            else:
                val = "Disarm Failed: Not safe to disarm"
        except Exception as e:
            val = f"Disarm failed: {str(e)}"
        finally:
            return self.finalize_response(id, val)

    def go_to(self, id, location_str):
        # Split the location string and go to the specified location
        try:
            lat, lon = map(float, location_str.split(','))
            print(f"Going to latitude: {lat}, longitude: {lon}")
            location = LocationGlobalRelative(lat, lon, self.drone.location.global_relative_frame.alt)
            self.drone.simple_goto(location)
            val = "went"
        except Exception as e:
            val = f"GoTo failed: {str(e)}"
        finally:
            return self.finalize_response(id, val)

    def land_now(self, id):
        try:
            print("Landing Now")
            self.drone.mode = VehicleMode("LAND")
            val = "Land Good"
        except Exception as e:
            val = f"Land now failed: {str(e)}"
        finally:
            return self.finalize_response(id, val)

    def land_home(self, id):
        try:
            print("Returning to Launch")
            self.drone.mode = VehicleMode("RTL")
            val = "Land good"
        except Exception as e:
            val = f"Land home failed: {str(e)}"
        finally:
            return self.finalize_response(id, val)

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
            return self.finalize_response(id, val)
        
