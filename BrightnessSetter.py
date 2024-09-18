import screen_brightness_control as sbc


current_brightness = sbc.get_brightness()
print(f"Current brightness: {current_brightness}%")

#PARAMETER
brightness = 50

# Set the brightness to DAY%
sbc.set_brightness(brightness)
print(f"Brightness set to {sbc.get_brightness()}%")