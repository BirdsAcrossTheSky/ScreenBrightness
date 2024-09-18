import screen_brightness_control as sbc
import schedule
import time
from datetime import datetime, timedelta
import pandas as pd
import functools
import logging
import os


script_path = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(
    filename=f'{script_path}/brightness.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def SetBrightness(value):
    sbc.set_brightness(value)
    logging.info(f'Brightness set to {value}')


def TimeWindow(timespan_h,  s_time):
    base_time = datetime.strptime(s_time, '%H:%M')
    start_time = base_time - timedelta(hours=timespan_h / 2)
    end_time = base_time + timedelta(hours=timespan_h / 2)
    return start_time, end_time

def BrightnessTimeSlots(timespan_h, s_time, day_brightness, night_brightness, is_sunset):
    if is_sunset:
        base_brightness = day_brightness
        end_brightness = night_brightness
        step = -1
    else:
        base_brightness = night_brightness
        end_brightness = day_brightness
        step = 1

    time_slots = []
    start_time, end_time = TimeWindow(timespan_h, s_time)
    total_duration = (end_time - start_time).total_seconds()
    interval = timedelta(seconds=round(total_duration / (abs(end_brightness - base_brightness) - 1)))
    curr_time = start_time
    
    while base_brightness != end_brightness:
        base_brightness += step
        time_slots.append((curr_time.strftime('%H:%M'), base_brightness))
        curr_time += interval

    return time_slots


#PARAMETERS
day_brightness = 75
night_brightness = 25
transition_time_h = 4

'''
# Get the current brightness
current_brightness = sbc.get_brightness()
print(f"Current brightness: {current_brightness}%")

# Set the brightness to DAY%
sbc.set_brightness(day_brightness)
print(f"Brightness set to {sbc.get_brightness()}%")
'''

logging.info(f'Started.')
current_date = datetime.now().strftime('%Y-%m-%d')

df = pd.read_csv(r'F:\Programming\VisualStudio\ScreenBrightness\suntimes.csv')
today_suntimes = df[df['Date'] == current_date]
# print(today_suntimes)

brightness_diff = day_brightness - night_brightness
sr_start_time, sr_end_time = TimeWindow(transition_time_h, today_suntimes['Sunrise time'].iloc[0])
ss_start_time, ss_end_time = TimeWindow(transition_time_h, today_suntimes['Sunset time'].iloc[0])
# print(sr_start_time, sr_end_time, ss_start_time, ss_end_time)
# print(type(sr_start_time))
# print(sr_start_time.time())

curr_time = datetime.now().time()
# print(curr_time)
if curr_time < sr_start_time.time():
    SetBrightness(night_brightness)
elif curr_time < sr_end_time.time():
    SetBrightness((night_brightness + day_brightness) / 2)
elif curr_time < ss_start_time.time():
    SetBrightness(day_brightness)
elif curr_time < ss_end_time.time():
    SetBrightness((night_brightness + day_brightness) / 2)
else:
    SetBrightness(night_brightness)


sunrise_slots = BrightnessTimeSlots(4, today_suntimes['Sunrise time'].iloc[0], day_brightness, night_brightness, 0)
sunset_slots = BrightnessTimeSlots(4, today_suntimes['Sunset time'].iloc[0], day_brightness, night_brightness, 1)
# print(sunrise_slots)
# print(sunset_slots)


# Schedule the job to run every day at a specific time
for slot in sunrise_slots:
    schedule.every().day.at(slot[0]).do(functools.partial(SetBrightness, slot[1]))
for slot in sunset_slots:
    schedule.every().day.at(slot[0]).do(functools.partial(SetBrightness, slot[1]))

while True:
    schedule.run_pending()
    time.sleep(30)

