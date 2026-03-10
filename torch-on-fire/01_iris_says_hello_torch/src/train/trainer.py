import torch
from torch.utils.data import DataLoader
from src.data.dataset import IrisDataset
from src.models.mlp import IrisMLP


def train(cfg):

    dataset = IrisDataset(size=cfg.dataset_size)
    loader = DataLoader(dataset, batch_size=cfg.batch_size, shuffle=True)

    model = IrisMLP(cfg.input_dim, cfg.num_classes)

    optimizer = torch.optim.Adam(model.parameters(), lr=cfg.lr)
    criterion = torch.nn.CrossEntropyLoss()

    for epoch in range(cfg.epochs):
        total_loss = 0

        for X, y in loader:
            optimizer.zero_grad()

            logits = model(X)
            loss = criterion(logits, y)

            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"Epoch {epoch} Loss {total_loss:.4f}")

    torch.save(model.state_dict(), "artifacts/model.pt")
