import Config

import numpy as np

class Analyzer:
    def __init__(self, tool, world):
        self.tool = tool
        self.world = world
        
        self.radial_mask = np.zeros(shape = (2 * self.tool.radius, 2 * self.tool.radius))
        self.total_pixels = 0
        for i in range(2 * self.tool.radius):
            for j in range(2 * self.tool.radius):
                if (tool.radius ** 2) <= (i ** 2) + (j ** 2):
                    self.radial_mask[i, j] = 1
                    self.total_pixels += 1
    
    def get_times(self, path):
        times = {}
        
        self.tool.reset(path)
        
        prev_edge = path.get_edge(0)
        prev = np.array(prev_edge[1]) - np.array(prev_edge[0])
        
        times[prev_edge] = self.travel_edge(prev_edge, self.tool)
        
        for i in range(1, path.get_size()):
            current_edge = path.get_edge(i)
            current = np.array(current_edge[1]) - np.array(current_edge[0])
            
            alignment = np.dot(current, prev) / (np.linalg.norm(current) * np.linalg.norm(prev))
            
            times[current_edge] = self.travel_edge(current_edge, self.tool)
            
            if alignment < 0.8:
                self.tool.speed = 0
            
            prev_edge = current_edge
            
        return times
            
    def travel_edge(self, edge, tool):
        travel_times = 0
        
        start = edge[0]
        end = edge[1]
        
        edge_samples = self.get_edge_samples(tool, start, end, 10)
        
        for i in range(0, len(edge_samples) - 1):
            sample_now = edge_samples[i]
            sample_next = edge_samples[i + 1]
            
            sample_now = np.array(sample_now)
            sample_next = np.array(sample_next)
            
            tool_engagement_now = self.count_tool_engagements(sample_now)
            tool_engagement_next = self.count_tool_engagements(sample_next)
            
            ratio_now = tool_engagement_now / self.total_pixels
            ratio_next = tool_engagement_next / self.total_pixels
            
            ratio = (ratio_now + ratio_next) / 2

            d = np.linalg.norm(sample_now - sample_next)
            
            acceleration = Config.MAX_ACCELERATION * ratio 
            
            tool.speed += acceleration
            
            if tool.speed > Config.MAX_SPEED:
                tool.speed = Config.MAX_SPEED
            
            travel_times[(sample_now, sample_next)] += d / tool.speed
        
        return travel_times
    
    def count_tool_engagements(self, position):

        voxels = self.world[ 
            int(position[0] - self.tool.radius) : int(position[0] + self.tool.radius), 
            int(position[1] - self.tool.radius) : int(position[1] + self.tool.radius)
        ]
        
        voxels = np.multiply(voxels, self.radial_mask)
        
        return np.sum(voxels)
    
    def get_edge_samples(self, tool, start, end, sample_count):
        samples = []
        
        startY = start[0]
        startX = start[1]
        endY = end[0]
        endX = end[1]
        
        deltaY = endY - startY
        deltaX = endX - startX
        
        offsetY = end[0] - deltaY
        offsetX = end[1] - deltaX
        
        for i in range(sample_count + 1,):
            t = i / sample_count
            
            y = (deltaY * t) + offsetY
            x = (deltaX * t) + offsetX
            
            samples.append((y, x))
            
        return samples
    
    