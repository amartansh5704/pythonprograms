from abc import ABC, abstractmethod
import math

class Shape(ABC):
    
    def __init__(self, color="white"):
        self.color = color
    
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass

    def display_info(self):
        print("=" * 30)
        print(f"Shape: {self.__class__.__name__}")
        print(f"Color: {self.color}")
        print(f"Area: {self.area()}")
        print(f"Perimeter: {self.perimeter()}")
        print("=" * 30)
    
    def is_larger_than(self, other_shape):
        return self.area() > other_shape.area()
    def __str__(self):
        return f"{self.__class__.__name__} Color: {self.color}, Area: {self.area():2f}"

class Circle(Shape):
    def __init__(self, radius, color="white"):
        super().__init__(color)
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius

    def diameter(self):
        return 2 * self.radius

class Rectangle(Shape):
    def __init__(self, width, height, color="white"):
        super().__init__(color)
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def is_square(self):
        return self.width == self.height

class Triangle(Shape):
    def __init__(self, side_a, side_b, side_c, color="white"):
        super().__init__(color)
        self.side_a = side_a
        self.side_b = side_b
        self.side_c = side_c

    def area(self):
        s = (self.side_a + self.side_b + self.side_c) / 2
        return math.sqrt(s * (s - self.side_a) * (s - self.side_b) * (s - self.side_c))
    
    def perimeter(self):
        return self.side_a + self.side_b + self.side_c

    def get_type(self):
        if self.side_a == self.side_b == self.side_c:
            return "Equilateral"
        elif self.side_a == self.side_b or self.side_b == self.side_c or self.side_a == self.side_c:
            return "Isosceles"
        else:
            return "Scalene"

class ShapeCalculator:
    def __init__(self):
        self.shapes = []

    def add_shape(self, shape):
        self.shapes.append(shape)
        print(f"{shape.__class__.__name__} added to the calculator.")
    
    def total_area(self):
        return sum(shape.area() for shape in self.shapes)
    
    def largest_shape(self):
        return max(self.shapes, key=lambda s: s.area())
    
    def smallest_shape(self):
        return min(self.shapes, key=lambda s: s.area())
    
    def show_all_shapes(self):
        print("All Shapes in the Calculator:")
        print("=" * 30)
        for i , shape in enumerate(self.shapes, start=1):
            print(f"{i}. {shape}")
    
print("Shape Calculator")

circle1 = Circle(5, "red")
rectangle1 = Rectangle(5, 10, "blue")
rectangle2 = Rectangle(7, 7, "green")
triangle1 = Triangle(3, 4, 5, "yellow")

circle1.display_info()
rectangle1.display_info()
rectangle2.display_info()
triangle1.display_info()

print("\n Polymorphism Demonstration:")
shapes = [circle1, rectangle1, rectangle2, triangle1]
for shape in shapes:
    print(f"{shape.__class__.__name__} Area: {shape.area():.2f}, Perimeter: {shape.perimeter():.2f}")

print("\n Shape specific methods:")
print(f"Circle Diameter: {circle1.diameter():.2f}")
print(f"Rectangle1 is square: {rectangle1.is_square()}")
print(f"Rectangle2 is square: {rectangle2.is_square()}")
print(f"Triangle1 Type: {triangle1.get_type()}")

print("\n Comparison of Shapes:")
print(f"Is Circle1 larger than Rectangle? {circle1.is_larger_than(rectangle1)}")

print("\n Shape Calculator Operations:")
calculator = ShapeCalculator()
for shape in shapes:
    calculator.add_shape(shape)

calculator.show_all_shapes()
print(f"Largest Shape: {calculator.largest_shape()}")
print(f"Smallest Shape: {calculator.smallest_shape()}")

print(f"Testing abstract class instantiation:")
try:
    shape = Shape()
except TypeError as e:
    print(f"Error: {e}")
    