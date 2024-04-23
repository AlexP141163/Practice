class Hero:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.attack_power = 20

    def attack(self, other):
        """Атака другого героя, уменьшение его здоровья на величину силы атаки атакующего."""
        other.health -= self.attack_power
        print(f"{self.name} attacks {other.name} for {self.attack_power} damage.")

    def is_alive(self):
        """Проверка, жив ли еще герой."""
        return self.health > 0


class Game:
    def __init__(self):
        # Создаем игрока и компьютер как экземпляры класса Hero
        self.player = Hero("Player")
        self.computer = Hero("Computer")

    def start(self):
        """Запуск игры и чередование ходов между игроком и компьютером."""
        turn = 0  # Начинаем с хода игрока

        while self.player.is_alive() and self.computer.is_alive():
            if turn % 2 == 0:  # Ход игрока
                self.player.attack(self.computer)
            else:  # Ход компьютера
                self.computer.attack(self.player)

            # Выводим текущее состояние здоровья обоих героев
            print(
                f"{self.player.name} Health: {self.player.health}, {self.computer.name} Health: {self.computer.health}")

            turn += 1

        # Определяем и объявляем победителя
        if self.player.is_alive():
            print(f"{self.player.name} wins!")
        else:
            print(f"{self.computer.name} wins!")


# Создаем экземпляр игры и начинаем игру
game = Game()
game.start()