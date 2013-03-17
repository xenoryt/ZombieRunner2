#! /usr/bin/env python

"""
ScaleClock - Allow your realtime application to self-adjust for fps changes.

There are two general approaches to handling timing issues in a game. The first
is to specify a maximum frame rate, and use pygame.time.delay() to make the length
of each frame as close to the preceeding one as possible. This has the advantage of
simplicity, but it means that a powerful machine will run at the same rate as a
slow one, reducing efficiency - much processor time could be wasted in delay loops.

This example demonstrates the alternative - running at the maximum possible framerate,
then scaling all events to match. This method is more complicated; each moving object
must have its movement rate scaled to compensate for longer or shorter frame durations.
In addition, each recurring event must take into account the length of each frame in
its timer.

Create a timer object, then call timer.begin before your main loop, and timer.tick()
during that loop.  You'll need to handle movement and interval issues as mentioned
above; check the example code at the bottom to see how to do it.
"""

import pygame, sys

class FpsClock:
    def __init__(self):
        self.frame_duration = 0.000
        self.this_frame_time = 0
        self.last_frame_time = 0
        return
    
    def tick(self):
        "Call this every frame"
        self.this_frame_time = self.get_current_time()
        self.frame_duration = (self.this_frame_time - self.last_frame_time) / 1000.000
        self.last_frame_time = self.this_frame_time
        return

    def get_frame_duration(self):
        "Returns the length of the previous frame, in seconds"
        return self.frame_duration

    def get_current_time(self):
        "Used internally. Returns current time in ms."
        return pygame.time.get_ticks()

    def begin(self):
        "Starts/restarts the timer. Call just before your main loop."
        self.last_frame_time = self.get_current_time()
        return
        
if __name__ == "__main__":

    pygame.init()

    timer = FpsClock()

    timer.begin()

    # Object setup for the movement example
    
    display = pygame.display.set_mode((320, 20), pygame.SWSURFACE)

    red_square = pygame.Surface((20, 20), pygame.SWSURFACE)
    red_square.fill((255, 0, 0))
    
    black_square = pygame.Surface((20, 20), pygame.SWSURFACE)
    black_square.fill((0, 0, 0))

    square_speed = 160 
    square_x = 0

    # Setup for the interval example
    
    tick_interval = 1.000
    tick_time = 0

    # Change this to see how different framerates result in consistent
    # motion. Try values like 50 or 200
    
    delay_duration = 5
    
    while 1:
        # Interval example
        
        tick_time += timer.get_frame_duration()
        if tick_time > tick_interval:
            tick_time = 0
            print "Tick"

        # Motion example
            
        display.blit(black_square, (square_x, 0))
        square_x += (square_speed * timer.get_frame_duration())
        if square_x > 320:
            square_x = 0
        display.blit(red_square, (square_x, 0))
        
        pygame.display.update()

        # Insert artificial delay
        
        pygame.time.delay(delay_duration)

        # Must call this every frame
        
        timer.tick()

        # Check for keypress, exit if we get one.
        
        pygame.event.peek()
        keys = pygame.key.get_pressed()
        for key in keys:
            if key:
                sys.exit()




        
