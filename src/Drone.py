import numpy as np
from src import Utils


class Drone:
    def __init__(self, Map, ScanSize, DisplacementVariance: int, StartPosition: np.ndarray = None):
        self.Map = Map
        self.ScanSize = ScanSize
        self.DisplacementVariance = DisplacementVariance
        if StartPosition is None:
            MaxX, MaxY = Map.Width - ScanSize, Map.Height - ScanSize
            self.Position = np.array([np.random.randint(0, MaxX), np.random.randint(0, MaxY)])
        else:
            self.Position = StartPosition

    def Scan(self):
        x, y = self.Position.astype(int)
        return self.Map.GetScan(self.Position, self.ScanSize)

    def Move(self, MovementVector: np.ndarray):

        # Calculate new position
        Variation = Utils.GenerateRandomMovementVector(self.DisplacementVariance)
        NewPosition = self.Position + MovementVector + Variation

        # Ensure the new position is within the map boundaries
        MaxX, MaxY = self.Map.Width - self.ScanSize, self.Map.Height - self.ScanSize
        NewPosition[0] = np.clip(NewPosition[0], 0, MaxX)
        NewPosition[1] = np.clip(NewPosition[1], 0, MaxY)

        self.Position = NewPosition
