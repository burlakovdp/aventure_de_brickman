<div align="center">
<img alt="Preview" src="readme/logo_aventure_de_brickman.jpg" width=100% />
</div>

# Aventure de Brickman : Les Labyrinthes des Redmans

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white) ![Tkinter](https://img.shields.io/badge/Tkinter-GUI-3776AB?style=for-the-badge&logo=python&logoColor=yellow) ![PNM](https://img.shields.io/badge/PNM-Custom_Lib-orange?style=for-the-badge) ![OS](https://img.shields.io/badge/OS-Windows_|_macOS_|_Linux-9cf?style=for-the-badge&logo=linux&logoColor=white) ![UCA](https://img.shields.io/badge/Univ-Côte_d'Azur-007EC7?style=for-the-badge&logo=academic-cap&logoColor=white)

**Student Project - 1st Year Computer Science Bachelor (L1)**
**Université Côte d'Azur**

## Overview
This project is a 2D arcade game developed in **Python** as part of my first semester of studies.

The player controls **Brickman**, a hero who must escape a series of mazes, survive against the **Redmans**, and defeat their leader, the **Redman Chief** (The Boss).

## Tools and Libraries
The game was developed under the following academic constraints:
* **Language:** Python 3
* **GUI:** `Tkinter` (standard library)
* **Image Processing:** `pnm.py` module (provided by Mr. Olivier Baldellon) for handling images and matrices.

## Features

* **Maze Exploration:** Navigation through multiple dynamically loaded levels.
* **Combat System:**
    * Health (HP) management.
    * Bomb planting mechanic to defeat the Boss.
* **"Limbo" Mechanic:** When the player loses all health, they are sent to Limbo and must find the exit to resurrect.
* **Final Boss:** A strategic fight against a boss with specific movement patterns and a dedicated health bar.
* **Matrix Handling:** Uses the `pnm` library (provided by Olivier Baldellon) to manipulate matrices and load image files (.ppm, .pbm).

## Prerequisites

To run this project, you need:

* **Python 3.x** installed on your machine.
* The **Tkinter** standard library (usually included with Python).

## Installation and Launch

1.  Clone this repository (or download the files):
    ````bash
    git clone https://github.com/burlakovdp/aventure_de_brickman.git

    cd aventure_de_brickman
    
2.  Ensure all resource files (folders `interface`, `cartes`, `donnees`, `limbo`) and the `pnm.py` module are present in the root directory.

3.  Run the game:
    ```bash
    python main.py

## Controls

| Key | Action |
| :--- | :--- |
| **Up Arrow (↑)** | Move Up |
| **Down Arrow (↓)** | Move Down |
| **Left Arrow (←)** | Move Left |
| **Right Arrow (→)** | Move Right |
| **Spacebar** | Plant a Bomb (Boss Level only) |

## Project Structure

* `main.py`: The entry point of the game and the main loop.
* `pnm.py`: Utility module for matrix and image file management (provided by Mr. Olivier Baldellon).
* `/cartes`: Contains `.pbm` files representing the level architecture.
* `/donnees`: `.txt` files containing object and enemy positions.
* `/interface`: Sprites and graphical elements (logo, menu, textures).

## Author

Project created by **Danyil-Polina Burlakov** as part of the **1st Year Computer Science Bachelor (L1)** at **Université Côte d'Azur**.
