# Elevator Simulation System

## Overview
This project implements a multi-building elevator simulation system in Python using Pygame. The simulation demonstrates efficient elevator routing algorithms and can visualize multiple buildings with customizable numbers of floors and elevators.

## Features
- Multiple building support with configurable number of floors and elevators
- Real-time elevator animation with smooth movement
- Intelligent elevator dispatching algorithm that minimizes wait times
- Visual timer display showing estimated arrival time for each requested floor
- Interactive controls for requesting elevators
- Scrollable interface for navigating large buildings

## Technical Implementation
- **Object-Oriented Design**: Implemented using classes for elevators, floors, buildings, and neighborhoods
- **Factory Design Pattern**: Used for creating building elements
- **Real-time Animation**: Smooth movement of elevators between floors
- **Event-Driven Architecture**: Processes user inputs to control elevator requests
- **Efficient Algorithm**: Selects the optimal elevator for each request based on estimated travel time

## Project Structure
- `main.py` - Entry point for the application
- `settings.py` - Configuration settings for the simulation
- `Elevator.py` - Defines elevator behavior and movement
- `Floor.py` - Implements floor functionality and button requests
- `Building.py` - Manages elevators and floors within a building
- `Neighborhood.py` - Orchestrates multiple buildings
- `factory.py` - Factory design pattern implementation for creating components
- `NeighborhoodManager.py` - Main simulation loop and event handling
- `NeighborhoodRenderer.py` - Rendering functions for the simulation
- `ScrollManager.py` - Handles scrolling behavior for large buildings

## Requirements
- Python 3.x
- Pygame library
- Font file: "RubikDoodleShadow-Regular.ttf"
- Image files:
  - "wall.png" - Floor image
  - "elevator_button (1).png" - Button image
  - "elv (1).png" - Elevator image
- Sound file: "ding.mp3" - Elevator arrival sound

## How to Run
1. Ensure all required files are in the project directory
2. Install required dependencies: `pip install pygame`
3. Run the application: `python main.py`

## Usage
- Click on elevator buttons on any floor to request an elevator
- Press TAB to switch focus between buildings
- Use arrow keys or mouse wheel to scroll through buildings
- Observe the timer display that shows the estimated time until elevator arrival

## Customization
You can customize the simulation by modifying the `DEFAULT_NEIGHBORHOOD_CONFIG` in `settings.py` to change:
- Number of buildings
- Number of floors per building
- Number of elevators per building

## Algorithm Description
The elevator dispatching algorithm selects the elevator with the shortest estimated travel time to the requested floor. It considers:
- Current elevator position
- Direction of travel
- Current queue of floor requests
- Estimated travel and wait times

This approach minimizes passenger wait times while maintaining efficient elevator movement.
