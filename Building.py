import pygame
import time
from settings import *
from factory import BuildingElementFactory

class Building:
    """Class representing a building and managing elevators and floors"""
    
    def __init__(self, num_of_floors, num_of_elevators, floor_image, button_image, elevator_image, sound):
        """Initialize building with elevators and floors"""
        self.num_of_floors = num_of_floors
        self.num_of_elevators = num_of_elevators
        
        self.elevators = BuildingElementFactory.create_elevators(
            num_of_elevators, elevator_image, sound)
            
        self.floors = BuildingElementFactory.create_floors(
            num_of_floors, floor_image, button_image)
            
    def draw_building(self, screen, screen_height):
        """Draw entire building on screen"""
        for i, floor in enumerate(self.floors):
            color = FLOOR_NUMBER_ACTIVE_COLOR if floor.has_request else FLOOR_NUMBER_DEFAULT_COLOR
            floor.draw_floor(i, screen, screen_height, color)
        
        for i, elevator in enumerate(self.elevators):
            elevator.draw(i + 1, screen, screen_height, FLOOR_WIDTH, ELEVATOR_X_OFFSET, ELEVATOR_MARGIN)

    def update_elevators(self, screen, screen_height):
        """Update elevators and handle their movement"""
        significant_movement = False
        
        for elevator in self.elevators:
            if elevator.is_moving or elevator.is_waiting:
                target_floor = elevator.get_next_destination()
                if target_floor is not None:
                    elevator_completed = elevator.elevator_move(target_floor, screen, screen_height)
                    
                    if elevator_completed and target_floor in elevator.queue:
                        elevator.queue.remove(target_floor)
                        significant_movement = True
            
            elif elevator.queue:
                next_floor = elevator.get_next_destination()
                elevator.elevator_move(next_floor, screen, screen_height)
                significant_movement = True
        
        return significant_movement

    def is_elevator_at_floor(self, floor):
        """Check if there is an elevator at a specific floor"""
        for elevator in self.elevators:
            if elevator.current_floor == floor and not elevator.is_moving:
                return True
        return False

    def request_elevator(self, floor, screen, screen_height):
        """Handle elevator request for specific floor"""
        if self.is_elevator_at_floor(floor) or self.floors[floor].has_request:
            return
        
        closest_elevator = self._find_closest_elevator(floor)
        
        if closest_elevator:
            closest_elevator.add_to_queue(floor)
            
            travel_time = closest_elevator.calculate_travel_time(floor)
            
            self.floors[floor].set_request(closest_elevator, travel_time)
            
            self.floors[floor].draw_floor(floor, screen, screen_height, FLOOR_NUMBER_ACTIVE_COLOR)
            
            self.floors[floor].display_timer(screen, screen_height, travel_time)

    def _find_closest_elevator(self, floor):
        """Find closest elevator (by time) to a specific floor"""
        closest_elevator = None
        min_time = float('inf')
        
        for elevator in self.elevators:
            travel_time = elevator.calculate_travel_time(floor)
            if travel_time < min_time:
                min_time = travel_time
                closest_elevator = elevator
        
        return closest_elevator

    def update_floor_timers(self, screen, screen_height):
        """Update timers on each floor"""
        for i, floor in enumerate(self.floors):
            if floor.has_request and floor.assigned_elevator:
                elevator = floor.assigned_elevator
                if elevator.current_floor == i and (elevator.is_waiting or not elevator.is_moving):
                    floor.display_timer(screen, screen_height, 0.0)
                    
                    floor.clear_request()
                    
                    floor.draw_floor(i, screen, screen_height, FLOOR_NUMBER_DEFAULT_COLOR)
                else:
                    remaining = elevator.calculate_remaining_time(i)
                    
                    floor.display_timer(screen, screen_height, remaining)