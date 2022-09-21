
        
# Add common but missing functions to time module (from redefined/recreated micropython module)
import asyncio
import pygame
import os
import sys

sys.path.append("lib")

import time
import utime

time.ticks_ms = utime.ticks_ms
time.ticks_us = utime.ticks_us
time.ticks_diff = utime.ticks_diff
time.sleep_ms = utime.sleep_ms


# See thumbyGraphics.__init__() for set_mode() call
pygame.init()
pygame.display.set_caption("Thumby game")

# Common overrides to get scripts working in the browsers. This should be prepended to each file in the game

# Re-define the open function to create a directory for a file if it doesn't already exist (mimic MicroPython)
def open(path, mode):
    import builtins
    from pathlib import Path
    
    filename = Path(path)
    filename.parent.mkdir(parents=True, exist_ok=True)

    return builtins.open(path, mode)

os.chdir(sys.path[0])


async def main():
	import time
	import thumby
	# BITMAP: width: 32, height: 32
	# BITMAP: width: 40, height: 20
	logo = bytearray([255,255,63,39,231,231,231,231,231,231,199,7,7,199,7,7,7,31,127,255,255,127,63,31,143,193,225,49,25,25,153,153,249,249,251,243,3,7,143,255,
	           255,227,224,224,231,231,231,231,231,227,225,240,248,255,255,252,240,128,192,240,248,252,254,255,255,255,255,240,240,240,243,243,243,243,241,252,252,254,255,255,
	           9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,9])
	thumby.display.setFPS(60)
	y = 20
	x = 20
	ydir = 'up'
	xdir = 'right'
	while(1):
	    thumby.display.fill(1)
	    print(xdir, ydir, x, y)
	    if y <= 0:
	        ydir = 'down'
	    if y >= 20:
	        ydir = 'up'
	    if x <= 0:
	        xdir = 'right'
	    if x >= 30:
	        xdir = 'left'
	    if ydir == 'down':
	        y += 1
	    if ydir == 'up':
	        y -= 1
	    if xdir == 'left':
	        x -= 1
	    if xdir == 'right':
	        x += 1
	    time.sleep(0.1)
	    thumby.display.blit(logo, x, y, 40, 20, 1, 0, 0)
	    await thumby.display.update()
	    

asyncio.run(main())