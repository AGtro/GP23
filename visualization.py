from vpython import *
import numpy as np

class agent():
    position = vector(0,0,0)

class cube_visualized():
    def __init__(self, grid, cube, num_agents):
        self.grid_size = grid
        self.cube_size = cube
        self.cubes = np.empty((grid, grid, grid), dtype=object)
        self.agents = np.empty((num_agents), dtype=agent)
    
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
        
        box(pos=vector(0+self.cube_size/2, 0+self.cube_size/2, 2+self.cube_size/2), 
            size=vector(self.cube_size*.25, self.cube_size*.5, self.cube_size*.25), color=color.blue, opacity=1, emissive=True)
        
        box(pos=vector(1+self.cube_size/2, 2+self.cube_size/2, 0+self.cube_size/2), 
            size=vector(self.cube_size*.25, self.cube_size*.5, self.cube_size*.25), color=color.purple, opacity=1, emissive=True)

        scene.center = vector(self.grid_size/2, self.grid_size/2, self.grid_size/2)

    def draw_agents(self):
        for agent in self.agents:
            pass


cube = cube_visualized(3, 1, 2)
cube.draw_cubes([(2, 2, 1), (3, 3, 2)], [(1, 1, 2), (1, 1, 3), (3, 1, 1), (3, 2, 3)], [(2, 2, 2), (3, 2, 1)])