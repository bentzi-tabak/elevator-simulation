import pygame
from Building import Building
from settings import *

class Neighborhood:
    """Class representing a neighborhood with multiple buildings"""
    
    def __init__(self, buildings_config):
        """Initialize neighborhood with multiple buildings"""
        self.buildings = []
        self.building_surfaces = []
        self.building_heights = []
        self.building_widths = []
        self.building_config = buildings_config
        
        for config in buildings_config:
            num_floors = config.get('floors', DEFAULT_NUM_OF_FLOORS)
            num_elevators = config.get('elevators', DEFAULT_NUM_OF_ELEVATORS)
            
            building_height = (num_floors * TOTAL_FLOOR_HEIGHT) - FLOOR_SPACING
            
            building_width = FLOOR_WIDTH + TIMER_WIDTH + ELEVATOR_X_OFFSET + \
                           (num_elevators * ELEVATOR_WIDTH) + \
                           ((num_elevators - 1) * ELEVATOR_MARGIN)
            
            building = Building(num_floors, num_elevators, 
                             DEFAULT_FLOOR_IMAGE, DEFAULT_BUTTON_IMAGE,
                             DEFAULT_ELEVATOR_IMAGE, DEFAULT_SOUND_FILE)
            
            building_surface = pygame.Surface((building_width, building_height))
            
            self.buildings.append(building)
            self.building_surfaces.append(building_surface)
            self.building_heights.append(building_height)
            self.building_widths.append(building_width)
    
    def get_total_width(self):
        """Returns total width of all buildings + margins"""
        total_width = 0
        for width in self.building_widths:
            total_width += width + BUILDING_MARGIN
        
        if self.buildings:
            total_width -= BUILDING_MARGIN
            
        return total_width
    
    def get_max_height(self):
        """Returns the height of the tallest building"""
        if not self.building_heights:
            return 0
        return max(self.building_heights)