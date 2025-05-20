import pygame
from settings import *

def init_neighborhood(neighborhood):
    """Initialize neighborhood display data"""
    building_display_widths = []
    for building_width in neighborhood.building_widths:
        building_display_widths.append(building_width)
    
    total_width = sum(building_display_widths) + (len(building_display_widths) - 1) * BUILDING_MARGIN
    
    return building_display_widths, total_width

def handle_building_click(event, screen_height, neighborhood, building_display_widths, 
                        neighborhood_scroll_x, building_scrolls_y, focused_building):
    """Handle click on a building"""
    mouse_x, mouse_y = event.pos
    new_focused_building = focused_building
    floor_clicked = None
    building_index = None
    
    adjusted_x = mouse_x + neighborhood_scroll_x
    building_start_x = 0
    
    for i, building in enumerate(neighborhood.buildings):
        building_width = building_display_widths[i]
        building_end_x = building_start_x + building_width
        
        if building_start_x <= adjusted_x < building_end_x:
            new_focused_building = i
            
            building_x = adjusted_x - building_start_x
            
            building_height = neighborhood.building_heights[i]
            
            if building_height <= screen_height - SCROLLBAR_WIDTH:
                y_offset = screen_height - building_height - SCROLLBAR_WIDTH
                
                if mouse_y < y_offset or mouse_y >= screen_height - SCROLLBAR_WIDTH:
                    break
                    
                adjusted_y = mouse_y - y_offset
                
                if BUTTON_CLICK_MIN_X <= building_x <= BUTTON_CLICK_MAX_X:
                    floor_y = building_height - adjusted_y
                    floor_index = int(floor_y / TOTAL_FLOOR_HEIGHT)
                    
                    if 0 <= floor_index < len(building.floors):
                        floor_clicked = floor_index
                        building_index = i
            else:
                adjusted_y = mouse_y + building_scrolls_y[i]
                
                if BUTTON_CLICK_MIN_X <= building_x <= BUTTON_CLICK_MAX_X:
                    floor_y = building_height - adjusted_y
                    floor_index = int(floor_y / TOTAL_FLOOR_HEIGHT)
                    
                    if 0 <= floor_index < len(building.floors):
                        floor_clicked = floor_index
                        building_index = i
            
            break
        
        building_start_x += building_width + BUILDING_MARGIN
    
    return new_focused_building, floor_clicked, building_index

def draw_buildings(screen, screen_width, screen_height, neighborhood, building_display_widths,
                 neighborhood_scroll_x, building_scrolls_y, focused_building):
    """Draw all buildings on screen"""
    start_x = -neighborhood_scroll_x
    
    for i, building in enumerate(neighborhood.buildings):
        surface = neighborhood.building_surfaces[i]
        surface.fill(BACKGROUND_COLOR)
        
        building.update_elevators(surface, neighborhood.building_heights[i])
        building.update_floor_timers(surface, neighborhood.building_heights[i])
        
        building.draw_building(surface, neighborhood.building_heights[i])
        
        building_x = start_x
        
        if building_x < screen_width and building_x + building_display_widths[i] > 0:
            building_height = neighborhood.building_heights[i]
            
            if building_height <= screen_height - SCROLLBAR_WIDTH:
                dest_y = screen_height - building_height - SCROLLBAR_WIDTH
                
                screen.blit(surface, (building_x, dest_y))
            else:
                scroll_y = building_scrolls_y[i]
                
                src_rect = pygame.Rect(0, scroll_y, 
                                     building_display_widths[i], 
                                     min(screen_height - SCROLLBAR_WIDTH, building_height - scroll_y))
                
                if building_height - scroll_y < screen_height - SCROLLBAR_WIDTH:
                    remaining_space = (screen_height - SCROLLBAR_WIDTH) - (building_height - scroll_y)
                    dest_y = remaining_space
                else:
                    dest_y = 0
                
                screen.blit(surface, (building_x, dest_y), src_rect)
            
            if i == focused_building:
                if building_height <= screen_height - SCROLLBAR_WIDTH:
                    frame_y = screen_height - building_height - SCROLLBAR_WIDTH
                    frame_height = building_height
                else:
                    frame_y = dest_y
                    frame_height = min(screen_height - frame_y - SCROLLBAR_WIDTH, 
                                     building_height - building_scrolls_y[i])
                
                pygame.draw.rect(screen, FOCUSED_BUILDING_COLOR, 
                               (building_x, frame_y, building_display_widths[i], frame_height), 3)
        
        start_x += building_display_widths[i] + BUILDING_MARGIN