
class Tool:
    def __init__(self, radius):
        self.radius = radius
        
        self.speed = 0
        
    def reset(self, path):
        self.speed = 0
        
    def accelerate(self, speed):
        self.speed += speed
        
    def setSpeed(self, speed):
        self.speed = speed