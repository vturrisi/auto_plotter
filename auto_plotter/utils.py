import numpy as np
import pandas as pd


class DataLoader:
    def __init__(self, files):
        self.data = np.dstack([pd.read_csv(f).values for f in files])

    def __iter__(self):
        return self.data

    def __getitem__(self, v):
        return self.data[v]

    @property
    def shape(self):
        return self.data.shape
