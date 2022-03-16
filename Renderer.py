import Config

import numpy as np
import cv2

def render(times, path, img_scale, worldSize):
    
    canvas = np.ones(shape = (worldSize[1] * img_scale, worldSize[0] * img_scale))
        
    for edge in path.edge_order:
        edge_times = times[edge]
        
        draw_edge(canvas, edge, edge_times, img_scale, worldSize)    

    cv2.imshow("img", canvas)
    cv2.waitKey(0)
            
def draw_edge(canvas, edge, edge_times, img_scale, worldSize):
    p0 = np.array(edge[0]) * img_scale
    p1 = np.array(edge[1]) * img_scale
    
    diff = p1 - p0
    dist = np.linalg.norm(diff)
    
    tip_length = 5
    tip_ratio = tip_length / dist
    
    cv2.arrowedLine(canvas, tuple(p0), tuple(p1), (0, 0, 0), 1, 8, 0, tip_ratio)
    
    t = get_time(edge_times)
    t = "{:.1f}".format(t)
    
    mid = (p0 + p1) / 2
    
    normal = np.array((
        diff[1],
        -diff[0]
    ))
    normal_size = np.linalg.norm(normal)
    
    if normal_size == 0:
        normal = np.zeros(2)
    else:
        normal = normal / normal_size
    
    
    text_pos = mid + (normal * 5)
    text_pos= (int(text_pos[0]), int(text_pos[1]))
    
    cv2.putText(
        img = canvas, 
        text = t, 
        org = text_pos, 
        fontFace = cv2.FONT_HERSHEY_SIMPLEX, 
        fontScale = 1.0,
        color = (0, 0, 0), 
        thickness = 1, 
        lineType = cv2.LINE_AA
    )
    
def get_time(edge_times):
    t = 0
    
    for sub_edge in edge_times:
        t += edge_times[sub_edge]
        
    return t