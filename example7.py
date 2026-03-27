from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x:int
    y:int

@dataclass(frozen=True)
class Vector:
    p1:Point
    p2:Point


@dataclass
class Base:
    base:list[Vector] = []


p1 = Point(1,2)
p1.x = 3
p2 = Point(-1,1)
p3 = Point(0,0)
p4 = Point(3,-2)
p5 = Point(1,2)

print(p1, p2, p3, p4)
print(f"{p1==p2=}")
print(f"{p1==p5=}")


