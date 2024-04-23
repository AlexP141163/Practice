class Hero:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.attack_power = 20

    def attack(self, other):
        other.health -= self.attack_power
        print(f"{self.name} атакует {other.name}, нанося {self.attack_power} урона.")

    def is_alive(self):
        return self.health > 0

    import random

    class Game:
        def __init__(self, player, computer):
            self.player = player
            self.computer = computer

        def start(self):
            turn = 0  # 0 - ход игрока, 1 - ход компьютера
            while self.player.is_alive() and self.computer.is_alive():
                if turn == 0:
                    self.player.attack(self.computer)
                    turn = 1
                else:
                    self.computer.attack(self.player)
                    turn = 0
                print(f"Здоровье игрока: {self.player.health}. Здоровье компьютера: {self.computer.health}.\n")
            winner = self.player if self.player.is_alive() else self.computer
            print(f"Игра окончена. Победитель - {winner.name}!")