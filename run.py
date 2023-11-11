from Coche import mesa, trackModel, crashAgent, carAgent
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from mesa.visualization.modules import ChartModule


def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}
    if isinstance(agent, carAgent):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
    elif isinstance(agent, crashAgent):
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    return portrayal



grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)

chart = mesa.visualization.ChartModule([{"Label":"Choques","Color":"Blue"}],data_collector_name="datacollector")

server = mesa.visualization.ModularServer(trackModel,
                       [grid,chart],
                       "Track Model",
                       {"N":10, "width":10, "height":10})
server.port = 8521 # The default
server.launch()

