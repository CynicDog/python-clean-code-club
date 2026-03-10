import torch


def predict(model, features):

    x = torch.tensor(features, dtype=torch.float32)

    if x.ndim == 1:
        x = x.unsqueeze(0)

    with torch.no_grad():
        logits = model(x)

    preds = torch.argmax(logits, dim=1)

    return preds.tolist()