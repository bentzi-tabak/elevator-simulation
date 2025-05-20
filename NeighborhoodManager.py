import pygame
from Neighborhood import Neighborhood
from ScrollManager import *
from NeighborhoodRenderer import *
from settings import *

def main_loop():
    """Main game loop for elevator neighborhood"""
    # Initialize pygame
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.set_num_channels(64)
    
    # Get available screen resolution
    info = pygame.display.Info()
    screen_width = info.current_w - 80
    screen_height = info.current_h - 100
    
    # Create game window
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Building Neighborhood Simulation")
    
    # Create neighborhood with default settings
    neighborhood = Neighborhood(DEFAULT_NEIGHBORHOOD_CONFIG)
    
    # Initialize display data
    building_display_widths, total_width = init_neighborhood(neighborhood)
    
    # Initialize scroll data
    max_scroll_x, building_scrolls_y, max_scrolls_y, neighborhood_scroll_x = init_scrollbars(
        screen_width, screen_height, neighborhood, total_width)
    
    # Set focused building
    focused_building = 0
    
    # Variables for key handling
    keys_pressed = {
        pygame.K_UP: False,
        pygame.K_DOWN: False,
        pygame.K_LEFT: False,
        pygame.K_RIGHT: False
    }
    
    # Variables for scrollbar dragging
    dragging_scrollbar_x = False
    dragging_scrollbar_y = False
    dragging_offset_x = 0
    dragging_offset_y = 0
    
    # Initialize game loop variables
    run = True
    clock = pygame.time.Clock()
    
    # Main game loop
    while run:
        # Limit frame rate
        delta_time = clock.tick(FPS)
        
        # Update scroll limits
        max_scroll_x, building_scrolls_y, max_scrolls_y, neighborhood_scroll_x = update_scroll_limits(
            screen_width, screen_height, total_width, neighborhood, building_scrolls_y, max_scrolls_y, neighborhood_scroll_x)
        
        # Event handling
        for event in pygame.event.get():
            # Exit game
            if event.type == pygame.QUIT:
                run = False
                
            # Handle key presses
            elif event.type == pygame.KEYDOWN:
                if event.key in keys_pressed:
                    keys_pressed[event.key] = True
                elif event.key == pygame.K_TAB:
                    focused_building = (focused_building + 1) % len(neighborhood.buildings)
                    
            # Handle key releases
            elif event.type == pygame.KEYUP:
                if event.key in keys_pressed:
                    keys_pressed[event.key] = False
            
            # Handle mouse button press
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Check if clicked on scrollbars
                    is_scrollbar, dragging_scrollbar_x, dragging_scrollbar_y, dragging_offset_x, dragging_offset_y = check_scrollbar_click(
                        event, screen_width, screen_height, focused_building, building_display_widths, 
                        neighborhood_scroll_x, building_scrolls_y, max_scrolls_y, max_scroll_x, 
                        total_width, neighborhood.building_heights)
                    
                    # If not clicked on scrollbar, check if clicked on building
                    if not is_scrollbar:
                        new_focused, floor_clicked, building_index = handle_building_click(
                            event, screen_height, neighborhood, building_display_widths, 
                            neighborhood_scroll_x, building_scrolls_y, focused_building)
                        
                        # Update focused building
                        focused_building = new_focused
                        
                        # If clicked on elevator button in a floor
                        if floor_clicked is not None and building_index is not None:
                            building = neighborhood.buildings[building_index]
                            building_surface = neighborhood.building_surfaces[building_index]
                            building_height = neighborhood.building_heights[building_index]
                            
                            # Request elevator for clicked floor
                            building.request_elevator(floor_clicked, building_surface, building_height)
                
                # Handle mouse wheel scroll
                elif event.button in (4, 5):  # Scroll up or down
                    building_scrolls_y = handle_mouse_wheel(
                        event, focused_building, building_scrolls_y, max_scrolls_y)
            
            # Mouse button release
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left button release
                    # Cancel scrollbar dragging
                    dragging_scrollbar_x = False
                    dragging_scrollbar_y = False
            
            # Mouse drag
            elif event.type == pygame.MOUSEMOTION and event.buttons[0]:  # Drag with left button
                if dragging_scrollbar_x or dragging_scrollbar_y:
                    # Update scroll position based on drag
                    building_scrolls_y, neighborhood_scroll_x = handle_scrollbar_drag(
                        event, screen_width, screen_height, dragging_scrollbar_x, dragging_scrollbar_y,
                        dragging_offset_x, dragging_offset_y, focused_building, total_width, 
                        building_scrolls_y, max_scrolls_y, neighborhood_scroll_x, max_scroll_x, 
                        neighborhood.building_heights)
        
        # Handle keyboard scrolling
        building_scrolls_y, neighborhood_scroll_x = handle_keyboard_scroll(
            keys_pressed, focused_building, building_scrolls_y, max_scrolls_y, 
            neighborhood_scroll_x, max_scroll_x)
        
        # Clear main screen
        screen.fill(BACKGROUND_COLOR)
        
        # Draw buildings
        draw_buildings(
            screen, screen_width, screen_height, neighborhood, building_display_widths,
            neighborhood_scroll_x, building_scrolls_y, focused_building)
        
        # Draw scrollbars
        draw_scrollbars(
            screen, screen_width, screen_height, total_width, neighborhood, building_display_widths,
            neighborhood_scroll_x, building_scrolls_y, focused_building, max_scrolls_y, max_scroll_x)
        
        # Update display
        pygame.display.flip()
    
    # Close pygame at end
    pygame.quit()

# Run main loop when file is run directly
if __name__ == "__main__":
    main_loop()