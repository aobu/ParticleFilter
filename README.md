# Image-Based Particle Filter for Drone Localization

This project is an implementation of an Image-Based Particle Filter for localizing a simulated drone within a known map. The core logic is implemented in Python, with a focus on accurately predicting the drone's position based on visual data from small image scans.

## Features

- **Particle Filter Localization**: Utilizes a particle filter algorithm to estimate the drone's position, leveraging a set of virtual drones that are resampled based on their similarity to the real drone's image scans.
- **Noisy Movement Simulation**: The drone's movements are simulated with noise, mimicking real-world sensor inaccuracies, adding a realistic challenge to the localization process.
- **Image-Based Matching**: Both the real drone and virtual drones take image scans of their environment. The similarity between these scans is used to adjust the likelihood of each particle, driving the resampling process.
- **Convergence Monitoring**: Over multiple iterations, the particles converge to the real drone's position, providing an accurate estimate of its location on the map.

## Methodology

1. **Initialization**:
   - The real drone is initialized at a known starting position.
   - Virtual drones (particles) are initialized at random positions within the map.

2. **Movement**:
   - The real drone moves through the environment, providing noisy measurements of its movements.
   - Virtual drones adjust their positions based on the noisy movement data.

3. **Image Scanning**:
   - The real drone and virtual drones take small image scans of their surroundings.
   - Similarity metric used was Histogram Correlation Comparison.

4. **Resampling**:
   - Particles that more closely match the real drone's scan are given higher weights.
   - A resampling step selects new particles based on these weights, biasing the most likely positions.

5. **Iteration**:
   - The process repeats, refining the particle distribution until it converges on the real drone's location.

## Technical Details

The particle filter is an effective method for localization in uncertain environments. It relies on maintaining and updating a set of hypotheses (particles) about the system's state, which are continuously refined through resampling. In this project, visual data from image scans plays a crucial role in determining the likelihood of each hypothesis.

### Core Concepts:

- **Particles**: Represent possible positions of the drone, each with an associated weight indicating its likelihood.
- **Noisy Measurements**: Simulated noise in the drone's movement to replicate real-world conditions.
- **Image Matching**: Comparison of image scans between the real drone and particles to evaluate similarity.
- **Resampling**: Process of selecting new particles based on their weights, focusing on the most probable locations.
- **Convergence**: The iterative process of particle movement and resampling leads to convergence on the real drone's position.

## Demo

Here is a quick demonstration of the particle filter localization in action:

![Drone Localization Demo 1](/Output/CityMapGif.gif)

![Drone Localization Demo 2](/Output/OtherMapGif.gif)

## References

For more information on particle filters and their applications in localization, you can refer to the following resources:

- [Sebastian Thrun, "Probabilistic Robotics"](http://www.probabilistic-robotics.org/)
- [Wikipedia: Particle Filter](https://en.wikipedia.org/wiki/Particle_filter)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
