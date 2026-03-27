from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

class Square(Shape):
    def __init__(self, s:int|float):
        self.s:float = float(s)

    def area(self) -> float:
        return self.s * self.s
  
class Triangle(Shape):
    def __init__(self,b:int|float,h:int|float):
        self.b:float = float(b)
        self.h:float = float(h)

    def area(self) -> float:
        return (self.b*self.h)/2



sq = Square(3)
print(isinstance(sq, Shape))
print(sq.area())
tri = Triangle(5,4)
print(tri)
print(tri.area())