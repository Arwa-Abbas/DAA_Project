import random
import os

os.makedirs("closest_inputs", exist_ok=True)

for i in range(1, 11):
    filename = f"closest_inputs/closest_input_{i}.txt"
    with open(filename, "w") as f:
        n = random.randint(100, 300)   # at least 100 points
        f.write(str(n) + "\n")
        for _ in range(n):
            x = random.randint(0, 1000)
            y = random.randint(0, 1000)
            f.write(f"{x} {y}\n")
    print(f"Created {filename} with {n} points.")
