""" Let's Create The Cat Toys Main Code """

# Import Needed libraries
import time
import board
import asyncio                     # Allows simultaneous running

import neopixel                    # Needed For LEDs
from rainbowio import colorwheel   # Needed For LEDs

import pwmio                       # Needed For Servo
from adafruit_motor import servo   # Needed For Servo

import audiomp3                    # Needed for Speaker
import audiopwmio                  # Needed for Speaker

import digitalio                   # Needed for Sensor

import busio                       # Needed For Bluetooth



""" Code For Setting Up The WS2812 LEDs """

num_pixels = 14 # Holds the number of pixels in use
pixels = neopixel.NeoPixel(board.GP0, num_pixels) # Pin 0 , number of LEDs
pixels.brightness = 0.02


# on board LED
led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT

############################################
##          RGB color choices             ##
############################################

# Note:
# > red, green, or blue = 20mA

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)

purple = (128,0,128)
pink = (255,105,180)
yellow = (255,255,0)
orange = (255,69,0)

off = (0,0,0)

############################################




""" Code For Setting Up Servo Motor """

# create a PWMOut object on Pin 15.
pwm = pwmio.PWMOut(board.GP15, duty_cycle=2 ** 15, frequency=150)

# Create a servo object, my_servo.
my_servo = servo.Servo(pwm)




""" Code For Setting Up For STEMMA Speaker """

# create a object on Pin 13.
audio = audiopwmio.PWMAudioOut(board.GP13)



""" Code For Setting Up For HC-SR501 Sensor """

# Place on pin 14
pir = digitalio.DigitalInOut(board.GP14)
pir.direction = digitalio.Direction.INPUT

nextTime = 120 # Will allow the nect "sleep" after 120 seconds

""" Code For Setting Up For HC-05 Bluetooth """

# Pin 16 for TX & Pin 17 for RX
uart = busio.UART(board.GP16, board.GP17, baudrate=9600)

# Base toy function variabls. Global for App to change.

# 1st digit is function 
#      0 - lighting
#      1 - sound
#      2 - tail motion
# 2nd digit is pattern / sound
#      0 - Option 1 (base)
#      1 - Option 2
#      2 - Option 3
#      3 - Option 4 (off)
# Ex: O1 changes lighting to pattern option 2

data_string_light = "00"
data_string_sound = "10"
data_string_motion = "20"

# variable to check if app made a change
change = 0
temp = 0

""" Code to break between function codes """

class Controls:
    def __init__(self):
        self.reverse = False
        self.wait = 0.0
        
""" Functions """

async def LED(controls):
    ############################################
    ##           Patterns Programmed          ##
    ############################################
    
    while True:
        pixels.fill(off)
        
        # base pattern will toggle the 1 LEDS at a time
        while (data_string_light == "00"):
            
            for i in range(num_pixels):
                
                pixels[i] = red
                await asyncio.sleep(controls.wait)  # wait to bounce between tasks
                pixels.fill(off)
                if (data_string_light != "00"):
                    pixels.fill(off)
                    break
            
        # 1st pattern: toggle the 3 LEDS green, yellow ,red
        while (data_string_light == "01"):
            
            for i in range((num_pixels+2)):
                if i < 1 :
                    pixels[i] = yellow
                    time.sleep(.1)
                    
                elif i < 2 :
                    pixels[i] = red
                    time.sleep(.1)
                    pixels[i-1] = yellow
                    time.sleep(.1)
                    
                elif i == (num_pixels-1):
                    pixels[i] = green
                    time.sleep(.1)
                    pixels[i-1] = red
                    time.sleep(.1)
                    pixels[i-2] = yellow
                    time.sleep(.1)
                    
                elif i == (num_pixels):
                    pixels[i-1] = green
                    time.sleep(.1)
                    pixels[i-2] = red
                    time.sleep(.1)

                elif i == (num_pixels+1):
                    pixels[i-2] = green
                    time.sleep(.1)
                    
                else:
                    pixels[i] = green
                    time.sleep(.1)
                    pixels[i-1] = red
                    time.sleep(.1)
                    pixels[i-2] = yellow
                    time.sleep(.1)

                pixels.fill(off)
                await asyncio.sleep(controls.wait)  # wait to bounce between tasks
                if (data_string_light != "01"):
                    pixels.fill(off)
                    break
        
        # 2nd Pattern:  one at a time red, orange, yellow, green, blue, purple, pink       
        while (data_string_light == "02"):
            for i in range((num_pixels)):
                if 0 == (i%7) :
                    pixels[i] = red
                elif 1 == (i%7) :
                    pixels[i] = orange
                elif 2 == (i%7) :
                    pixels[i] = yellow
                elif 3 == (i%7) :
                    pixels[i] = green
                elif 4 == (i%7) :
                    pixels[i] = blue
                elif 5 == (i%7) :
                    pixels[i] = purple
                elif 6 == (i%7) :
                    pixels[i] = pink
                await asyncio.sleep(controls.wait)  # wait to bounce between tasks
                if (data_string_light != "02"):
                    pixels.fill(off)
                    break
                pixels[i] = off
        
        # 3rd Pattern: off
        while (data_string_light == "03"):
            await asyncio.sleep(controls.wait)  # wait to bounce between tasks
            if (data_string_light != "03"):
                break
    
            
            
async def Servo(controls):
    ############################################
    ##           Patterns Programmed          ##
    ############################################
    while True:
        # Base Pattern: Wags at a constant speed
        while ( data_string_motion == "20" ):       
            for angle in range(130, 180, 10):  # 130 - 180 degrees, 10 degrees at a time.
                my_servo.angle = angle
            await asyncio.sleep(controls.wait)   # wait to bounce between tasks
            if (data_string_motion != "20"):
                break
            for angle in range(180, 130, -10): # 180 - 130 degrees, 10 degrees at a time.
                my_servo.angle = angle
            await asyncio.sleep(controls.wait)   # wait to bounce between tasks
            if (data_string_motion != "20"):
                break
            
        # 1st Pattern: Full wag to half wag at a constant speed
        while ( data_string_motion == "21" ):
            for angle in range(130, 180, 5):  # 130 - 180 degrees, 5 degrees at a time.
                my_servo.angle = angle
            await asyncio.sleep(controls.wait)   # wait to bounce between tasks
            if (data_string_motion != "21"):
                break
            
            
            for angle in range(180, 130, -5): # 180 - 130 degrees, 5 degrees at a time.
                my_servo.angle = angle
            await asyncio.sleep(controls.wait)   # wait to bounce between tasks
            if (data_string_motion != "21"):
                break
            
            for angle in range(130, 160, 5):  # 130 - 160 degrees, 5 degrees at a time.
                my_servo.angle = angle
            await asyncio.sleep(controls.wait)   # wait to bounce between tasks
            if (data_string_motion != "21"):
                break
            
            
            for angle in range(160, 130, -5): # 160 - 130 degrees, 5 degrees at a time.
                my_servo.angle = angle
            await asyncio.sleep(controls.wait)   # wait to bounce between tasks
            if (data_string_motion != "21"):
                break
        
        # 2nd Pattern: Full wag at a fast constant speed
        while ( data_string_motion == "22" ):
            for angle in range(130, 180, 2):  # 130 - 180 degrees, 2 degrees at a time.
                my_servo.angle = angle
            
            for angle in range(180, 130, -2): # 180 - 130 degrees, 2 degrees at a time.
                my_servo.angle = angle
            await asyncio.sleep(controls.wait)   # wait to bounce between tasks
            if (data_string_motion != "22"):
                    break
        # 3rd Pattern: off
        while (data_string_light == "23"):
            await asyncio.sleep(controls.wait)  # wait to bounce between tasks
            if (data_string_light != "23"):
                break

            
async def Sleep(sleepTime, controls):
    while True :
        currentTime = time.monotonic()           # grabs current time on board
        if( sleepTime <= currentTime ):
            print("in time = ",time.monotonic())
            pixels.fill(off)
            
            # Loop that does nothing until their is motion
            while( pir.value == False):
                pass
            
            print("Motion Detected")
            sleepTime = time.monotonic() + nextTime
            
        await asyncio.sleep(controls.wait)       # wait to bounce between tasks
        
async def Speaker(controls):
    while True:
        
        while ( data_string_sound == "10" ):
            if ( data_string_sound != "10" ):
                break
            if audio.playing:
                await asyncio.sleep(controls.wait)       # wait to bounce between tasks
            else:
                # opens up the audio and decodes mp3
                decoder = audiomp3.MP3Decoder(open("squirrelCall.mp3", "rb")) 
                audio.play(decoder)
                await asyncio.sleep(controls.wait)       # wait to bounce between tasks
                
        while ( data_string_sound == "11" ):
            if ( data_string_sound != "11" ):
                break
            if audio.playing:
                await asyncio.sleep(controls.wait)       # wait to bounce between tasks
            else:
                # opens up the audio and decodes mp3
                decoder = audiomp3.MP3Decoder(open("MorningBirds.mp3", "rb")) 
                audio.play(decoder)
                await asyncio.sleep(controls.wait)       # wait to bounce between tasks


        while ( data_string_sound == "12" ):
            if ( data_string_sound != "12" ):
                break
            if audio.playing:
                await asyncio.sleep(controls.wait)       # wait to bounce between tasks
            else:
                # opens up the audio and decodes mp3
                decoder = audiomp3.MP3Decoder(open("fly.mp3", "rb")) 
                audio.play(decoder)
                await asyncio.sleep(controls.wait)       # wait to bounce between tasks
        
        # 3rd Pattern: off
        while (data_string_light == "13"):
            await asyncio.sleep(controls.wait)  # wait to bounce between tasks
            if (data_string_light != "13"):
                break
                            
        
async def Bluetooth(controls):
    # notates using a global variable and not a new variable with the same name
    global data_string_light
    global data_string_sound
    global data_string_motion
    
    while True:
        # Grab message from app
        # But this slows down the code**
        data = uart.read(32)          # read up to 32 bytes
    
        if data is not None:
            data_string = ''.join([chr(b) for b in data]) #Sets the grabbed datta into a string to read
            
            # checks to see if light pattern changed
            if ( (data_string == "00") | (data_string == "01") | (data_string == "02") | (data_string == "03") ):
                data_string_light = data_string
            
            # checks to see if sound changed
            if ( (data_string == "10") | (data_string == "11") | (data_string == "12") | (data_string == "13") ):
                data_string_sound = data_string
                print(data_string_sound)
                
            # checks to see if tail motion changed
            if ( (data_string == "20") | (data_string == "21") | (data_string == "22") | (data_string == "23") ):
                data_string_motion = data_string
                print(data_string_motion)                

        await asyncio.sleep(controls.wait)    
            
async def main():
    print("Program start:")
    controls = Controls()
    sleepTime = start + nextTime    # sets time for nexTime value
    #led.value = True                # turns on the on board LED
    
    servo_task = asyncio.create_task(Servo(controls))
    LED_task = asyncio.create_task(LED(controls))
    Sleep_task = asyncio.create_task(Sleep(sleepTime,controls))
    Speaker_task = asyncio.create_task(Speaker(controls))
    Bluetooth_task = asyncio.create_task(Bluetooth(controls))
  
    await asyncio.gather(servo_task, LED_task , Sleep_task,Speaker_task, Bluetooth_task)   


start = time.monotonic() # grabs current time on board
print("time= ", start)
asyncio.run(main())      #begins the program
