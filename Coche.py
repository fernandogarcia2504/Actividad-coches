import mesa
import seaborn as sns
import numpy as np
import pandas as pd

class crashAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        print(f"Crash spot created {str(self.unique_id)}.") 


class carAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        print(f"Car agent created {str(self.unique_id)}.")
    

    def see(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for cellmate in cellmates:
            if isinstance(cellmate, crashAgent):
                print(f'Crash detected at {self.pos}. Stopping car agent {self.unique_id}.')
                self.model.schedule.remove(self)
    def move(self):
        print(f"Agent {self.unique_id} moving from {self.pos} to ...")  

        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        possible_steps = [step for step in possible_steps if step[1] > self.pos[1]]
        if possible_steps:
            new_position = self.random.choice(possible_steps)
            self.model.grid.move_agent(self, new_position)
            if new_position[1] == self.model.grid_height:
                self.pos = (self.pos[0]) 

    def step(self):    
        self.move()
        self.see()
        


class trackModel(mesa.Model):
    def __init__(self, N, width, height):
        self.grid = mesa.space.MultiGrid(width, height, False)
        self.num_agents = N
        self.grid_width = width
        self.grid_height = height
        self.schedule = mesa.time.RandomActivation(self)

        self.crash_events = 0
        self.car_crash_events = []

        self.datacollector = mesa.datacollection.DataCollector(
            agent_reporters={"Position": "pos"},
            model_reporters ={"Crash_events":"crash_events"}
        )


        for i in range(self.num_agents):
            a = carAgent(i + 1, self)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.grid_height -10
            self.grid.place_agent(a, (x, y))

            if i % 2 == 0:  
                crash_x, crash_y = self.random.randrange(self.grid_width), self.random.randrange(self.grid_height)
                while (crash_x, crash_y) == (x, y):
                    crash_x, crash_y = self.random.randrange(self.grid_width), self.random.randrange(self.grid_height)
                    
                c = crashAgent(-1 - i, self)
                self.schedule.add(c)
                self.grid.place_agent(c, (crash_x, crash_y))

    
    def detect_collision(self):
        for agent in self.schedule.agents:
            if isinstance(agent, carAgent):
                cellmates = self.grid.get_cell_list_contents([agent.pos])
                for cellmate in cellmates:
                    if isinstance(cellmate, crashAgent):
                        print(f'Car {agent.unique_id} collided with crash at {agent.pos}.')
                        self.crash_events += 1
                        self.car_crash_events.append(self.schedule.time)


    def step(self):
        print("Step:", self.schedule.time)

        self.schedule.step()

        for agent in self.schedule.agents:
            if isinstance(agent, carAgent) and agent.pos[1] == self.grid_height:
                agent.pos = (agent.pos[0], 0)

        self.detect_collision()
        self.datacollector.collect(self)