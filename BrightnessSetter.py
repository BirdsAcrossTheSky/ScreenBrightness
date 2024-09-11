import screen_brightness_control as sbc


#PARAMETERS
day_brightness = 75
night_brightness = 25

current_brightness = sbc.get_brightness()
print(f"Current brightness: {current_brightness}%")

# Set the brightness to DAY%
sbc.set_brightness(day_brightness)
print(f"Brightness set to {sbc.get_brightness()}%")