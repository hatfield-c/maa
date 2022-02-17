import numpy as np
import matplotlib.pyplot as plt

def render(points):
    fig = plt.figure()
    ax = plt.axes(projection = '3d')
    
    ax.scatter(list(points[0]), list(points[1]), list(points[2]))
    
    plt.show()
    
points = [ 
    [ 0, 1, 2 ],
    [ 0, 0, 0 ],
    [ 0, 0, 0 ]
]
render(points)