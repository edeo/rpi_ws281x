# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time

from neopixel import *

def isNaN(num):
         return num != num

# LED strip configuration:
LED_COUNT      = 30      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

import requests
import pandas as pd

count =0

while(count<1000):
   y = requests.get("https://api.wmata.com/TrainPositions/TrainPositions?contentType=json&api_key=bce6ec600e2342f28bc7751435ac0f52" )
   x = y.json()
   z = pd.DataFrame(x['TrainPositions'])
   gr = z[z['LineCode'] =='GR']
   routes = requests.get("https://api.wmata.com/TrainPositions/StandardRoutes?contentType=json&api_key=bce6ec600e2342f28bc7751435ac0f52")
   rt = routes.json()
   gnrt = pd.DataFrame(rt['StandardRoutes'][1]['TrackCircuits'])
   led = pd.read_csv('led.csv')
   rt_led = pd.merge(left=gnrt,right=led, how='left', left_on='SeqNum',right_on='SeqNum')
   train_locations =  pd.merge(left=gr,right=rt_led,how='left',left_on='CircuitId',right_on='CircuitId')
   df = train_locations
   df1 = df[(df.DirectionNum  == 1)]
   df2 = df1['led']
   strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
   strip.begin()
   print ('Press Ctrl-C to quit.')
   print(df2)
   for x in df2:
       if isNaN(x)==True:
           strip.setPixelColor(0,16711680)
           strip.show()
       else:
           strip.setPixelColor(int(x),16711680)
           strip.show()
   print(df1)
   count = count + 1
   time.sleep(3)
