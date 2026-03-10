import torch
from torch.utils.data import Dataset
from sklearn.datasets import load_iris
import numpy as np


class IrisDataset(Dataset):

    def __init__(self, size=100000):
        iris = load_iris()
        X = iris.data
        y = iris.target

        repeats = size // len(X) + 1

        X = np.tile(X, (repeats, 1))[:size]
        y = np.tile(y, repeats)[:size]

        noise = np.random.normal(0, 0.2, X.shape)
        X = X + noise

        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.long)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]