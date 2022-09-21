
        
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

    await return builtins.open(path, mode)

os.chdir(sys.path[0])


async def main():
	import random, time, thumby, collections
	
	controls_map = bytearray([224,32,32,32,32,63,1,1,1,1,1,1,1,1,1,63,32,32,32,32,224,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,1,1,1,1,1,1,1,255,
	    255,128,128,128,128,128,0,0,0,0,0,0,0,0,0,128,128,128,128,128,255,0,0,0,0,0,0,0,0,0,252,4,4,4,4,4,4,4,252,0,7,4,4,4,4,4,4,4,7,
	    0,0,0,0,0,31,16,16,16,16,16,16,16,16,16,31,0,0,0,0,0,0,0,0,0,0,0,0,0,0,31,16,16,16,16,16,16,16,31,0,0,0,0,0,0,0,0,0,0])
	controls_sprite = thumby.Sprite(49, 21, controls_map, 10, 10)  # sprite based on Laveréna Wienclaw
	Button = collections.namedtuple("Button", "letter freq x y")
	KEYS = [Button("", 20, 0, 0), Button("A", 7458, 52, 12), Button("B", 7902, 42, 22), Button("U", 10548, 18, 12), Button("R", 8870, 24, 17), Button("D", 7458, 18, 22), Button("L", 7902, 12, 17)]
	
	async def show(val=0, text=["", "", "", "", ""]):
	    thumby.display.fill(0)
	    for index, content in enumerate(text):
	        thumby.display.drawText(content, 0, 8 * index, 1)
	    thumby.display.drawSprite(controls_sprite)
	    thumby.display.drawText(KEYS[val].letter, KEYS[val].x, KEYS[val].y, 1)
	    await thumby.display.update()
	    thumby.audio.playBlocking(KEYS[val].freq, val == 0 or 1000)
	
	async def start():
	    await show(text=["  Tiny Mem!", "", "", "", "  hard;easy"])
	    value_range = (1, 2) if wait_press() < 3 else (3, 6)
	    random.seed(time.ticks_ms())
	    await return 0, [random.randint(*value_range) for i in range(100)]
	
	def wait_press(c=None):
	    while(c is None):
	        c = (thumby.buttonL.justPressed() and 6) or (thumby.buttonD.justPressed() and 5) or (thumby.buttonR.justPressed() and 4) or (thumby.buttonU.justPressed() and 3) or (thumby.buttonB.justPressed() and 2) or (thumby.buttonA.justPressed() and 1) or None
	    await return c
	
	async def turn(max_pos, sequence, current_pos=0):
	    for index, val in enumerate(sequence[:max_pos + 1]):  # await show sequence
	        await show(val=val, text=[f"  key={KEYS[val].letter}", "", "", "", f"  num={index + 1}"])
	    await show(text=["  your await turn", "", "", "", "  repeat"])  # ask sequence
	    while (current_pos <= max_pos):
	        if sequence[current_pos] != wait_press():  # GAME OVER
	            await show(text=["  your mem=", "", "", "", f"  {str(max_pos*(min(sequence) == 1 or 2))} bits"])
	            wait_press()
	            await return await start()
	        current_pos += 1
	        await show(val=sequence[current_pos - 1], text=[f"  {current_pos} done", "", "", "", f"  {max_pos - current_pos + 1} left"])
	    await return max_pos + 1, sequence
	
	max_pos, sequence = await start()
	while(True):
	    max_pos, sequence = await turn(max_pos, sequence)

asyncio.run(main())