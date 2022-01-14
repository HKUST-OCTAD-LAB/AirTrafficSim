import numpy as np

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.z = z
    
    def get_position(self):
        return x,y,z

    def get_long(self):
        return x

    def get_lat(self):
        return y

    def get_alt(self):
        return z

    def get_distance(self, position):
        return np.sqrt(np.power(position.x-self.x, 2) + np.power(position.y-self.y, 2)\
             + np.power(position.z-self.z, 2))