
# Tank Reward Game

An exciting and challenging tank battle game created using Pygame. In this game, you control a tank and battle against various obstacles and enemy forces. The game includes a player tank that can shoot bullets, enemies that can fire back, and obstacles that affect gameplay. The goal is to survive as long as possible and achieve a high score.

## Features
- **Player Tank**: Move your tank using arrow keys and shoot with the spacebar.
- **Enemy Bullets**: Enemies shoot back once you reach a certain score level.
- **Obstacles**: Avoid or destroy obstacles on the battlefield.
- **Dynamic Difficulty**: The difficulty increases as your score grows, with faster obstacles and more aggressive enemies.
- **Score Tracking**: Your score increases by shooting obstacles or avoiding damage. The best score is saved.
- **Levels**: Enemies get stronger as the game progresses.

## Controls
- **Arrow Keys**: Move the player tank (up, down, left, right).
- **Spacebar**: Shoot bullets.
- **Esc**: Quit the game during gameplay.
- **Spacebar (on Game Over screen)**: Restart the game.

## Game Mechanics
- **Tank**: Your tank is controlled by arrow keys. It can move in all directions within the game window.
- **Bullets**: Shoot bullets by pressing the spacebar. Bullets move upwards and destroy obstacles or enemies on collision.
- **Enemies**: Enemies appear as obstacles. After a certain score threshold, some obstacles can shoot bullets at the player.
- **Obstacles**: Red rectangular obstacles that move down the screen. Avoid them to stay alive.
- **Levels**: As your score increases, the game gets harder with faster obstacles and enemy bullet speed.
  
## Installation
1. Install Python (version 3.6 or higher).
2. Install Pygame using pip:

   ```bash
   pip install pygame
   ```

3. Download or clone the repository.

4. Run the game script:

   ```bash
   python tank_battle.py
   ```

## Game Over & Restart
- After you lose the game, you can choose to restart or quit.
- If you score higher than your previous best score, it will be saved in a `highscore.txt` file.

## Customization
- The game features adjustable parameters such as tank speed, bullet speed, and enemy difficulty. These can be modified within the script.

## Contributing
Feel free to contribute by forking the repository, making improvements, or fixing bugs. Open a pull request for any changes.

## License
This project is open source and available under the MIT License.
