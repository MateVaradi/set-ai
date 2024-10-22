# Set Recognition with LLM

## Overview

This project uses the OpenAI's GPT-4o model to identify valid sets in photos of the game *SET*.

### What is Set?

*SET* is a card game where each card displays a combination of four attributes: shape, color, number, and shading. A *SET* consists of three cards where, for each attribute, the values are either all the same or all different.

### How it works

1. **Image Input**: The user uploads a photo of a SET game layout.
2. **Preprocessing and Card Recognition**: The image is processed to detect and extract individual cards. GPT-4o is used to describe the cards on the photo.
3. **Set Recognition**: A simple algorithm finds all *SET*s among the cards.
4. **Output**: The recognized sets are highlighted and returned.

### How to use

Simply upload your SET game to: https://set-ai-app-c162aa183dd5.herokuapp.com/

### Example

![set_board_results_3](https://github.com/user-attachments/assets/55e4a888-4efe-4449-b2d6-1fcf532e4cf0)
![set_board_results_2](https://github.com/user-attachments/assets/2905a377-a55c-47c4-b11d-a51a7a4fce1f)
![set_board_results_1](https://github.com/user-attachments/assets/7c5e79a7-114a-4a78-89fe-afd4b6791019)
![set_board_results_0](https://github.com/user-attachments/assets/0845aa69-f1ca-4ef9-a059-6ad60f780b3f)

### License
This project is licensed under the MIT License.
