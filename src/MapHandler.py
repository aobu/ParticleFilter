import cv2
import numpy as np

class Map:
    def __init__(self, path):
        self.Image = cv2.imread(path)
        if self.Image is None:
            raise ValueError(f"Image at path '{path}' could not be loaded.")
        self.Height, self.Width = self.Image.shape[:2]

    def GetMapImage(self):
        return self.Image

    def GetScan(self, Position: np.ndarray, ScanSize: int):
        x, y = Position.astype(int)
        # Check if the scan coordinates are within bounds
        if x < 0 or y < 0 or x + ScanSize > self.Width or y + ScanSize > self.Height:
            raise ValueError("Scan coordinates are out of bounds")
        # Return the scanned portion of the image
        Scan = self.Image[y:y + ScanSize, x:x + ScanSize]
        return Scan
