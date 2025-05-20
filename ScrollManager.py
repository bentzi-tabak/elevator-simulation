# ScrollManager.py
import pygame
from settings import *

def init_scrollbars(screen_width, screen_height, neighborhood, total_width):
    """Initialize scroll data"""
    max_scroll_x = max(0, total_width - (screen_width - SCROLLBAR_WIDTH))
    
    building_scrolls_y = []
    max_scrolls_y = []
    
    for height in neighborhood.building_heights:
        max_scroll_y = max(0, height - (screen_height - SCROLLBAR_WIDTH))
        max_scrolls_y.append(max_scroll_y)
        
        building_scrolls_y.append(max_scroll_y)
    
    neighborhood_scroll_x = 0
    
    return max_scroll_x, building_scrolls_y, max_scrolls_y, neighborhood_scroll_x

def update_scroll_limits(screen_width, screen_height, total_width, neighborhood, building_scrolls_y, max_scrolls_y, neighborhood_scroll_x):
    """Update scroll limits"""
    max_scroll_x = max(0, total_width - (screen_width - SCROLLBAR_WIDTH))
    
    for i, height in enumerate(neighborhood.building_heights):
        max_scrolls_y[i] = max(0, height - (screen_height - SCROLLBAR_WIDTH))
        
        building_scrolls_y[i] = max(0, min(max_scrolls_y[i], building_scrolls_y[i]))
    
    neighborhood_scroll_x = max(0, min(max_scroll_x, neighborhood_scroll_x))
    
    return max_scroll_x, building_scrolls_y, max_scrolls_y, neighborhood_scroll_x

def handle_keyboard_scroll(keys_pressed, focused_building, building_scrolls_y, max_scrolls_y, neighborhood_scroll_x, max_scroll_x):
    """Handle keyboard scrolling"""
    if keys_pressed[pygame.K_UP]:
        building_scrolls_y[focused_building] = max(0, building_scrolls_y[focused_building] - SCROLL_SPEED)
    
    if keys_pressed[pygame.K_DOWN]:
        max_scroll_y = max_scrolls_y[focused_building]
        building_scrolls_y[focused_building] = min(max_scroll_y, building_scrolls_y[focused_building] + SCROLL_SPEED)
    
    if keys_pressed[pygame.K_LEFT]:
        neighborhood_scroll_x = max(0, neighborhood_scroll_x - SCROLL_SPEED)
    
    if keys_pressed[pygame.K_RIGHT]:
        neighborhood_scroll_x = min(max_scroll_x, neighborhood_scroll_x + SCROLL_SPEED)
    
    return building_scrolls_y, neighborhood_scroll_x

def handle_mouse_wheel(event, focused_building, building_scrolls_y, max_scrolls_y):
    """Handle mouse wheel scrolling"""
    if event.button == 4:  # Scroll up
        building_scrolls_y[focused_building] = max(0, building_scrolls_y[focused_building] - SCROLL_SPEED)
    elif event.button == 5:  # Scroll down
        max_scroll_y = max_scrolls_y[focused_building]
        building_scrolls_y[focused_building] = min(max_scroll_y, building_scrolls_y[focused_building] + SCROLL_SPEED)
    
    return building_scrolls_y

def handle_scrollbar_drag(event, screen_width, screen_height, dragging_scrollbar_x, dragging_scrollbar_y,
                         dragging_offset_x, dragging_offset_y, focused_building, total_width, 
                         building_scrolls_y, max_scrolls_y, neighborhood_scroll_x, max_scroll_x, building_heights):
    """Handle scrollbar dragging"""
    mouse_x, mouse_y = event.pos
    
    if dragging_scrollbar_y:
        max_scroll_y = max_scrolls_y[focused_building]
        if max_scroll_y > 0:
            scrollbar_pos = mouse_y - dragging_offset_y
            scrollbar_bottom = screen_height - SCROLLBAR_WIDTH
            scrollbar_height = max(30, (scrollbar_bottom / building_heights[focused_building]) * scrollbar_bottom)
            
            scroll_ratio = max(0, min(1, scrollbar_pos / (scrollbar_bottom - scrollbar_height)))
            
            building_scrolls_y[focused_building] = int(scroll_ratio * max_scroll_y)
    
    elif dragging_scrollbar_x and max_scroll_x > 0:
        scrollbar_pos = mouse_x - dragging_offset_x
        scrollbar_right = screen_width - SCROLLBAR_WIDTH
        scrollbar_width = max(30, (scrollbar_right / total_width) * scrollbar_right)
        
        scroll_ratio = max(0, min(1, scrollbar_pos / (scrollbar_right - scrollbar_width)))
        
        neighborhood_scroll_x = int(scroll_ratio * max_scroll_x)
    
    return building_scrolls_y, neighborhood_scroll_x

def check_scrollbar_click(event, screen_width, screen_height, focused_building, building_display_widths, 
                         neighborhood_scroll_x, building_scrolls_y, max_scrolls_y, max_scroll_x, total_width, building_heights):
    """Check if scrollbar was clicked"""
    dragging_scrollbar_x = False
    dragging_scrollbar_y = False
    dragging_offset_x = 0
    dragging_offset_y = 0
    
    mouse_x, mouse_y = event.pos
    
    building_x = 0
    for i in range(focused_building):
        building_x += building_display_widths[i] + BUILDING_MARGIN
    building_x -= neighborhood_scroll_x
    
    building_width = building_display_widths[focused_building]
    
    if (building_x + building_width - SCROLLBAR_WIDTH <= mouse_x <= building_x + building_width and
        0 <= mouse_y <= screen_height - SCROLLBAR_WIDTH):
        
        dragging_scrollbar_y = True
        max_scroll_y = max_scrolls_y[focused_building]
        
        if max_scroll_y > 0:
            scrollbar_height = max(30, (screen_height / building_heights[focused_building]) * screen_height)
            scrollbar_pos = (building_scrolls_y[focused_building] / max_scroll_y) * (screen_height - scrollbar_height - SCROLLBAR_WIDTH)
            
            dragging_offset_y = mouse_y - scrollbar_pos
        
        return True, dragging_scrollbar_x, dragging_scrollbar_y, dragging_offset_x, dragging_offset_y
    
    elif screen_height - SCROLLBAR_WIDTH <= mouse_y <= screen_height:
        dragging_scrollbar_x = True
        if max_scroll_x > 0:
            scrollbar_right = screen_width - SCROLLBAR_WIDTH
            scrollbar_width = max(30, (scrollbar_right / total_width) * scrollbar_right)
            scrollbar_pos = (neighborhood_scroll_x / max_scroll_x) * (scrollbar_right - scrollbar_width)
            
            dragging_offset_x = mouse_x - scrollbar_pos
        
        return True, dragging_scrollbar_x, dragging_scrollbar_y, dragging_offset_x, dragging_offset_y
    
    return False, dragging_scrollbar_x, dragging_scrollbar_y, dragging_offset_x, dragging_offset_y

def draw_scrollbars(screen, screen_width, screen_height, total_width, neighborhood, building_display_widths,
                   neighborhood_scroll_x, building_scrolls_y, focused_building, max_scrolls_y, max_scroll_x):
    """Draw scrollbars"""
    start_x = -neighborhood_scroll_x
    
    for i, building_height in enumerate(neighborhood.building_heights):
        building_x = start_x
        
        if (building_height > screen_height - SCROLLBAR_WIDTH and 
            building_x < screen_width and building_x + building_display_widths[i] > 0):
            
            scrollbar_x = building_x + building_display_widths[i] - SCROLLBAR_WIDTH
            
            if scrollbar_x >= 0 and scrollbar_x < screen_width:
                pygame.draw.rect(screen, SCROLL_BAR_BG_COLOR, 
                              (scrollbar_x, 0, SCROLLBAR_WIDTH, screen_height - SCROLLBAR_WIDTH))
                
                max_scroll_y = max_scrolls_y[i]
                if max_scroll_y > 0:
                    ratio = (screen_height - SCROLLBAR_WIDTH) / building_height
                    scrollbar_height = max(30, ratio * (screen_height - SCROLLBAR_WIDTH))
                    scrollbar_pos = (building_scrolls_y[i] / max_scroll_y) * ((screen_height - SCROLLBAR_WIDTH) - scrollbar_height)
                    
                    pygame.draw.rect(screen, SCROLL_BAR_COLOR if i == focused_building else SCROLL_BAR_BG_COLOR, 
                                  (scrollbar_x, scrollbar_pos, SCROLLBAR_WIDTH, scrollbar_height))
                
        start_x += building_display_widths[i] + BUILDING_MARGIN
    
    if max_scroll_x > 0:
        pygame.draw.rect(screen, SCROLL_BAR_BG_COLOR, 
                       (0, screen_height - SCROLLBAR_WIDTH, 
                        screen_width, SCROLLBAR_WIDTH))
        
        ratio = screen_width / total_width
        scrollbar_width = max(30, ratio * screen_width)
        scrollbar_pos = (neighborhood_scroll_x / max_scroll_x) * (screen_width - scrollbar_width)
        
        pygame.draw.rect(screen, SCROLL_BAR_COLOR, 
                       (scrollbar_pos, screen_height - SCROLLBAR_WIDTH, 
                        scrollbar_width, SCROLLBAR_WIDTH))