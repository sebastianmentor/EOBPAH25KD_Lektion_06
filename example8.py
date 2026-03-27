class Value:
    def __init__(self, v:int):
        self.v = v

    def __add__(self, other:'Value') -> 'Value':
        if isinstance(other, Value):
            return Value(self.v + other.v)

        raise TypeError("Cant be done!")

    def __repr__(self):
        return f"Value({self.v})"
    
v1 = Value(4)
v2 = Value(8)

print(v1.__add__(v2))
print(v1 + v2)