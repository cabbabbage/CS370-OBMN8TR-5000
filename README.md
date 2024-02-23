# 4G LTE Connected Multirotor Raspberry Pi Project

## Table of Contents
- [Project Overview](#project-overview)
-  [Progress](#progress)
-  [Team](#team).
- [Scrum Plan](#scrum-plan)
  - [Epic 1: Connectivity Setup](#epic-1-connectivity-setup)
  - [Epic 2: User Interface for Control](#epic-2-user-interface-for-control)
  - [Epic 3: Raspberry Pi Command Processing](#epic-3-raspberry-pi-command-processing)
  - [Epic 4: Data Acquisition and Transmission](#epic-4-data-acquisition-and-transmission)
  - [Epic 5: UI Enhancements for Data Display](#epic-5-ui-enhancements-for-data-display)
  - [Epic 6: Multi-threading for Optimized Data Handling](#epic-6-multi-threading-for-optimized-data-handling)

## Project Overview
This project aims to create a sophisticated control system for a small multirotor using 4G LTE connectivity, leveraging a Raspberry Pi as the command-and-control center. It enables the quadcopter to be operated remotely, supporting both manual and autonomous flight modes, and includes real-time video and data transmission back to the user.

## Progress
The Progress section is designed to provide a comprehensive overview of the status of tasks across all epics. It helps team members and stakeholders quickly understand which tasks are underway, who is responsible for them, and the progress towards completion.

| Task Number | Epic Number | In Progress | Assignee | Date Started | Date Complete | Reviewer |
|-------------|-------------|-------------|----------|--------------|---------------|----------|
| [1.1](#task-11-establish-ssh-connection)         | 1           | [ ]         |          |              |               |          |
*Note: Click on the task number to navigate to the detailed task description.*

 
## Team

### Calvin
- **GitHub Username:** cabbabbage
- **EID:** rollo
- **Phone Number:** 970-666-1069
- **Email:** rollo@colostate.edu

### Team Member 2
- **GitHub Username:** 
- **EID:** 
- **Phone Number:** 
- **Email:** 

### Team Member 3
- **GitHub Username:** 
- **EID:** 
- **Phone Number:** 
- **Email:** 





## Scrum Plan
To add a task, include a number, a description, priority level (High, Medium, Low), and creator. Link the task number to the corresponding entry in the Progress section and fill out the table.
### Epic 1: Connectivity Setup
#### Story Points:
- Develop a Pi-side startup script for SSH connection via reverse tunneling.
- Implement user-side procedure for establishing an SSH shell.
- Secure the connection with SSH key exchange.
#### Tasks
##### Task 1.1: Establish SSH Connection
- **Number:** [1.1](#progress)
- **Description:** Develop a startup script for establishing an SSH connection via reverse tunneling.
- **Priority Level:** High
- **Creator:** rollo



##### Task Example
- **Number:** [(add task #)](#progress)
- **Description:** (add description)
- **Priority Level:** (add priority level)
- **Creator:** (add creator eId)

##### Task Example
- **Number:** [(add task #)](#progress)
- **Description:** (add description)
- **Priority Level:** (add priority level)
- **Creator:** (add creator eId)

### Epic 2: User Interface for Control
#### Story Points:
- Design and integrate a basic, intuitive UI for command input.
- Include manual and autonomous mode control options within the UI.

### Epic 3: Raspberry Pi Command Processing
#### Story Points:
- Create a drone-side command shell for direct UI interaction.
- Interpret UI commands into MAVLink messages for the flight controller.

### Epic 4: Data Acquisition and Transmission
#### Story Points:
- Implement video streaming and flight data transmission back to the user.
- Provide command confirmation feedback.

### Epic 5: UI Enhancements for Data Display
#### Story Points:
- Upgrade UI to include a section for real-time video streaming.
- Display flight data in a user-friendly manner.

### Epic 6: Multi-threading for Optimized Data Handling
#### Story Points:
- Implement multi-threading for handling video, data streams, and command inputs.
- Integrate efficient encoding techniques for video streaming.






  
## Main Materials
- 4g/LTE cellular HAT
- Raspberry Pi 3 A+
- Flight controller (purchased)
