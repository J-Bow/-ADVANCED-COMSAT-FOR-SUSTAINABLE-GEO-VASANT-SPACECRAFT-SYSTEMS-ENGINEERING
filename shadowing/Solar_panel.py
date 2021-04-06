import numpy as np



def cart_to_pol(x, y):
    r = (x**2 + y**2)**0.5
    if y == 0:
        if x > 0:
            theta = np.pi/2
        elif x < 0:
            theta = -np.pi/2
        else:
            theta = 0
    elif y < 0:
        theta = np.arctan(x/y) + np.pi
    else:
        theta = np.arctan(x/y)
    return r, theta 

def pol_to_cart(r, theta):
    x = r*np.sin(theta)
    y = r*np.cos(theta)
    return x, y

class solar_panel():

    def __init__(self, x_pos, y_pos):
        self.r, self.theta = cart_to_pol(x_pos, y_pos)
    
    def update(self, theta):
        self.theta += theta
