# ScreenBrightness
This is a project that adjusts brightness of a screen based on sun position. It works based on suntimes.csv file which consists times of sunrises and sunsets for every day of a year. The file was prepepared for Warsaw but you can generate it for any city in Poland using another one of my projects: DayDuration. Two times a day (around sunrise and sunset) it smoothly changes your screen brightness: from low to high and from high to low.

## INSTRUCTION FOR WINDOWS
In order to run use script you need to do the following:
1. Make sure you have python installed on your machine
2. Install the modules listed in requirements file you can use command:
    pip install -r requirements.txt
3. Set the parameters in python code. 
    a) day_brightness - max brightness
    b) night_brightness = min brightness
    c) transition_time_h - time it takes for full transition from one threshold brightness to another (in hours)

    In order to set the threshold values you can use BrightnessSetter.py so that you can choose desirable value for both day and night.
4. Swap the paths in ScreenBrightness.bat file with the locations of files listed below on your machine.
    a) pythonw.exe
    b) ScreenBrightness
5. Put the .bat file into your Autostart folder. (You can open it using WindowsKey + R and then type shell:startup)

Congratulations! Now every time you start your computer the script will be running in the background adjusting the brightness of your screen based on parameters you set. 
Enjoy!
