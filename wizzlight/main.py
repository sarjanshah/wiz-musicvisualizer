import asyncio
import time
from pywizlight import wizlight, PilotBuilder
import pyaudio
import numpy as np


CHUNK = 2**11
RATE = 44100

p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK)



lightinput = input('IP Address of your WiZ Light:')
light = wizlight(lightinput)
async def music():
    await light.turn_on(PilotBuilder())
    await light.turn_on(PilotBuilder(brightness = 1))

    for i in range (int(10*44100/1024)): #go for a few seconds
        data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
        peak = np.average(np.abs(data))*2
        bars = "#"*int(50*peak/2**16)
        r = 0
        g = 0
        b = 0
        if (peak <= 5000 / 6):
            r = 245
            g = peak / 5000 * 179 + 66
            b = 66
        elif (peak <= 5000 / 6 * 2):
            r = peak / 5000 * 179 + 66
            g = 245
            b = 66
        elif (peak <= 5000 / 6 * 3):
            r = 66
            g = 245
            b = peak / 5000 * 179 + 66
        elif (peak <= 5000 / 6 * 4):
            r = 66
            g = peak / 5000 * 179 + 66
            b = 245
        elif (peak <= 5000 / 6 * 5):
            r = peak / 5000 * 179 + 66
            g = 245
            b = 66
        elif (peak <= 5000 / 6 * 6):
            r = 245
            g = 66
            b = peak / 5000 * 179 + 66
        r = min(r, 255)
        g = min(g, 255)
        b = min(b, 255)
        #r = min(127.5 + peak/7000 * 255, 254)
        #g = max(127.5 - peak/5500 * 255, 0)
        #b = min(peak/4000 * 255, 254)
        brightlevel = min(peak/7000 * 254, 255)
        #print("%04d %05d %s"%(i,peak,bars))
        #print(bars)
        print(peak)
        await light.turn_on(PilotBuilder(rgb = (r, g, b), brightness = brightlevel))
        print('r value', r)
        print('g value', g)
        print('g value', b)
        print('brightness value', brightlevel)



        #await light.turn_on(PilotBuilder(rgb= (17, 203, 104)))
        #print(peakvalues)



time.sleep(1)
print('Starting now! Uses default microphone input of windows')
loop = asyncio.get_event_loop()
loop.run_until_complete(music())
