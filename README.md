# Veronica - Drone Swarm Simulation

## Overview
Veronica is a **Python-based drone swarm simulation** that integrates **animated drone designs, an interactive radar system, and real-time communication** between drones. The project visualizes how a master drone locates and interacts with its slave drones while simulating realistic communication, including latency and packet loss.

## Features
- **Animated Drone Swarm**: Drones move dynamically across the simulation space.
- **Radar System**: Detects drones within a set range with a sweeping effect.
- **Real-time Communication**: Master drone communicates with nearby drones with latency and packet loss simulation.
- **Interactive Visuals**: Drones change colors based on detection and communication status.

## Technologies Used
- **Python**
- **Pygame** (for visualization and animation)
- **Mathematical Computation** (for movement, detection, and communication modeling)

## Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/your-username/Veronica.git
   cd Veronica
   ```
2. Install dependencies:
   ```sh
   pip install pygame
   ```
3. Run the simulation:
   ```sh
   python veronica.py
   ```

## Usage
- The simulation runs automatically.
- The **master drone** (red) will communicate with **slave drones** (blue) within a set range.
- The **radar system** (green) detects drones as they move.
- Communication lines (yellow) appear when messages are successfully transmitted.

## Future Enhancements
- **Obstacle Avoidance**: Smarter pathfinding for drones.
- **3D Visualization**: Advanced graphical representation.
- **User Controls**: Manual drone navigation.
- **AI-Based Decision Making**: Adaptive drone behavior based on environment.

## License
This project is open-source under the MIT License. Feel free to contribute and enhance Veronica!

---
### Contributors
- **Suhani Verma** - Developer & Designer

Happy Coding! 🚀

