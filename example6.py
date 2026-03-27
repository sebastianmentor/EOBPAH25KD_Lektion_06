class Bird:
    def eat(self):
        print("Bird is eating bird seeds!!")

class Human:
    def eat(self):
        print("Human is eating good burgure!")

class CarPress:
    def eat(self):
        print("Car Press is eating car, num num num!")

class Flower():
    def drink(self):
        print("Drinking water!!!")

def apply_eat(list_of_eaters:list):
    for eater in list_of_eaters:
        eater.eat()


b1 = Bird()
b2 = Bird()
h1 = Human()
c1 = CarPress()
c2 = CarPress()
f1 = Flower()

eaters = [b1, h1, c1, b2, c2, f1]

apply_eat(eaters)