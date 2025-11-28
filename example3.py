from math import sqrt

class Point:
    def __init__(self, x:float, y:float):
        self._x = x
        self._y = y

    @property
    def x(self) -> float:
        return self._x
    
    @property
    def y(self) -> float:
        return self._y
    
    def __eq__(self, other:"Point") -> bool:
        return self.x == other.x and self.y == other.y
    
    def __lt__(self, other:"Point") -> bool:
        return sqrt(self.x**2 + self.y**2) < sqrt(other.x**2 + other.y**2)

    def __le__(self, other:"Point") -> bool:
        return sqrt(self.x**2 + self.y**2) <= sqrt(other.x**2 + other.y**2)

    def __gt__(self, other:"Point") -> bool:
        return sqrt(self.x**2 + self.y**2) > sqrt(other.x**2 + other.y**2)
    
    def __ge__(self, other:"Point") -> bool:
        return sqrt(self.x**2 + self.y**2) >= sqrt(other.x**2 + other.y**2)    

    def __add__(self, other:"Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __repr__(self) -> str:
        return f"Point(x={self.x}, y={self.y})"
    
class Vector:
    def __init__(self, x, y):
        self.origo = Point(0.0,0.0)
        self.v = Point(x,y)


p1 = Point(1.0,2.0)
p2 = Point(3.5,1.3)

print(p1)
print(p2)
p3 = p1 + p2
print(p3)

p4 = Point(4.5, 3.3)
print(f"{p3==p4=}")
print(f"{p1<p2=}")
print(f"{p1>p2=}")
print(f"{p4>p3=}")
print(f"{p3>=p4=}")