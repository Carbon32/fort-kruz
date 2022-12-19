# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon                              #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *
from src.button import *

# User Interface: #

class UserInterface():
    def __init__(self, game):

        # Game:

        self.game = game

        # Buttons:

        self.button_repair = ButtonImage(self.game.display, self.game.screen_width - self.game.screen_width // 16, self.game.screen_height // 2 - self.game.screen_height // 4, self.game.load_game_image('assets/buttons/repair.png', int((self.game.screen_width // 4) * 0.19), int((self.game.screen_height // 2) * 0.17)))
        self.button_armour = ButtonImage(self.game.display, self.game.screen_width - self.game.screen_width // 16, self.game.screen_height // 2 - self.game.screen_height // 6, self.game.load_game_image('assets/buttons/armour.png', int((self.game.screen_width // 4) * 0.19), int((self.game.screen_height // 2) * 0.17)))
        self.button_tower = ButtonImage(self.game.display, self.game.screen_width - self.game.screen_width // 16, self.game.screen_height // 2 - self.game.screen_height // 12, self.game.load_game_image('assets/buttons/tower.png', int((self.game.screen_width // 4) * 0.19), int((self.game.screen_height // 2) * 0.17)))
        self.button_balls = ButtonImage(self.game.display, self.game.screen_width - self.game.screen_width // 16, self.game.screen_height - self.game.screen_height// 2, self.game.load_game_image('assets/buttons/add_balls.png', int((self.game.screen_width // 4) * 0.19), int((self.game.screen_height // 2) * 0.17)))
        self.button_ball_type = ButtonImage(self.game.display, self.game.screen_width - self.game.screen_width // 16, self.game.screen_height // 2 - self.game.screen_height // 3, self.game.load_game_image('assets/buttons/ball_type.png', int((self.game.screen_width // 4) * 0.19), int((self.game.screen_height // 2) * 0.17)))

        # User Interface Container: 

        self.container = self.game.load_game_image("assets/ui.png", self.game.screen_width // 2, self.game.screen_height - self.game.screen_height // 3)

    def show_stats(self, fort):
        text_size = 1 * (self.game.screen_height // 54)
        self.game.display.blit(self.container, (self.game.screen_width // 2, 0))
        self.game.draw_text('Coins: ' + str(self.game.coins), text_size, (69, 69, 69), self.game.screen_width // 2 + self.game.screen_width // 4, 10)
        self.game.draw_text('Cannon Balls: ' + str(fort.current_balls) + "/" + str(self.game.available_balls), text_size, (69, 69, 69), self.game.screen_width // 2 + self.game.screen_width // 3, 10)
        self.game.draw_text('Score: ' + str(self.game.kills), text_size, (69, 69, 69), self.game.screen_width // 2 + self.game.screen_width // 14, 10)
        self.game.draw_text('Level: ' + str(self.game.level.current_level), text_size, (69, 69, 69), self.game.screen_width // 2 + self.game.screen_width // 7, 10)
        self.game.draw_text('500c', text_size, (69, 69, 69), self.game.screen_width - self.game.screen_width // 11, self.game.screen_height // 2 - self.game.screen_height // 5)
        self.game.draw_text('5,000c (' + str(self.game.ball_type) + "/" + str(self.game.total_balls) + ")", text_size, (69, 69, 69), self.game.screen_width - self.game.screen_width // 7, self.game.screen_height // 2 - self.game.screen_height // 5 - self.game.screen_height // 11)
        self.game.draw_text('250c (5b)', text_size, (69, 69, 69), self.game.screen_width - self.game.screen_width // 8, 5 * (self.game.screen_height // 9))
        self.game.draw_text('1,000c', text_size, (69, 69, 69), self.game.screen_width - self.game.screen_width // 10, self.game.screen_height // 2 - self.game.screen_height // 8)
        self.game.draw_text('2,000c (Max: 2)', text_size - 2, (69, 69, 69), self.game.screen_width - self.game.screen_width // 7, self.game.screen_height // 2 - self.game.screen_height // 24)