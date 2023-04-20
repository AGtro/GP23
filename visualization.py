from vpython import *
import numpy as np
from cube import *
import time
from vpython.no_notebook import *
import os
import signal

def get_color(iterations, frequency):
    if frequency < iterations/1000:
        return 0
    elif frequency < iterations/500:
        return 1        
    elif frequency < iterations/400:
        return 2        
    elif frequency < iterations/300:
        return 3        
    elif frequency < iterations/200:
        return 4        
    elif frequency < iterations/100:
        return 5        
    else:
        return 6        

class cube_visualized():
    def __init__(self, grid, cube, agents_array):
        self.grid_size = grid
        self.cube_size = cube
        self.cubes = np.empty((grid, grid, grid), dtype=object)
        
        for agent in agents_array:
            self.add_box(agent)
        agents_array[0].box.color = color.purple
        agents_array[0].box.trail_color = color.purple
        agents_array[1].box.color = color.blue
        agents_array[1].box.trail_color = color.blue
    
    def add_box(self, agent):
        agent.box = box(pos=vector((agent.position[0]-1)+self.cube_size/2, (agent.position[2]-1)+self.cube_size/2, (self.grid_size-agent.position[1])+self.cube_size/2), 
            size=vector(self.cube_size*.25, self.cube_size*.5, self.cube_size*.25), color=color.white, opacity=1, emissive=True, make_trail=True, retain=10)

    def generate_heatmap(self, frequencies, iterations):
        colors = [vector(0,1,0), vector(.2,1,0), vector(.5,.80,0), vector(0.75,.50,0), vector(.75,.25,0), vector(1,.50,0), vector(1,0,0)]
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                for z in range(self.grid_size):
                    color_val = colors[get_color(iterations, frequencies[x,z,self.cube_size-(y+1)])]
                    self.cubes[x,y,z] = box(pos=vector(x+self.cube_size/2, (y+self.cube_size/2)*1.5, z+self.cube_size/2), 
                        size=vector(self.cube_size, self.cube_size, self.cube_size),
                        color = color_val,
                        opacity = .5, emissive = True)
        
        scene.center = vector(self.grid_size/2, (self.grid_size/2)*1.5, self.grid_size/2)

    
    def draw_cubes(self, pickups, dropoffs, risks):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                for z in range(self.grid_size):
                    self.cubes[x,y,z] = box(pos=vector(x+self.cube_size/2, y+self.cube_size/2, z+self.cube_size/2), 
                        size=vector(self.cube_size, self.cube_size, self.cube_size), color=color.white, opacity=.25, emissive=True)
        
        for pickup in pickups:
            self.cubes[pickup[0]-1, pickup[2]-1, self.grid_size-(pickup[1])].color = color.blue

        for dropoff in dropoffs:
            self.cubes[dropoff[0]-1, dropoff[2]-1, self.grid_size-(dropoff[1])].color = color.green

        for risk in risks:
            self.cubes[risk[0]-1, risk[2]-1, self.grid_size-(risk[1])].color = color.red

        scene.center = vector(self.grid_size/2, self.grid_size/2, self.grid_size/2)

    def draw_agents(self, agents_array):
        for agent in agents_array:
            agent.box.pos = vector((agent.position[0]-1)+self.cube_size/2, (agent.position[2]-1)+self.cube_size/2, (self.grid_size-agent.position[1])+self.cube_size/2)

    def invisible(self, agents_array):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                for z in range(self.grid_size):
                    self.cubes[x,y,z].visible = False
        for agent in agents_array:
            agent.box.visible = False

def done():
    os.kill(os.getpid(), signal.SIGINT)    

# makeAgent('x', (1, 1, 1), PEXPLOIT)
# makeAgent('y', (2, 3, 3), PEXPLOIT)

# cube = cube_visualized(3, 1, list(agents.values()))
# cube.draw_cubes([(2, 2, 1), (3, 3, 2)], [(1, 1, 2), (1, 1, 3), (3, 1, 1), (3, 2, 3)], [(2, 2, 2), (3, 2, 1)])

# time.sleep(3)

# agents['x'].position = (3, 3, 3)
# cube.draw_agents(agents.values())
# (iterations/2)/((iterations/2)-frequencies[x,z,self.cube_size-(y+1)])