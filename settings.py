# Global settings for the elevator simulation

# General settings
BACKGROUND_COLOR = (250, 250, 250)
FPS = 60

# Display settings
SCREEN_HEIGHT = 1000
SCROLL_SPEED = 30

# Image dimensions
FLOOR_WIDTH = 129
FLOOR_HEIGHT = 64
ELEVATOR_WIDTH = 64
ELEVATOR_HEIGHT = 64
BUTTON_WIDTH = 34
BUTTON_HEIGHT = 34

# Spacing and positions
FLOOR_SPACING = 7
TOTAL_FLOOR_HEIGHT = FLOOR_HEIGHT + FLOOR_SPACING
BUTTON_X_POSITION = 80
BUTTON_CLICK_MIN_X = 94
BUTTON_CLICK_MAX_X = 128
ELEVATOR_MARGIN = 10
ELEVATOR_X_OFFSET = 90

# Timer position
TIMER_X_POSITION = 130
TIMER_WIDTH = 50
TIMER_HEIGHT = 40
TIMER_Y_OFFSET = 55
TIMER_FONT_SIZE = 20

# Fonts
FLOOR_NUMBER_FONT_SIZE = 36
FONT_FILE = 'RubikDoodleShadow-Regular.ttf'

# Colors
FLOOR_NUMBER_DEFAULT_COLOR = (0, 0, 0)
FLOOR_NUMBER_ACTIVE_COLOR = (0, 255, 0)
TIMER_COLOR = (255, 0, 0)
BLACK_COLOR = (0, 0, 0)
SCROLL_BAR_BG_COLOR = (200, 200, 200)
SCROLL_BAR_COLOR = (100, 100, 100)
SCROLLBAR_WIDTH = 10

# Time settings
FLOOR_TRAVEL_TIME = 0.5
ELEVATOR_WAIT_TIME = 2

# Default image paths
DEFAULT_FLOOR_IMAGE = "wall.png"
DEFAULT_BUTTON_IMAGE = "elevator_button (1).png"
DEFAULT_ELEVATOR_IMAGE = "elv (1).png"
DEFAULT_SOUND_FILE = "ding.mp3"

# Default settings
DEFAULT_NUM_OF_FLOORS = 40
DEFAULT_NUM_OF_ELEVATORS = 12

# Neighborhood settings
BUILDING_MARGIN = 20
FOCUSED_BUILDING_COLOR = (255, 0, 0)

# Default neighborhood configuration
DEFAULT_NEIGHBORHOOD_CONFIG = [
    {'floors': 10, 'elevators': 2},
    {'floors': 15, 'elevators': 3},
    {'floors': 12, 'elevators': 7},
    {'floors': 16, 'elevators': 5},
    {'floors': 6, 'elevators': 4}
]