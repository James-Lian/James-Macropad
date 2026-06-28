print("Starting")

import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC, make_key
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.modules.encoder import EncoderHandler
from kmk.modules.mouse_keys import MouseKeys
from kmk.modules.combos import Combos, Chord, Sequence
from kmk.extensions_media_keys import MediaKeys


keyboard = KMKKeyboard() # class instance
combos = Combos()
layers = Layers()
encoder_handler = EncoderHandler()
mousekeys = MouseKeys(
    max_speed = 10,
    acc_interval = 20, # Delta ms to apply acceleration
    move_step = 1
)

keyboard.modules = [
    layers, 
    combos,
    # combo_layers,
    # holdtap,
    # sticky_mod,
    # sticky_keys,
    # macros,
    encoder_handler,
    mousekeys,
]
keyboard.extensions.append(MediaKeys())

keyboard.col_pins = (board.D3, board.D10, board.D9, board.D6)
keyboard.row_pins = (board.D0, board.D1, board.D2)
keyboard.diode_orientation = DiodeOrientation.COL2ROW


# custom modifier keys
# MOD1 = KC.F13
# MOD1_active = False
# MOD2 = KC.F14
# MOD2_active = False

keyboard.keymap = [
    # std layer
    [
        [KC.ESCAPE, KC.F2, KC.F11, KC.F12],
        [KC.HOME, KC.UP, KC.ENTER, KC.ENTER], # ENTER double-key
        [KC.END, KC.LEFT, KC.DOWN, KC.RIGHT],
    ],
    # art layer
    [
        [KC.K, KC.L, KC.SLASH, KC.E], # or Esc, R, Slash, E
        [KC.LSHIFT, KC.R, KC.B, KC.M], # or Shift, Shift, B, M
        [KC.LEADER, KC.N3, KC.SPACE, KC.SPACE],
    ]
]

combos.combos = [
    Sequence((KC.LEADER, KC.R), KC.LCTRL(KC.Z)), 
    Sequence((KC.LEADER, KC.LSHIFT, KC.R), KC.LCTRL(KC.LSHIFT(KC.Z))),
    Sequence((KC.LEADER, KC.LSHIFT, KC.M), KC.LCTRL(KC.LSHIFT(KC.M))), # ctrl shift m
    Sequence((KC.LEADER, KC.LSHIFT, KC.B), KC.LCTRL(KC.LSHIFT(KC.K))), # ctrl shift k
    Sequence((KC.LEADER, KC.LSHIFT, KC.L), KC.LCTRL(KC.LSHIFT(KC.A))), # ctrl shift a
    Sequence((KC.LEADER, KC.LSHIFT, KC.R), KC.LCTRL(KC.LSHIFT(KC.R))), #ctrl shift r
    Sequence((KC.LEADER, KC.E), KC.EQUAL),
    Sequence((KC.LEADER, KC.SLASH), KC.MINUS),
    Sequence((KC.LEADER, KC.K), KC.A), # for selection
    Sequence((KC.Leader, KC.L), KC.S) # for selection
]

# Layers
LYR_STD, LYR_ART = 0, 1

import busio
from kmk.extensions.display import Display, TextEntry
# for SSD1306
from kmk.extensions.display.ssd1306 import SSD1306

i2c_bus = busio.I2C(board.D5, board.D4)

driver = SSD1306(i2c=i2c_bus)

display = Display(
    # Mandatory:
    display=driver,
    # Optional:
    width=128, # screen size
    height=32, # screen size
    flip = False, # flips your display content
    brightness=1.0, # initial screen brightness level
    brightness_step=0.1, # used for brightness increase/decrease keycodes
    dim_time=20, # time in seconds to reduce screen brightness
    dim_target=0.1, # set level for brightness decrease
    off_time=60, # time in seconds to turn off screen
    powersave_dim_time=10, # time in seconds to reduce screen brightness
    powersave_dim_target=0.1, # set level for brightness decrease
    powersave_off_time=30, # time in seconds to turn off screen
)


display.entries = [
    TextEntry(text='Layer: ', x=0, y=32, y_anchor='B'),
    TextEntry(text='STND', x=40, y=32, y_anchor="B", layer=0),
    TextEntry(text='ART', x=40, y=32, y_anchor="B", layer=1),
    TextEntry(text='0', x=0, y=4, inverted=True, layer=0),
    TextEntry(text='1', x=0, y=4, inverted=True, layer=1),
]
keyboard.extensions.append(display)



encoder_handler.pins = (
    (board.D7, board.D8, None) # direction encoder pins A, B, and button pin, and divisor for detent pulses
)

encoder_handler.map = [
    ((KC.VOLD, KC.VOLU),), # standard layer
    ((KC.MS_UP, KC.MS_DN),) # art layer
]


if __name__ == '__main__':
    keyboard.go()