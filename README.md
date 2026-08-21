# James-Macropad
A functional 3x4 layout macropad created following Hack Club's Hackpad guide. Designed to be used for digital art on Krita. 

<img width="774" height="777" alt="image" src="https://github.com/user-attachments/assets/3eca3088-ac46-4613-ba21-6f261d3027d8" />

## 💡 Features
- 3x4 layout, 12 Cherry MX keys
- rotary encoder
- OLED screen
- custom designed rotary encoder knurled knob
- 5 profiles (default + numpad + art + art-ctrl + art-shift)

## 🔌 PCB
Below is the schematic and PCB.
<br>
<img width="466" height="610" alt="image" src="https://github.com/user-attachments/assets/73b9e42f-ff6c-4b16-ad2d-2ee9c5b2ba81" />
<img width="867" height="834" alt="image" src="https://github.com/user-attachments/assets/398214c7-57e5-4c40-a0cb-340faa0f8970" />

## 🧱 Case CAD model
The case is made up of two parts; a top section and a bottom section. The PCB is mounted plateless on the bottom section. <img width="946" height="628" alt="image" src="https://github.com/user-attachments/assets/1968c931-d70d-4938-b0b0-71b5a0e8fe90" />   
<img width="949" height="481" alt="image" src="https://github.com/user-attachments/assets/569e52c5-1e92-4904-8182-462ff799cd38" />   
I've also designed a custom knob to fit on the rotary encoder. I've taken inspiration from the knob on alexren's OrpheusPad, while adding some adjustments to ensure that the knob is smaller so it fits better between the rotary encoder and the keycaps.
<img width="493" height="352" alt="image" src="https://github.com/user-attachments/assets/838a79be-5942-4099-bce4-8b674d89cbab" />

## 📋 BOM
Here's everything needed to make this hackpad.
- 12x Cherry MX switches
- 12x DSA keycaps
- 6x M3x16mm screws
- 6x M3x5mmx4mm heatset inserts
- 1x 0.91 inch OLED display
- 1x EC11 rotary encoder
- 12x 1N4148 diodes
- 1x unsoldered Seeed XIAO RP2040
- + the custom-designed case (3 printed parts: bottom, top, knob)
 
## ⚙️ Assembly
1. Solder the diodes, Seeeduino, OLED, and rotary encoder to the PCB (recommended in that order)
2. Install CircuitPython on the Seeeduino, and then KMK, as well as the adafruit_display_text, adafruit_framebuf.mpy, adafruit_displayio_ssd1306.mpy, and adafruit_ssd1306.mpy libraries (recommended to do this before the "Middle" 3d printed part blocks the Seeeduino bootloader button)
5. Push the 12 Cherry MX switches through the holes in the "Middle" 3d printed part, and then solder the backs of the switches to the PCB
6. Heatset the inserts into the "Bottom" 3d printed part (4 in total) and install the screws from the top.
<br>
<img width="3024" height="3506" alt="image" src="https://github.com/user-attachments/assets/fe5150ec-9cb9-483a-a22e-53147651a4c8" />

## ⭐ How to Use
Below is a screenshot of the keymap layers (arranged in a 3x4 layout), along with a screenshot of KEY_LABELS that denote what each key does.
<br>
The MO keys temporarily change the macropad's layers when holding them down. The TG keys toggle between the default and art layers. On the art layer (layer 2), holding MO(3) toggles the ART-CTRL layer, essentially acting like a CTRL modifier key and allowing the user to access CTRL-related commands. Holding both the MO(3) and MO(4) keys toggles the ART-CTRL-SHIFT layer, which allows you to access CTRL-SHIFT-related commands and other additional keys. 
<br>
<img width="652" height="651" alt="image" src="https://github.com/user-attachments/assets/f77a66ad-3a19-4881-9e3d-b669b894a657" />
<img width="493" height="543" alt="image" src="https://github.com/user-attachments/assets/36e7c99f-1a04-4f12-9b4a-969346fa473d" />


