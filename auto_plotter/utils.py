import numpy as np
import pandas as pd


class DataLoader:
    '''
    Utility class to read multiple log files from experiments to support
    automatic plotting for each algorithm/technique.
    It works by maintaining a numpy array of 3 dimensions
    of size number of observations x number of datasets/metrics x number of techniques
    '''

    def __init__(self, files, alg_names):
        assert len(alg_names) == len(files)
        assert len(alg_names) == len(set(alg_names)), \
            'algorithm names must be unique'

        self.data = np.dstack([pd.read_csv(f).values for f in files])
        self.alg_names = alg_names

    def __iter__(self):
        return self.data

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    @property
    def shape(self):
        return self.data.shape

    # think about a better name
    @property
    def n_scenarios(self):
        return self.shape[1]

    @property
    def n_algorithms(self):
        return self.shape[2]

    @property
    def algorithms(self):
        return self.alg_names

    def get_algorithm(self, alg):
        if isinstance(alg, int) and alg < self.n_algorithms:
            dim = alg
        elif alg in self.alg_names:
            dim = self.alg_names.index(alg)
        else:
            msg = ('{} must be inside algorithms'
                   'or be a valid dimension in '
                   'the range of 0-{}'.format(alg, self.n_algorithms))
            raise ValueError(msg)

        return self.data[:, :, dim]


