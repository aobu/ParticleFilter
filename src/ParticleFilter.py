from src.Drone import Drone
from src import Utils
import cv2 as cv2
import numpy as np
from copy import deepcopy
import random


class ParticleFilter:
    def __init__(self, RealDrone: Drone, VirtualDrones: list[Drone], ResampleVariance, NumChannelBins):
        self.RealDrone = RealDrone
        self.VirtualDrones = VirtualDrones
        self.NumVirtualDrones = len(self.VirtualDrones)
        self.ResampleVariance = ResampleVariance
        self.NumChannelBins = NumChannelBins

        self.Weights = [1.0 / self.NumVirtualDrones for _ in range(self.NumVirtualDrones)]

    def CompareSimilarity(self, A, B):
        # Calculate the RGB histograms for each image
        HistA = cv2.calcHist([A], [0, 1, 2], None, [self.NumChannelBins] * 3, [0, 256, 0, 256, 0, 256])
        HistB = cv2.calcHist([B], [0, 1, 2], None, [self.NumChannelBins] * 3, [0, 256, 0, 256, 0, 256])

        # Normalize the histograms
        histA = cv2.normalize(HistA, HistA).flatten()
        histB = cv2.normalize(HistB, HistB).flatten()

        # Calculate the similarity as the correlation between the histograms
        Similarity = cv2.compareHist(histA, histB, cv2.HISTCMP_CORREL)

        return Similarity

    def ComputeWeights(self):
        RealScan = self.RealDrone.Scan()

        MinSimilarity = float('inf')
        MaxSimilarity = float('-inf')

        # First pass: Compute similarities and find min, max
        for i, VirtualDrone in enumerate(self.VirtualDrones):
            VirtualScan = VirtualDrone.Scan()
            Similarity = self.CompareSimilarity(RealScan, VirtualScan)
            self.Weights[i] = Similarity

            if Similarity < MinSimilarity:
                MinSimilarity = Similarity

            if Similarity > MaxSimilarity:
                MaxSimilarity = Similarity

        # Compute the range of similarities
        RangeSimilarity = MaxSimilarity - MinSimilarity

        # Second pass: Rescale weights and square them
        SumSquaredWeights = 0.0
        for i in range(len(self.VirtualDrones)):
            if RangeSimilarity > 0:
                # Linearly rescale the weight to be between 0 and 1
                self.Weights[i] = (self.Weights[i] - MinSimilarity) / RangeSimilarity
            else:
                # Handle the edge case where all similarities are the same
                self.Weights[i] = 1.0

            # Square the rescaled weight
            self.Weights[i] = self.Weights[i] ** 4

            # Accumulate the sum of squared weights
            SumSquaredWeights += self.Weights[i]

        # Normalize the squared weights so they sum to 1
        for i in range(len(self.VirtualDrones)):
            self.Weights[i] /= SumSquaredWeights

    def ResampleVirtualDrones(self):
        # Initialize the resampled drones list
        ResampledDrones = []

        # Number of virtual drones (particles)
        M = self.NumVirtualDrones

        # Compute the random starting point for the resampling wheel
        random_start = np.random.uniform(0, 1 / M)

        # Initialize the cumulative weight
        cumulative_weight = self.Weights[0]

        # Index of the current particle
        i = 0

        # Systematically loop over each particle index
        for m in range(M):
            U = random_start + m / M

            # Move along the cumulative weight until U is less than the cumulative weight
            while U > cumulative_weight:
                i += 1
                cumulative_weight += self.Weights[i]

            # Add the selected particle (deepcopy to avoid reference issues)
            ResampledDrones.append(deepcopy(self.VirtualDrones[i]))

        # Update the list of virtual drones with the resampled drones
        self.VirtualDrones = ResampledDrones

        # Apply a small random movement to each resampled drone
        for VirtualDrone in self.VirtualDrones:
            ResampleVarianceVector = Utils.GenerateRandomMovementVector(self.ResampleVariance)
            VirtualDrone.Move(ResampleVarianceVector)

    def CullParticles(self, Cutoff=0.5):
        # Sort the drones based on weights only, in descending order
        SortedDrones = sorted(zip(self.Weights, self.VirtualDrones), key=lambda x: x[0], reverse=True)

        # Determine the cutoff index
        cutoff_index = int(len(SortedDrones) * Cutoff)

        # Keep only the top Cutoff proportion of items
        CulledDrones = SortedDrones[:cutoff_index]

        # Unzip the culled drones back into weights and drones
        self.Weights, self.VirtualDrones = zip(*CulledDrones)

        # Convert them back to lists (if they need to remain lists)
        self.Weights = list(self.Weights)
        self.VirtualDrones = list(self.VirtualDrones)

        l = len(self.VirtualDrones)

        # Resample to match the number of virtual drones
        while len(self.VirtualDrones) < self.NumVirtualDrones:
            # Randomly choose an index from the existing drones
            idx = random.randint(0, len(self.VirtualDrones) - 1)
            # Append the chosen drone and its weight to the list
            self.VirtualDrones.append(deepcopy(self.VirtualDrones[idx]))
            self.Weights.append(self.Weights[idx])

        # Optionally, normalize weights if needed
        total_weight = sum(self.Weights)
        if total_weight > 0:
            self.Weights = [w / total_weight for w in self.Weights]

        # Apply a small random movement to each resampled drone
        for VirtualDrone in self.VirtualDrones[l:]:
            ResampleVarianceVector = Utils.GenerateRandomMovementVector(self.ResampleVariance)
            VirtualDrone.Move(ResampleVarianceVector)

    def EstimatePosition(self):

        # Initialize an array to sum the positions
        TotalPosition = np.array([0, 0])

        # Sum up all the drone positions
        for VD in self.VirtualDrones:
            TotalPosition += VD.Position

        # Calculate the average position
        MeanPosition = TotalPosition / self.NumVirtualDrones

        return MeanPosition



