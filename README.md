# 4G LTE Connected Multirotor Raspberry Pi Project

## Table of Contents
- [Project Overview](#project-overview)
- [Project Objectives](#project-objectives)
- [Scrum Plan](#scrum-plan)
  - [Epic 1: Connectivity Setup](#epic-1-connectivity-setup)
  - [Epic 2: User Interface for Control](#epic-2-user-interface-for-control)
  - [Epic 3: Raspberry Pi Command Processing](#epic-3-raspberry-pi-command-processing)
  - [Epic 4: Data Acquisition and Transmission](#epic-4-data-acquisition-and-transmission)
  - [Epic 5: UI Enhancements for Data Display](#epic-5-ui-enhancements-for-data-display)
  - [Epic 6: Multi-threading for Optimized Data Handling](#epic-6-multi-threading-for-optimized-data-handling)
- [Com Stack and Basic Assembly Diagram](#com-stack-and-basic-assembly-diagram)
- [Main Materials](#main-materials)

## Project Overview
This project aims to create a sophisticated control system for a small multirotor using 4G LTE connectivity, leveraging a Raspberry Pi as the command-and-control center. It enables the quadcopter to be operated remotely, supporting both manual and autonomous flight modes, and includes real-time video and data transmission back to the user.

## Project Objectives
- Develop a secure and reliable SSH-based communication link.
- Implement a user-friendly interface for real-time control and navigation.
- Enable effective command relay to the quadcopter's flight controller.
- Stream live video and telemetry data enhancing operational awareness.
- Utilize multi-threading for optimized data and command stream handling.

## Scrum Plan
### Epic 1: Connectivity Setup
- Develop a Pi-side startup script for SSH connection via reverse tunneling.
- Implement user-side procedure for establishing an SSH shell.
- Secure the connection with SSH key exchange.

### Epic 2: User Interface for Control
- Design and integrate a basic, intuitive UI for command input.
- Include manual and autonomous mode control options within the UI.

### Epic 3: Raspberry Pi Command Processing
- Create a drone-side command shell for direct UI interaction.
- Interpret UI commands into MAVLink messages for the flight controller.

### Epic 4: Data Acquisition and Transmission
- Implement video streaming and flight data transmission back to the user.
- Provide command confirmation feedback.

### Epic 5: UI Enhancements for Data Display
- Upgrade UI to include a section for real-time video streaming.
- Display flight data in a user-friendly manner.

### Epic 6: Multi-threading for Optimized Data Handling
- Implement multi-threading for handling video, data streams, and command inputs.
- Integrate efficient encoding techniques for video streaming.

## Com Stack and Basic Assembly Diagram
- Omni GPS antenna
- Flight Controller
- LTE Shield
- Raspberry Pi

## Main Materials
- 4g/LTE cellular HAT
- Raspberry Pi 3 A+
- Flight controller (purchased)
