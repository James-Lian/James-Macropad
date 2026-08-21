print("Starting")

import board
import busio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.modules.encoder import EncoderHandler
from kmk.modules.mouse_keys import MouseKeys
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.display import Display, TextEntry
from kmk.extensions.display.ssd1306 import SSD1306

import time

keyboard = KMKKeyboard()
layers = Layers()
encoder_handler = EncoderHandler()
mousekeys = MouseKeys(
    max_speed = 10,
    acc_interval = 20,
    move_step = 1
)

# Using standard KMK setup 
keyboard.col_pins = (board.D3, board.D10, board.D9, board.D6)
keyboard.row_pins = (board.D0, board.D1, board.D2)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

KEY_LABELS = {
    0: {
        0: "ESC", 1: "F2", 2: "F11", 3: "F12", 
        4: "HOME", 5: "END", 6: "UP", 7: "TG(Default)", 
        8: "MO(Numpad)", 9: "LEFT", 10: "DOWN", 11: "RIGHT"
    },
    1: {
        0: "Backspace", 1: "7", 2: "8", 3: "9", 
        4: "Enter", 5: "4", 6: "5", 7: "6", 
        8: "MO(Numpad)", 9: "1", 10: "2", 11: "3"
    },
    2: {
        0: "A", 1: "S", 2: "E", 3: "R", 
        4: "Del", 5: "/", 6: "B", 7: "TG(Art)", 
        8: "Ctrl", 9: "3", 10: "Space", 11: "M"
    },
    3: {
        0: "Ctrl+A", 1: "Ctrl+S", 2: "Ctrl+E", 3: "Ctrl+T", 
        4: "Ctrl+Shift", 5: "Ctrl+Z", 6: "Ctrl+G", 7: "Ctrl+J", 
        8: "Ctrl", 9: "Ctrl+X", 10: "Ctrl+C", 11: "Ctrl+R"
    },
    4: {
        0: "Ctrl+Shift+A", 1: "Ctrl+Shift+S", 2: "Minus", 3: "Plus", 
        4: "Ctrl+Shift", 5: "Ctrl+Shift+Z", 6: "Ctrl+Shift+I", 7: "PgUp", 
        8: "Ctrl", 9: "C+S+R", 10: "F11", 11: "PgDn"
    },
}

keyboard.keymap = [
    # Layer 0: Standard
    [
        KC.ESCAPE, KC.F2,   KC.F11,   KC.F12,
        KC.HOME,   KC.END,  KC.UP,    KC.TG(2), 
        KC.MO(1),  KC.LEFT, KC.DOWN,  KC.RIGHT
    ],
    # Layer 1: Standard modifier layer
    [
        KC.BSPACE, KC.KP_7, KC.KP_8, KC.KP_9, 
        KC.ENTER,  KC.KP_4, KC.KP_5, KC.KP_6, 
        KC.TRNS,   KC.KP_1, KC.KP_2, KC.KP_3
    ],
    # Layer 2: Art
    [
        KC.A,     KC.S,     KC.E,     KC.R, # or Escmm, R, Slash, E
        KC.DEL,   KC.SLASH, KC.B,     KC.TG(2), # or Shift, Shift, B, M
        KC.MO(3), KC.N3,    KC.SPACE, KC.M # SPACE, layer toggle back to std
    ],
    # Layer 3: Art (CTRL) modifier layer
    [
        KC.LCTRL(KC.A), KC.LCTRL(KC.S), KC.LCTRL(KC.E), KC.LCTRL(KC.T),
        KC.MO(4),       KC.LCTRL(KC.Z), KC.LCTRL(KC.G), KC.LCTRL(KC.J),
        KC.TRNS,        KC.LCTRL(KC.X), KC.LCTRL(KC.C), KC.LCTRL(KC.R)
    ],
    # Layer 4: Art (SHIFT) modifier layer
    [
        KC.LCTRL(KC.LSHIFT(KC.A)), KC.LCTRL(KC.LSHIFT(KC.S)), KC.MINUS,                  KC.PLUS,
        KC.TRNS,                   KC.LCTRL(KC.LSHIFT(KC.Z)), KC.LCTRL(KC.LSHIFT(KC.I)), KC.PGUP,
        KC.TRNS,                   KC.LCTRL(KC.LSHIFT(KC.R)), KC.F11,                    KC.PGDN
    ]
]

LYR_STD, LYR_ART = 0, 1

# OLED Setup 
i2c_bus = board.I2C() 
driver = SSD1306(i2c=i2c_bus)

display = Display(
    display=driver,
    width=128,
    height=32,
    flip = False,
    brightness=0.8,
    brightness_step=0.1,
    dim_time=20,
    dim_target=0.1,
    off_time=60,
    powersave_dim_time=10,
    powersave_dim_target=0.1,
    powersave_off_time=30,
)

input_display_entry = TextEntry(text=" ", x=0, y=0, y_anchor="T")
layer_display_num = TextEntry(text='0:', x=32, y=31, y_anchor="B")
layer_display_name = TextEntry(text='DEFAULT', x=50, y=31, y_anchor="B")
LAYER_NAMES = {
    0: "DEFAULT", 
    1: "NUMPAD",
    2: "ART",
    3: "ART-CTRL",
    4: "ART-CTRL-SHIFT"
}

display.entries = [
    input_display_entry,
    TextEntry(text='Layer', x=0, y=31, y_anchor="B"),
    layer_display_num,
    layer_display_name,
]
keyboard.extensions.append(display)

class OLEDManager:
    def __init__(self):
        self.held_keys = []
        self.last_text = ""
        self.last_input_time = time.monotonic()
        self.is_cleared = False
        self.last_layer = 0

    def process_key(self, keyboard, key, is_pressed, int_coord=None, *args, **kwargs):
        # coord is integer representing physical key location
        coord = int_coord 
        if coord is None and "coord_int" in kwargs:
            coord = kwargs["coord_int"]
        if coord is None and len(args) > 0 and isinstance(args[0], int):
            coord = args[0]

        # track physical keys going up and down
        if coord is not None:
            if is_pressed: # press events
                if coord not in self.held_keys:
                    self.held_keys.append(coord)
            else: # release events
                if coord in self.held_keys:
                    self.held_keys.remove(coord)

        return key

    # constantly monitors keyboard for layer changes, etc.
    def after_matrix_scan(self, keyboard, *args, **kwargs):
        current_time = time.monotonic()
        new_text = None
        top_layer = max(keyboard.active_layers) if keyboard.active_layers else 0

        if top_layer != self.last_layer:
            top_layer = max(keyboard.active_layers) if keyboard.active_layers else 0
            layer_display_num.text = f"{top_layer}: "
            layer_display_name.text = f"{LAYER_NAMES.get(top_layer, 'UNKNOWN')}"

        # 1. If keys are held, grab the label
        if len(self.held_keys) > 0:
            active_coord = self.held_keys[-1]
            label = KEY_LABELS.get(top_layer, {}).get(active_coord, "Key")
            new_text = f"{label}"
            
            # Reset timer and clear flag while actively holding keys
            self.last_input_time = current_time
            self.is_cleared = False

        # 2. If no keys are held, check if 5 seconds have passed since release
        elif not self.is_cleared and (current_time - self.last_input_time >= 5):
            self.is_cleared = True
            new_text = " "

        # 3. Apply changes if there's something new to show/clear
        if new_text is not None and new_text != self.last_text:
            # prevent rerenders of modifier keys after rendering valid key press
            if (self.last_text in KEY_LABELS[1].values()) and (new_text == "MO(Numpad)"):
                return
            if (self.last_text in KEY_LABELS[3].values()) and (new_text == "Ctrl"):
                return
            if (self.last_text in KEY_LABELS[4].values()) and (new_text == "Ctrl+Shift" and self.last_text != "Ctrl"):
                return
            
            input_display_entry.text = new_text
            self.last_text = new_text

            self.last_layer = top_layer
            try:
                display.render(keyboard)
            except AttributeError:
                pass
        else:
            if top_layer != self.last_layer:
                self.last_layer = top_layer
                try:
                    display.render(keyboard)
                except AttributeError:
                    pass


    # Required boilerplate
    def during_bootup(self, *args, **kwargs): pass
    def before_matrix_scan(self, *args, **kwargs): pass
    def before_hid_send(self, *args, **kwargs): pass
    def after_hid_send(self, *args, **kwargs): pass
    def on_powersave_enable(self, *args, **kwargs): pass
    def on_powersave_disable(self, *args, **kwargs): pass

keyboard.modules = [
    OLEDManager(),
    layers, 
    encoder_handler,
    mousekeys,
]
keyboard.extensions.append(MediaKeys())

# Encoder Setup
encoder_handler.pins = (
    (board.D7, board.D8, None),
)

encoder_handler.map = [
    ((KC.VOLD, KC.VOLU),),
    ((KC.MS_UP, KC.MS_DN),)
]

if __name__ == '__main__':
    keyboard.go()
