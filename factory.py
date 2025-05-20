from Floor import Floor
from Elevator import Elevator
from settings import *

class BuildingElementFactory:
    """Factory class for creating building elements"""
    @staticmethod
    def create_floors(num_floors, floor_image=None, button_image=None):
        """Create multiple floors at once"""
        floor_img = floor_image or DEFAULT_FLOOR_IMAGE
        button_img = button_image or DEFAULT_BUTTON_IMAGE
        
        floors = []
        for i in range(num_floors):
            floor = Floor(floor_img, button_img, i, num_floors)
            floors.append(floor)
            
        return floors
    
    @staticmethod
    def create_elevators(num_elevators, elevator_image=None, sound_file=None):
        """Create multiple elevators at once"""
        elevator_img = elevator_image or DEFAULT_ELEVATOR_IMAGE
        sound = sound_file or DEFAULT_SOUND_FILE
        
        elevators = []
        for i in range(num_elevators):
            elevator = Elevator(elevator_img, sound)
            elevator.elevator_id = i + 1
            elevators.append(elevator)
            
        return elevators