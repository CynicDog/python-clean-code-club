from src.train.trainer import train
from src.config.config import Config

def main():
    cfg = Config()
    train(cfg)

if __name__ == "__main__":
    main()