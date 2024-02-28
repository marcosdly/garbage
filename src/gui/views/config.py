import tkinter as t
from src.gui.views.view import View
from src.gui.config.character_select import CharacterSelect


class ConfigView(View):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.player = CharacterSelect(self, "Identificar Jogador", "player.png")
        self.enemy = CharacterSelect(self, "Identificar Inimigo", "main_enemy.png")
        self.player.grid(column=0, row=0)
        self.enemy.grid(column=1, row=0)
