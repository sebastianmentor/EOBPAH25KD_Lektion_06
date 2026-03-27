from typing import Any

class Box:
    def __init__(self, content:Any):
        self.content = content
    
    def __str__(self) -> str:
        return f"The box contains this stuff: {self.content}"
    
    def __repr__(self):
        return f"Box({self.content})"
    
    def __add__(self, other:"Box") -> "Box":
        if not isinstance(other, Box):
            raise TypeError(f"Addition is not suported for {type(other)} and box!")
        
        return Box([other.content, self.content])


box1 = Box("Hejsan du där!")
box2 = Box([1,2,3,4])
box3 = Box(Box({1:"Hej", 2:"då"}))

print(box1)
print(repr(box1))
print(box2)
print(box3)

new_box1 = box1 + box2
new_box2 = box1 + box3

print(new_box1)
print(new_box2)
