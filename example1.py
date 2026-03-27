import random

class IdentityMixin:
    def __init__(self, id):
        self.id = id

class Vehicle:
    def __init__(self, number_of_wheels:int = 2):
        self.number_of_wheels = number_of_wheels

    def print_number_of_wheels(self) -> None:
        print(f"I have {self.number_of_wheels} number of wheels!")

class Bicicle(Vehicle):
    def __init__(self, number_of_wheels = 2):
        super().__init__(number_of_wheels)

class Car(Vehicle, IdentityMixin):
    modell = "Volvo"
    def __init__(self):
        Vehicle.__init__(self, 4)
        IdentityMixin.__init__(self, random.randint(100000, 999999))
        self.modell = "Saab"

# b = Bicicle()
# my_bicalcle_number_of_wheel_printer = b.print_number_of_wheels
# b.number_of_wheels = 9
# my_bicalcle_number_of_wheel_printer()

# car1 = Car()
# car1.print_number_of_wheels()

# print(Car.modell)
# print(f"{car1.modell=}, {car1.__dict__}")
# car1.color = "Blue"
# print(f"{car1.color=}, {car1.__dict__}")

# print(f"{isinstance(car1, Vehicle)=}")
# print(f"{issubclass(car1.__class__, Vehicle)=}")

# print(f"{isinstance(b, IdentityMixin)=}")


class A:
    def __init__(self,*args, **kwags):
        print("A init")
        self.value_a = kwags.get("a", None)
        super().__init__(kwags)

class B:
    def __init__(self, *args, **kwags):
        print("B init")
        self.value_b  = kwags.get("b", None)
        super().__init__(kwags)

class D:
    def __init__(self, *args, **kwags):
        print("D init")
        self.value_d = kwags.get("d", None)
        super().__init__(kwags)

class C(A, D, B):
    def __init__(self,*args, **kwags):
        # A.__init__(self, kwags)
        # D.__init__(self, kwags)
        # B.__init__(self, kwags)
        self.value_c = kwags.get("c", None)
        print("C init")
        super().__init__(kwags)


obj = C(d="hej", a="banan", b="sist")

# l = [1,2,3,4]

# first, *rest = l
# print(first, rest)