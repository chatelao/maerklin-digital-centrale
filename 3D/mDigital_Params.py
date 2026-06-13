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
BOSS_DIA = INLAY_DIA + (2 * THICK)
BOSS_HOLE_DIA = INLAY_DIA
BOSS_HOLE_DEPTH = INLAY_DEPTH + 0.5
BOSS_OFFSET = 15.0 # Offset from edges

PLATE_HOLE_DIA = 3.4
PLATE_CB_DIA = 6.5
PLATE_CB_DEPTH = 3.0

# Ventilation Slots (mm)
V_SLOT_W = 2.0
V_SLOT_L = 35.0
V_SLOT_P = 4.0
V_SLOT_D = THICK + 2.0
V_START_Y = 40.0

V_STD_SLOTS = 12
V_STD_L_X = 30.0
V_STD_R_X = 105.0

V_SLIM_SLOTS = 8
V_SLIM_C_X = W_SLIM / 2.0

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

# Faceplate & Controls (mm)
FP_POCKET_DEPTH = 1.0
FP_THICK = 0.8
FP_INSET = 5.0
FP_LENGTH_STD = 60.0
FP_LENGTH_6040 = 110.0
FP_LENGTH_6043 = 115.0
FP_LENGTH_80F = 110.0
FP_LENGTH_66045 = 110.0

KNOB_DIA = 30.0
KNOB_H = 15.0
KNOB_SHAFT_DIA = 6.0

SMALL_KNOB_DIA = 20.0
SMALL_KNOB_H = 10.0

BTN_SIZE = 12.0
BTN_CUTOUT = 12.4

ROUND_BTN_DIA = 12.0
ROUND_BTN_CUTOUT = 12.4

# LED (Status Lights)
LED_DIA = 3.0

# 7-Segment Display (4-Digit)
DISPLAY_W = 50.0
DISPLAY_H = 19.0
DISPLAY_RECESS = 2.0

# 7-Segment Display (2-Digit)
DISPLAY_2_W = 28.0
DISPLAY_2_H = 15.0

# 6021 Specific Layout (Offsets relative to Faceplate Inlay corner)
C6021_DISPLAY_X = 10.0
C6021_DISPLAY_Y = 35.0

C6021_FBTN_GRID_X = 85.0
C6021_FBTN_GRID_Y = 40.0
C6021_FBTN_PITCH = 16.0

C6021_KPAD_X = 20.0
C6021_KPAD_Y = 8.0
C6021_KPAD_PITCH_X = 16.0
C6021_KPAD_PITCH_Y = 13.0

C6021_KNOB_X = 95.0
C6021_KNOB_Y = 15.0

# 6040 Specific Layout (Keyboard)
C6040_GRID_X = 25.0
C6040_GRID_Y = 10.0
C6040_PITCH_X = 75.0
C6040_PITCH_Y = 13.0

# 6043 Specific Layout (Memory)
C6043_DISPLAY_X = 10.0
C6043_DISPLAY_Y = 96.0

C6043_GRID_X = 22.3
C6043_GRID_Y = 5.0
C6043_PITCH_X = 40.0
C6043_PITCH_Y = 12.5

# 6036 / 80f Specific Layout (Slim Control)
C80F_DISPLAY_X = 4.0
C80F_DISPLAY_Y = 85.0

C80F_KNOB_X = 28.75
C80F_KNOB_Y = 20.0

C80F_BTN_X = 15.0
C80F_BTN_Y = 60.0
C80F_BTN_PITCH_X = 27.5
C80F_BTN_PITCH_Y = 13.0

# 6070 IR Window (Infra Control)
C6070_IR_W = 30.0
C6070_IR_H = 4.0
C6070_IR_X = 13.55 # Centered on slim inlay
C6070_IR_Y = 105.0

# 6017 Specific Layout (Booster)
C6017_LED_X = 15.0
C6017_LED_Y = 35.0
C6017_LED_PITCH = 10.0

# 66045 Specific Layout (Delta Control 4f)
C66045_SEL_KNOB_X = 35.0
C66045_SEL_KNOB_Y = 85.0

C66045_BTN_X = 90.0
C66045_BTN_Y = 85.0

C66045_MAIN_KNOB_X = 62.3
C66045_MAIN_KNOB_Y = 35.0

# Aesthetics (Colors)
COLOR_MAERKLIN_GREY = (0.694, 0.694, 0.694) # #B1B1B1
COLOR_BLACK = (0.0, 0.0, 0.0)
COLOR_SIGNAL_RED = (0.647, 0.125, 0.098)    # #A52019

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
