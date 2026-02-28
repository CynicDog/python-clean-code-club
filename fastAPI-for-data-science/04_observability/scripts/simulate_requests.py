import time
import random
import math
import requests

URL = "http://localhost:8000/iris/predict"


def generate_drifting_iris(seconds_elapsed):
    """
    Simulates a 10-minute drift cycle.
    The drift subtly shifts the mean of the features over time.
    """
    # Base species profiles
    profiles = [
        {"name": "setosa", "base": [5.0, 3.4, 1.5, 0.2]},
        {"name": "versicolor", "base": [5.9, 2.7, 4.2, 1.3]},
        {"name": "virginica", "base": [6.5, 3.0, 5.5, 2.0]}
    ]

    selected = random.choice(profiles)

    drift_magnitude = 0.15 * math.sin(2 * math.pi * seconds_elapsed / 600)

    features = []
    for val in selected["base"]:
        drifted_val = val * (1 + drift_magnitude)
        noise = random.uniform(-0.1, 0.1)
        features.append(round(drifted_val + noise, 2))

    return {"features": features}, selected["name"]


def run_load():
    print(f"Starting load test on {URL}")
    print("Drift cycle: 10 minutes | Max Deviation: 15%")

    start_time = time.time()
    count = 0

    while True:
        try:
            elapsed = time.time() - start_time
            payload, actual_species = generate_drifting_iris(elapsed)

            response = requests.post(URL, json=payload, timeout=2)

            if response.status_code == 200:
                predicted = response.json()["predict"]["species"]
                status = "MATCH" if predicted == actual_species else "MISMATCH"
                print(
                    f"[{count:04d}] {status} | Target: {actual_species:10} | Pred: {predicted:10} | Features: {payload['features']}")
            else:
                print(f"Status Error: {response.status_code}")

            count += 1
            time.sleep(random.uniform(0.2, 0.8))

        except KeyboardInterrupt:
            print("\nLoad test stopped.")
            break
        except Exception as e:
            print(f"Request failed: {e}")
            time.sleep(2)


if __name__ == "__main__":
    run_load()