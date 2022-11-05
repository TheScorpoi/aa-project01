
class Vertex:
    
    def __init__(self, id, point):
        self.id = id
        self.point = point

    def __repr__(self):
        return f"[id={self.id}, point={self.point}]"

if __name__ == "__main__":
    from src.point import Point
    v = Vertex("A", Point(1,2))
    print(v)