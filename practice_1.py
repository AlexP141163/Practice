class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def make_sound(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def eat(self):
        print(f"{self.name} is eating.")

class Bird(Animal):
    def make_sound(self):
        print(f"{self.name} says tweet.")

class Mammal(Animal):
    def make_sound(self):
        print(f"{self.name} says roar.")

class Reptile(Animal):
    def make_sound(self):
        print(f"{self.name} says hiss.")

def animal_sound(animals):
    for animal in animals:
        animal.make_sound()

class Zoo:
    def __init__(self):
        self.animals = []
        self.staff = []

    def add_animal(self, animal):
        self.animals.append(animal)

    def add_staff(self, staff_member):
        self.staff.append(staff_member)

    def list_animals(self):
        for animal in self.animals:
            print(f"{animal.name}, {animal.age}")

class ZooKeeper:
    def __init__(self, name):
        self.name = name

    def feed_animal(self, animals):
        for animal in animals:
            print(f"{self.name} is feeding {animal.name}.")

class Veterinarian:
    def __init__(self, name):
        self.name = name

    def heal_animal(self, animal):
        print(f"{self.name} is healing {animal.name}.")

# Пример использования
zoo = Zoo()
zoo.add_animal(Bird("Tweety", 3))
zoo.add_animal(Mammal("Leo", 4))
zoo.add_animal(Reptile("Slither", 2))

zoo_keeper = ZooKeeper("John")
veterinarian = Veterinarian("Lucy")

zoo.add_staff(zoo_keeper)
zoo.add_staff(veterinarian)

animal_sound(zoo.animals)
zoo_keeper.feed_animal(zoo.animals)
veterinarian.heal_animal(zoo.animals[0])