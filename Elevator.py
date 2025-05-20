import pygame
import time
from settings import *

class Elevator:
    """Class representing an elevator in a building"""
    
    def __init__(self, image_path, sound_path):
        """Initialize elevator with image and sound"""
        self.current_floor = 0
        self.sound = pygame.mixer.Sound(sound_path)
        self.image = pygame.image.load(image_path)
        self.queue = []
        self.current_y = 0
        self.rect = self.image.get_rect()
        self.is_moving = False
        self.is_waiting = False
        self.target_floor = None
        self.move_start_time = None
        self.wait_start_time = None
        self.move_duration = None
        self.wait_time = ELEVATOR_WAIT_TIME
        self.elevator_id = 0

    def draw(self, num, screen, screen_height, floor_width, elevator_x_offset, elevator_margin):
        """Draw the elevator on the screen"""
        x = floor_width + elevator_x_offset + ((num - 1) * (ELEVATOR_WIDTH + elevator_margin))
        
        if self.is_moving:
            y = int(self.current_y)
        else:
            y = screen_height - FLOOR_HEIGHT - (self.current_floor * TOTAL_FLOOR_HEIGHT)
            self.current_y = y
        
        self.rect = pygame.Rect(x, y, ELEVATOR_WIDTH, ELEVATOR_HEIGHT)
        screen.blit(self.image, (x, y))

    def elevator_move(self, target_floor, screen, screen_height):
        """Handle elevator movement to a specific floor"""
        if self.is_waiting:
            if time.time() - self.wait_start_time >= self.wait_time:
                self.is_waiting = False
                self.is_moving = False
                
                if target_floor in self.queue:
                    self.queue.remove(target_floor)
                return True
            return False

        if not self.is_moving:
            self.is_moving = True
            self.target_floor = target_floor
            self.move_start_time = time.time()
            
            self.move_duration = abs(self.current_floor - self.target_floor) * FLOOR_TRAVEL_TIME
            
            if self.move_duration == 0:
                self.is_moving = False
                self.is_waiting = True
                self.wait_start_time = time.time()
                self._play_arrival_sound()
                return False

        current_time = time.time()
        elapsed_time = current_time - self.move_start_time
        
        progress = min(elapsed_time / self.move_duration, 1) if self.move_duration > 0 else 1

        start_y = screen_height - FLOOR_HEIGHT - (self.current_floor * TOTAL_FLOOR_HEIGHT)
        end_y = screen_height - FLOOR_HEIGHT - (self.target_floor * TOTAL_FLOOR_HEIGHT)
        new_y = start_y + (end_y - start_y) * progress
        
        self.current_y = new_y
        
        if progress >= 1:
            self.current_floor = self.target_floor
            self.is_moving = False
            self.is_waiting = True
            self.wait_start_time = time.time()
            self._play_arrival_sound()
            
            return False

        return False
    
    def _play_arrival_sound(self):
        """Play arrival sound"""
        self.sound.play()
        
    def get_next_destination(self):
        """Return the next destination in queue"""
        if self.queue:
            return self.queue[0]
        return None

    def add_to_queue(self, floor):
        """Add a floor to the elevator queue"""
        if floor not in self.queue:
            self.queue.append(floor)

    def is_idle(self):
        """Check if elevator is idle"""
        return not self.is_moving and not self.is_waiting and not self.queue
        
    def calculate_travel_time(self, target_floor):
        """Calculate estimated travel time to a specific floor"""
        if self.current_floor == target_floor and not self.is_moving:
            return 0
        
        total_time = 0
        current_position = self.current_floor
        
        if self.is_moving:
            elapsed = time.time() - self.move_start_time
            remaining = max(0, self.move_duration - elapsed)
            total_time += remaining
            
            current_position = self.target_floor
            total_time += ELEVATOR_WAIT_TIME
            
        elif self.is_waiting:
            elapsed = time.time() - self.wait_start_time
            remaining = max(0, ELEVATOR_WAIT_TIME - elapsed)
            total_time += remaining
        
        queue = list(self.queue)
        
        if (self.is_moving or self.is_waiting) and self.target_floor in queue:
            queue.remove(self.target_floor)
        
        for floor in queue:
            if floor == target_floor:
                break
                
            travel_time = abs(current_position - floor) * FLOOR_TRAVEL_TIME
            total_time += travel_time
            
            total_time += ELEVATOR_WAIT_TIME
            current_position = floor
        
        if target_floor not in queue:
            travel_time = abs(current_position - target_floor) * FLOOR_TRAVEL_TIME
            total_time += travel_time
        
        return total_time
        
    def calculate_remaining_time(self, target_floor):
        """Calculate remaining time until elevator reaches a floor"""
        if self.current_floor == target_floor and not self.is_moving:
            return 0.0
                
        current_time = time.time()
        total_remaining = 0.0
        
        if self.is_waiting:
            elapsed_wait = current_time - self.wait_start_time
            wait_remaining = max(0.0, ELEVATOR_WAIT_TIME - elapsed_wait)
            total_remaining += wait_remaining
            start_floor = self.current_floor
        
        elif self.is_moving:
            elapsed_move = current_time - self.move_start_time
            move_remaining = max(0.0, self.move_duration - elapsed_move)
            total_remaining += move_remaining
                
            if self.target_floor != target_floor:
                total_remaining += ELEVATOR_WAIT_TIME
            start_floor = self.target_floor
        
        else:
            start_floor = self.current_floor
        
        if target_floor in self.queue:
            queue_pos = self.queue.index(target_floor)
            current_pos = start_floor
                
            for i in range(queue_pos):
                next_floor = self.queue[i]
                    
                if next_floor == start_floor and (self.is_moving or self.is_waiting):
                    continue
                        
                travel_time = abs(current_pos - next_floor) * FLOOR_TRAVEL_TIME
                total_remaining += travel_time
                total_remaining += ELEVATOR_WAIT_TIME
                current_pos = next_floor
                
            if current_pos != target_floor:
                travel_time = abs(current_pos - target_floor) * FLOOR_TRAVEL_TIME
                total_remaining += travel_time
        else:
            if start_floor != target_floor:
                travel_time = abs(start_floor - target_floor) * FLOOR_TRAVEL_TIME
                total_remaining += travel_time
            
        return total_remaining