import numpy as np


def calculate_energy(frame):
    return np.sum(frame.astype(np.float64) ** 2)


def calculate_zcr(frame):
    signs = np.sign(frame)
    flips = signs[:-1] != signs[1:]
    return np.sum(flips)/ (len(frame) - 1 )