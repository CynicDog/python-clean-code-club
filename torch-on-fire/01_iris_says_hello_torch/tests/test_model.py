import torch
from src.models.mlp import IrisMLP


def test_forward():

    model = IrisMLP()

    x = torch.randn(8, 4)

    y = model(x)

    assert y.shape == (8, 3)
