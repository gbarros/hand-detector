"""
 This file will contain any hardcoded lists, enumarations and dicts
"""

PRESET_COLORS = [
    (0, 0, 255),      # Red
    (255, 0, 0),      # Blue
    (0, 255, 255),    # Yellow
    (128, 0, 128),    # Purple
    (0, 128, 0),      # Green
    (255, 0, 255),    # Magenta
    (0, 255, 0),      # Lime
    (255, 255, 0),    # Cyan
    (192, 192, 192),  # Silver
    (128, 128, 128),  # Gray
    (0, 0, 128),      # Maroon
    (0, 128, 128),    # Olive
    (128, 128, 0),    # Teal
    (128, 0, 0),      # Navy
    (0, 0, 0),        # Black
    (255, 255, 255)  # White
]

# These scan points are used for the image annotation tool as
# preset points of interest to scan and threshold the skin color
PRESET_SCAN_POINTS = [
    [(200, 110), (210, 120)],
    [(220, 100), (225, 105)],
    [(260, 130), (270, 140)],
    [(200, 190), (210, 200)],
    [(180, 150), (190, 160)]
]
