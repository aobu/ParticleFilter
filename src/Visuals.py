import cv2
import numpy as np
import imageio

class Visualizer:
    def __init__(self, Map):
        self.Map = Map

    def DisplayImage(self, Image, Title):
        cv2.imshow(Title, Image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def DrawDrones(self, Image, Drones, Color: (int, int, int)=(225, 0, 0), radius=5):
        for Drone in Drones:
            x, y = Drone.Position.astype(int)
            cv2.circle(Image, (x, y), radius=radius, color=Color, thickness=-1)
        return Image

    def DrawDotAtPosition(self, Image, Position: np.ndarray, radius=5):
        x, y = Position.astype(int)
        cv2.circle(Image, (x, y), radius=radius, color=(0, 0, 255), thickness=-1)
        return Image

    def compile_images_to_gif(self, image_list, output_path, duration=1):
        # Convert images from BGR (OpenCV format) to RGB (GIF format)
        rgb_images = [cv2.cvtColor(img, cv2.COLOR_BGR2RGB) for img in image_list]
        imageio.mimwrite(output_path, rgb_images, duration=duration)