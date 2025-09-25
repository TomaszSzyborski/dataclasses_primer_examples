# Property handling: dataclasses vs classic classes

from dataclasses import dataclass, field
import math


# Classic class with properties
class ClassicCircle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @property
    def area(self):
        return math.pi * self._radius ** 2

    @property
    def circumference(self):
        return 2 * math.pi * self._radius

    def __str__(self):
        return f"Circle(radius={self.radius})"

    def __repr__(self):
        return f"ClassicCircle(radius={self.radius})"


# Dataclass with properties
@dataclass
class DataCircle:
    _radius: float = field(repr=False)

    def __post_init__(self):
        if self._radius < 0:
            raise ValueError("Radius cannot be negative")

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @property
    def area(self):
        return math.pi * self._radius ** 2

    @property
    def circumference(self):
        return 2 * math.pi * self._radius


# Another approach: dataclass with computed fields
@dataclass
class DataCircleComputed:
    radius: float

    def __post_init__(self):
        if self.radius < 0:
            raise ValueError("Radius cannot be negative")

    @property
    def area(self):
        return math.pi * self.radius ** 2

    @property
    def circumference(self):
        return 2 * math.pi * self.radius

    # Computed fields using field()
    diameter: float = field(init=False)

    def __post_init__(self):
        if self.radius < 0:
            raise ValueError("Radius cannot be negative")
        self.diameter = 2 * self.radius


# Classic class with lazy property
class ClassicExpensiveCalculation:
    def __init__(self, base_value):
        self.base_value = base_value
        self._expensive_result = None

    @property
    def expensive_result(self):
        if self._expensive_result is None:
            print("Computing expensive result...")
            self._expensive_result = sum(i ** 2 for i in range(self.base_value))
        return self._expensive_result


# Dataclass with lazy property
@dataclass
class DataExpensiveCalculation:
    base_value: int
    _expensive_result: int = field(default=None, init=False, repr=False)

    @property
    def expensive_result(self):
        if self._expensive_result is None:
            print("Computing expensive result...")
            self._expensive_result = sum(i ** 2 for i in range(self.base_value))
        return self._expensive_result


if __name__ == '__main__':
    print("=== Property Handling Comparison ===")

    # Classic circle
    print("\n--- Classic Circle ---")
    classic_circle = ClassicCircle(5)
    print(f"Classic circle: {classic_circle}")
    print(f"Area: {classic_circle.area:.2f}")
    print(f"Circumference: {classic_circle.circumference:.2f}")

    # Dataclass circle
    print("\n--- Dataclass Circle ---")
    data_circle = DataCircle(5)
    print(f"Data circle: {data_circle}")
    print(f"Area: {data_circle.area:.2f}")
    print(f"Circumference: {data_circle.circumference:.2f}")

    # Dataclass with computed fields
    print("\n--- Dataclass with Computed Fields ---")
    computed_circle = DataCircleComputed(5)
    print(f"Computed circle: {computed_circle}")
    print(f"Diameter (computed): {computed_circle.diameter}")
    print(f"Area: {computed_circle.area:.2f}")

    # Property setters
    print("\n--- Property Setters ---")
    classic_circle.radius = 10
    data_circle.radius = 10
    print(f"Classic after radius change: {classic_circle}")
    print(f"Data after radius change: {data_circle}")

    # Error handling
    print("\n--- Error Handling ---")
    try:
        ClassicCircle(-1)
    except ValueError as e:
        print(f"Classic circle error: {e}")

    try:
        DataCircle(-1)
    except ValueError as e:
        print(f"Data circle error: {e}")

    # Lazy properties
    print("\n--- Lazy Properties ---")
    classic_expensive = ClassicExpensiveCalculation(1000)
    data_expensive = DataExpensiveCalculation(1000)

    print("First access to expensive_result:")
    print(f"Classic: {classic_expensive.expensive_result}")
    print(f"Data: {data_expensive.expensive_result}")

    print("\nSecond access (should be cached):")
    print(f"Classic: {classic_expensive.expensive_result}")
    print(f"Data: {data_expensive.expensive_result}")

    # Show repr differences
    print(f"\n--- Representation Differences ---")
    print(f"Classic repr: {repr(classic_circle)}")
    print(f"Data repr: {repr(data_circle)}")
    print(f"Computed repr: {repr(computed_circle)}")