import os
from dataclasses import dataclass


@dataclass
class Config:
    batch_size: int = 64
    epochs: int = 20
    lr: float = 1e-3
    input_dim: int = 4
    num_classes: int = 3
    dataset_size: int = 100_000

    def __post_init__(self):

        self.batch_size = int(os.getenv("BATCH_SIZE", self.batch_size))
        self.epochs = int(os.getenv("EPOCHS", self.epochs))
        self.lr = float(os.getenv("LR", self.lr))
        self.dataset_size = int(os.getenv("DATASET_SIZE", self.dataset_size))
