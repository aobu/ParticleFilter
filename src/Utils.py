import numpy as np

def GenerateRandomMovementVector(MaxDiscplacement: int) -> np.ndarray:
    dx = np.random.randint(-MaxDiscplacement, MaxDiscplacement + 1)
    dy = np.random.randint(-MaxDiscplacement, MaxDiscplacement + 1)
    return np.array([dx, dy])