import numpy as np
from scipy.interpolate import CubicSpline

def cubic_splane_interpol(x, y):
    cs = CubicSpline(x, y)
    return cs