"""
Configuration constants for VisualiserStudio
"""
from enum import Enum
from typing import Tuple

# Application
APP_NAME = "VisualiserStudio"
APP_VERSION = "9.0 ULTIMATE"

# Default Resolution
DEFAULT_WIDTH = 1920
DEFAULT_HEIGHT = 1080

# Preview Settings
PREVIEW_FPS = 30
MIN_ZOOM = 0.25
MAX_ZOOM = 2.0

# Element Constraints
MIN_ELEMENT_SIZE = 50
RESIZE_HANDLE_SIZE = 10
GRID_SNAP_SIZE = 10

# Gradients
GRADIENTS = {
    "Ocean": [(0, 119, 190), (0, 180, 216), (72, 202, 228)],
    "Sunset": [(255, 94, 77), (251, 206, 177), (255, 158, 128)],
    "Fire": [(255, 0, 0), (255, 165, 0), (255, 255, 0)],
    "Purple": [(138, 43, 226), (186, 85, 211), (221, 160, 221)],
    "Neon": [(0, 255, 255), (255, 0, 255), (255, 255, 0)],
    "Mint": [(0, 255, 127), (127, 255, 212), (175, 238, 238)],
    "Warm": [(255, 0, 0), (255, 127, 0), (255, 255, 0)],
    "Cool": [(0, 0, 255), (0, 127, 255), (0, 255, 255)],
    "Vintage": [(139, 69, 19), (184, 134, 11), (218, 165, 32)],
    "Forest": [(34, 139, 34), (50, 205, 50), (144, 238, 144)],
}

class VisualizerType(Enum):
    BARS = "bars"
    MIRROR_BARS = "mirror_bars"
    LINE = "line"
    AREA = "area"
    CIRCULAR = "circular"
    RING = "ring"
    DOTS = "dots"
    WAVEFORM = "waveform"
    PIXEL_EQ = "pixel_eq"
    RIBBON = "ribbon"
    SPIRAL = "spiral"
    PULSE_CIRCLE = "pulse_circle"

class ElementType(Enum):
    TEXT = "text"
    VISUALIZER = "visualizer"
    PROGRESS_BAR = "progress_bar"
    LYRICS = "lyrics"
    LOGO = "logo"

class ProgressBarStyle(Enum):
    SOLID = "solid"
    PILL = "pill"
    SEGMENTED = "segmented"
    DASHED = "dashed"
    NEON = "neon"

# Export Settings
DEFAULT_FPS = 30
DEFAULT_CRF = 18
VIDEO_CODEC = "libx264"
AUDIO_CODEC = "aac"
AUDIO_BITRATE = "320k"

# Grid Settings
GRID_SIZES = [5, 10, 25, 50]
DEFAULT_GRID_SIZE = 10

# Effects
MAX_GLOW_BLUR = 101
DEFAULT_GLOW_BLUR = 31
DEFAULT_GLOW_INTENSITY = 0.5

# Keyboard Shortcuts
SHORTCUTS = {
    # File
    "Ctrl+N": "New Project",
    "Ctrl+O": "Open Project",
    "Ctrl+S": "Save Project",
    "Ctrl+Shift+S": "Save Project As",
    "Ctrl+E": "Export Video",
    "Ctrl+Q": "Quit",
    
    # Edit
    "Ctrl+Z": "Undo",
    "Ctrl+Y": "Redo",
    "Ctrl+C": "Copy",
    "Ctrl+V": "Paste",
    "Ctrl+D": "Duplicate",
    "Delete": "Delete Element",
    "Ctrl+A": "Select All",
    "Escape": "Deselect",
    
    # Playback
    "Space": "Play/Pause",
    "Home": "Go to Start",
    "End": "Go to End",
    
    # View
    "Ctrl+0": "Reset Zoom",
    "Ctrl++": "Zoom In",
    "Ctrl+-": "Zoom Out",
    "Ctrl+G": "Toggle Grid",
    "Ctrl+B": "Toggle Borders",
    "F11": "Fullscreen",
    
    # Add Elements
    "Ctrl+Alt+V": "Add Visualizer",
    "Ctrl+Alt+T": "Add Text",
    "Ctrl+Alt+P": "Add Progress Bar",
    "Ctrl+Alt+L": "Add Lyrics",
}

# Window Settings
WINDOW_MIN_WIDTH = 1200
WINDOW_MIN_HEIGHT = 800
WINDOW_DEFAULT_WIDTH = 1600
WINDOW_DEFAULT_HEIGHT = 900

# Performance
MAX_UNDO_HISTORY = 50
FRAME_CACHE_SIZE = 100
PREVIEW_UPDATE_INTERVAL = 33  # ~30 FPS

# Colors
SELECTION_COLOR = (0, 255, 255)  # Cyan
GRID_COLOR = (80, 80, 80)
GUIDE_COLOR = (255, 0, 255)  # Magenta
BACKGROUND_COLOR = (20, 20, 20)

# Fonts
DEFAULT_FONTS = [
    "Arial",
    "Arial Black",
    "Comic Sans MS",
    "Courier New",
    "Georgia",
    "Impact",
    "Times New Roman",
    "Trebuchet MS",
    "Verdana"
]"""
Configuration constants for VisualiserStudio
"""
from enum import Enum
from typing import Tuple

# Application
APP_NAME = "VisualiserStudio"
APP_VERSION = "8.0"

# Default Resolution
DEFAULT_WIDTH = 1920
DEFAULT_HEIGHT = 1080

# Preview Settings
PREVIEW_FPS = 30
MIN_ZOOM = 0.25
MAX_ZOOM = 2.0

# Element Constraints
MIN_ELEMENT_SIZE = 50
RESIZE_HANDLE_SIZE = 10
GRID_SNAP_SIZE = 10

# Gradients
GRADIENTS = {
    "Ocean": [(0, 119, 190), (0, 180, 216), (72, 202, 228)],
    "Sunset": [(255, 94, 77), (251, 206, 177), (255, 158, 128)],
    "Fire": [(255, 0, 0), (255, 165, 0), (255, 255, 0)],
    "Purple": [(138, 43, 226), (186, 85, 211), (221, 160, 221)],
    "Neon": [(0, 255, 255), (255, 0, 255), (255, 255, 0)],
    "Mint": [(0, 255, 127), (127, 255, 212), (175, 238, 238)],
}

class VisualizerType(Enum):
    BARS = "bars"
    MIRROR_BARS = "mirror_bars"
    LINE = "line"
    AREA = "area"
    CIRCULAR = "circular"
    RING = "ring"
    DOTS = "dots"
    WAVEFORM = "waveform"

class ElementType(Enum):
    TEXT = "text"
    VISUALIZER = "visualizer"
    PROGRESS_BAR = "progress_bar"
    LYRICS = "lyrics"
    LOGO = "logo"

# Export Settings
DEFAULT_FPS = 30
DEFAULT_CRF = 18
VIDEO_CODEC = "libx264"
AUDIO_CODEC = "aac"
AUDIO_BITRATE = "320k"
