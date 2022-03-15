#import Planner
#import Renderer

import Tool
import Plan
import Analyzer

import numpy as np

worldSize = [ 100, 100 ]

blockSize = [ 30, 30 ]

world = np.zeros(shape = worldSize)
world[ 30 : 30 + blockSize[0], 30 : 30 + blockSize[1] ] = np.ones(shape = blockSize)

tool = Tool.Tool(radius = 5)
path = Plan.Plan()

path.edges = {
    ((25, 45), (45, 45)): ((25, 45), (45, 45)),
    ((45, 45), (75, 75)): ((45, 45), (75, 75))
}

path.edge_order = [
    ((25, 45), (45, 45)),
    ((45, 45), (75, 75))
]

analyzer = Analyzer.Analyzer(tool, world)

times = analyzer.getScore(path)

#Renderer.render(times, path)