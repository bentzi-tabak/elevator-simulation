import pygame
from settings import *
import time

class Floor:
    """Class representing a floor in a building"""
    
    def __init__(self, image_path, button_image_path, floor_number=None, total_floors=None):
        """Initialize floor with images"""
        self.image = pygame.image.load(image_path)
        self.button_image = pygame.image.load(button_image_path)
        self.timer_font = pygame.font.Font(FONT_FILE, TIMER_FONT_SIZE)
        self.floor_number = floor_number
        self.total_floors = total_floors
        self.has_request = False
        self.assigned_elevator = None
        self.start_time = None
        self.total_time = None
        

    def draw_floor(self, num, screen, screen_height, color):
        """Draw floor on screen"""
        if self.floor_number is None:
            self.floor_number = num
            
        y = screen_height - FLOOR_HEIGHT - num * TOTAL_FLOOR_HEIGHT
        
        screen.blit(self.image, (0, y))
        screen.blit(self.button_image, (BUTTON_X_POSITION, y))
        
        if num < self.total_floors - 1:
            black_space = pygame.Rect(0, screen_height - (TOTAL_FLOOR_HEIGHT * (num + 1)), 
                                    FLOOR_WIDTH, FLOOR_SPACING)
            pygame.draw.rect(screen, BLACK_COLOR, black_space)
        
        if not hasattr(self, 'cached_text') or not hasattr(self, 'cached_color') or self.cached_color != color:
            numbers_font = pygame.font.Font(FONT_FILE, FLOOR_NUMBER_FONT_SIZE)
            self.cached_text = numbers_font.render(f"{num}", True, color)
            self.cached_color = color
        
        text_width = self.cached_text.get_width()
        x_center = 45
        x_position = x_center - (text_width // 2)
        
        screen.blit(self.cached_text, (x_position, screen_height - TIMER_Y_OFFSET - (num * TOTAL_FLOOR_HEIGHT)))
        
    def display_timer(self, screen, screen_height, time_left):
        """Display timer with time left until elevator arrival"""
        x = TIMER_X_POSITION
        y = screen_height - TIMER_Y_OFFSET - (self.floor_number * TOTAL_FLOOR_HEIGHT)
        
        pygame.draw.rect(screen, BACKGROUND_COLOR, (x, y, TIMER_WIDTH, TIMER_HEIGHT))
        
        time_text = f"{time_left:.1f}"
        
        if not hasattr(self, 'cached_timer_text') or not hasattr(self, 'cached_time') or abs(self.cached_time - time_left) >= 0.1:
            self.cached_time = time_left
            self.cached_timer_text = self.timer_font.render(time_text, True, TIMER_COLOR)
        
        screen.blit(self.cached_timer_text, (x + 5, y + 5))
        
    def is_button_clicked(self, mouse_pos, scroll_y, screen_height):
        """Check if the floor button was clicked"""
        if BUTTON_CLICK_MIN_X < mouse_pos[0] < BUTTON_CLICK_MAX_X:
            adjusted_y = mouse_pos[1] + scroll_y
            
            clicked_floor = (screen_height - adjusted_y) // TOTAL_FLOOR_HEIGHT
            
            return clicked_floor == self.floor_number
        
        return False
        
    def set_request(self, elevator, travel_time):
        """Set elevator request for the floor"""
        self.has_request = True
        self.assigned_elevator = elevator
        self.start_time = time.time()
        self.total_time = travel_time
        
    def clear_request(self):
        """Clear elevator request from floor"""
        self.has_request = False
        self.assigned_elevator = None
        self.start_time = None
        self.total_time = None