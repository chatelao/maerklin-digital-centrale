import math

"""
Märklin Digital 60xx Series - Parametric Constants
Source: MAERKLIN_DIGITAL_3D_PARAMETERS.md
"""

# Global Dimensions (mm)
W_STD = 135.0
W_SLIM = 67.5
DEPTH = 120.0
H_FRONT = 25.0
H_BACK = 55.0
THICK = 2.5
TOL = 0.2

# Fastening System (mm)
SCREW_SIZE = 3.0   # M3
INLAY_DIA = 4.6    # Heat-set inlay OD
INLAY_DEPTH = 5.0

# Calculated Constants
SLOPE_ANGLE = math.degrees(math.atan((H_BACK - H_FRONT) / DEPTH)) # ~14.036°

# DIN 41612 B/2 Cutout (Side Panels)
DIN_CUTOUT_W = 54.8
DIN_CUTOUT_H = 14.8
DIN_CUTOUT_Y_CENTER = 60.0
DIN_CUTOUT_Z_CENTER = 12.5

# Interlocking Side-Panels (Patent DE 84 27 671 U1)
INTERLOCK_TAB_W = 5.0
INTERLOCK_TAB_H = 10.0
INTERLOCK_TAB_D = 20.0
INTERLOCK_FRONT_Y = 20.0
INTERLOCK_BACK_Y = 100.0
INTERLOCK_Z_CENTER = 12.5

def get_vertices(width):
    """Returns the 8 vertices for the base wedge primitive."""
    return [
        (0, 0, 0),             # V0: Bottom-Front-Left
        (0, DEPTH, 0),         # V1: Bottom-Back-Left
        (width, DEPTH, 0),     # V2: Bottom-Back-Right
        (width, 0, 0),         # V3: Bottom-Front-Right
        (0, 0, H_FRONT),       # V4: Top-Front-Left
        (0, DEPTH, H_BACK),    # V5: Top-Back-Left
        (width, DEPTH, H_BACK),# V6: Top-Back-Right
        (width, 0, H_FRONT)    # V7: Top-Front-Right
    ]
