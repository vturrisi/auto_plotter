import numpy as np
import pandas as pd


class DataLoader:
    '''
    Utility class to read multiple log files from ML experiments to support
    automatic plotting for each algorithm/technique.
    It works by maintaining a numpy array of 3 dimensions
    of size number of observations x number of datasets x number of techniques
    '''

    def __init__(self, files):
        self.data = np.dstack([pd.read_csv(f).values for f in files])

    def __iter__(self):
        return self.data

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    @property
    def shape(self):
        return self.data.shape
