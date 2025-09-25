# Memory usage and performance: dataclasses vs classic classes

import sys
import time
from dataclasses import dataclass, field
from memory_profiler import profile
import tracemalloc
from typing import List
from utils.fake_factory import fake


# Classic class - basic implementation
class ClassicPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"ClassicPoint(x={self.x}, y={self.y})"

    def __eq__(self, other):
        if not isinstance(other, ClassicPoint):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)

    def distance_from_origin(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5


# Dataclass - equivalent implementation
@dataclass
class DataPoint:
    x: float
    y: float

    def distance_from_origin(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5


# Classic class with slots for memory optimization
class ClassicPointSlots:
    __slots__ = ['x', 'y']

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"ClassicPointSlots(x={self.x}, y={self.y})"

    def __eq__(self, other):
        if not isinstance(other, ClassicPointSlots):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)

    def distance_from_origin(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5


# Dataclass with slots
@dataclass(slots=True)
class DataPointSlots:
    x: float
    y: float

    def distance_from_origin(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5


# Complex objects for comparison
class ClassicPerson:
    def __init__(self, name, age, email, address, phone, skills=None):
        self.name = name
        self.age = age
        self.email = email
        self.address = address
        self.phone = phone
        self.skills = skills or []
        self.metadata = {}

    def add_skill(self, skill):
        self.skills.append(skill)

    def __repr__(self):
        return f"ClassicPerson(name='{self.name}', age={self.age})"


@dataclass
class DataPerson:
    name: str
    age: int
    email: str
    address: str
    phone: str
    skills: List[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def add_skill(self, skill):
        self.skills.append(skill)


def measure_object_size(obj):
    """Measure the size of an object and its attributes"""
    size = sys.getsizeof(obj)

    if hasattr(obj, '__dict__'):
        size += sys.getsizeof(obj.__dict__)
        for key, value in obj.__dict__.items():
            size += sys.getsizeof(key) + sys.getsizeof(value)
            if isinstance(value, list):
                for item in value:
                    size += sys.getsizeof(item)
            elif isinstance(value, dict):
                for k, v in value.items():
                    size += sys.getsizeof(k) + sys.getsizeof(v)

    return size


def measure_creation_performance(class_type, count=10000):
    """Measure object creation performance"""
    start_time = time.time()

    objects = []
    for i in range(count):
        if class_type in [ClassicPoint, DataPoint, ClassicPointSlots, DataPointSlots]:
            obj = class_type(i * 0.1, i * 0.2)
        else:  # Person classes
            obj = class_type(
                name=f"Person{i}",
                age=25 + (i % 50),
                email=f"person{i}@email.com",
                address=f"{i} Main St",
                phone=f"555-000-{i:04d}"
            )
        objects.append(obj)

    end_time = time.time()
    return end_time - start_time, objects


def measure_attribute_access_performance(objects, iterations=100000):
    """Measure attribute access performance"""
    start_time = time.time()

    total = 0
    for _ in range(iterations):
        for obj in objects[:100]:  # Use first 100 objects
            if hasattr(obj, 'x'):  # Point objects
                total += obj.x + obj.y
            else:  # Person objects
                total += obj.age

    end_time = time.time()
    return end_time - start_time, total


def compare_memory_usage():
    """Compare memory usage of different implementations"""
    count = 1000

    print("=== Memory Usage Comparison ===")

    # Create objects
    classic_points = [ClassicPoint(i * 0.1, i * 0.2) for i in range(count)]
    data_points = [DataPoint(i * 0.1, i * 0.2) for i in range(count)]
    classic_slots_points = [ClassicPointSlots(i * 0.1, i * 0.2) for i in range(count)]
    data_slots_points = [DataPointSlots(i * 0.1, i * 0.2) for i in range(count)]

    # Measure individual object sizes
    classic_size = measure_object_size(classic_points[0])
    data_size = measure_object_size(data_points[0])
    classic_slots_size = measure_object_size(classic_slots_points[0])
    data_slots_size = measure_object_size(data_slots_points[0])

    print(f"\nSingle Object Memory Usage:")
    print(f"Classic Point:        {classic_size} bytes")
    print(f"Data Point:           {data_size} bytes")
    print(f"Classic Point Slots:  {classic_slots_size} bytes")
    print(f"Data Point Slots:     {data_slots_size} bytes")

    # Calculate total memory for collections
    classic_total = sum(measure_object_size(obj) for obj in classic_points)
    data_total = sum(measure_object_size(obj) for obj in data_points)
    classic_slots_total = sum(measure_object_size(obj) for obj in classic_slots_points)
    data_slots_total = sum(measure_object_size(obj) for obj in data_slots_points)

    print(f"\nTotal Memory for {count} Objects:")
    print(f"Classic Points:       {classic_total:,} bytes")
    print(f"Data Points:          {data_total:,} bytes")
    print(f"Classic Slots Points: {classic_slots_total:,} bytes")
    print(f"Data Slots Points:    {data_slots_total:,} bytes")

    # Calculate memory savings
    slots_savings_classic = ((classic_total - classic_slots_total) / classic_total) * 100
    slots_savings_data = ((data_total - data_slots_total) / data_total) * 100

    print(f"\nMemory Savings with Slots:")
    print(f"Classic: {slots_savings_classic:.1f}%")
    print(f"Data:    {slots_savings_data:.1f}%")


def compare_performance():
    """Compare performance of different implementations"""
    print("\n=== Performance Comparison ===")

    # Object creation performance
    print("\nObject Creation Performance (10,000 objects):")

    classic_time, classic_objects = measure_creation_performance(ClassicPoint)
    data_time, data_objects = measure_creation_performance(DataPoint)
    classic_slots_time, classic_slots_objects = measure_creation_performance(ClassicPointSlots)
    data_slots_time, data_slots_objects = measure_creation_performance(DataPointSlots)

    print(f"Classic Point:        {classic_time:.4f} seconds")
    print(f"Data Point:           {data_time:.4f} seconds")
    print(f"Classic Point Slots:  {classic_slots_time:.4f} seconds")
    print(f"Data Point Slots:     {data_slots_time:.4f} seconds")

    # Attribute access performance
    print("\nAttribute Access Performance (100,000 iterations):")

    classic_access_time, _ = measure_attribute_access_performance(classic_objects)
    data_access_time, _ = measure_attribute_access_performance(data_objects)
    classic_slots_access_time, _ = measure_attribute_access_performance(classic_slots_objects)
    data_slots_access_time, _ = measure_attribute_access_performance(data_slots_objects)

    print(f"Classic Point:        {classic_access_time:.4f} seconds")
    print(f"Data Point:           {data_access_time:.4f} seconds")
    print(f"Classic Point Slots:  {classic_slots_access_time:.4f} seconds")
    print(f"Data Point Slots:     {data_slots_access_time:.4f} seconds")


def compare_complex_objects():
    """Compare memory and performance for complex objects"""
    print("\n=== Complex Object Comparison ===")

    count = 1000

    # Create complex objects
    classic_persons = []
    data_persons = []

    for i in range(count):
        classic_person = ClassicPerson(
            name=fake.name(),
            age=fake.random_int(18, 80),
            email=fake.email(),
            address=fake.address(),
            phone=fake.phone_number(),
            skills=fake.random_elements(["Python", "Java", "JavaScript", "SQL", "Docker"], length=2)
        )
        classic_persons.append(classic_person)

        data_person = DataPerson(
            name=fake.name(),
            age=fake.random_int(18, 80),
            email=fake.email(),
            address=fake.address(),
            phone=fake.phone_number(),
            skills=list(fake.random_elements(["Python", "Java", "JavaScript", "SQL", "Docker"], length=2))
        )
        data_persons.append(data_person)

    # Measure memory usage
    classic_person_size = measure_object_size(classic_persons[0])
    data_person_size = measure_object_size(data_persons[0])

    print(f"\nComplex Object Memory Usage:")
    print(f"Classic Person: {classic_person_size} bytes")
    print(f"Data Person:    {data_person_size} bytes")

    # Method call performance
    print(f"\nMethod Call Performance:")

    start_time = time.time()
    for person in classic_persons:
        person.add_skill("NewSkill")
    classic_method_time = time.time() - start_time

    start_time = time.time()
    for person in data_persons:
        person.add_skill("NewSkill")
    data_method_time = time.time() - start_time

    print(f"Classic Person method calls: {classic_method_time:.4f} seconds")
    print(f"Data Person method calls:    {data_method_time:.4f} seconds")


def show_introspection_differences():
    """Show differences in introspection capabilities"""
    print("\n=== Introspection Differences ===")

    classic_point = ClassicPoint(1.0, 2.0)
    data_point = DataPoint(1.0, 2.0)

    print(f"Classic Point __dict__: {classic_point.__dict__}")
    print(f"Data Point __dict__: {data_point.__dict__}")

    print(f"\nData Point fields: {data_point.__dataclass_fields__}")
    print(f"Data Point annotations: {DataPoint.__annotations__}")

    # Show repr differences
    print(f"\nRepr comparison:")
    print(f"Classic: {repr(classic_point)}")
    print(f"Data:    {repr(data_point)}")


if __name__ == '__main__':
    print("=== Memory Usage and Performance Comparison ===")
    print("Note: Install memory_profiler with: pip install memory_profiler")
    print("      Some features may not work without it.\n")

    try:
        compare_memory_usage()
        compare_performance()
        compare_complex_objects()
        show_introspection_differences()

        print("\n=== Summary ===")
        print("Performance Characteristics:")
        print("• Dataclasses have slight overhead for __repr__, __eq__, etc.")
        print("• Object creation is generally similar")
        print("• Attribute access performance is nearly identical")
        print("• Slots provide significant memory savings for both")
        print("• Dataclass slots combine best of both worlds")

        print("\nMemory Characteristics:")
        print("• Regular classes and dataclasses use similar memory")
        print("• Slots reduce memory usage significantly (30-50%)")
        print("• Complex objects show more varied memory patterns")
        print("• Dataclass field metadata adds minimal overhead")

        print("\nDevelopment Characteristics:")
        print("• Dataclasses reduce boilerplate code significantly")
        print("• Built-in methods (__repr__, __eq__) save development time")
        print("• Type annotations are more natural in dataclasses")
        print("• Introspection capabilities are enhanced")

    except ImportError:
        print("Warning: memory_profiler not installed. Some measurements may be inaccurate.")
        print("Install with: pip install memory_profiler")
    except Exception as e:
        print(f"Error during benchmarking: {e}")
        print("Continuing with available measurements...")