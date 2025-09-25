# Comparison and hashing: dataclasses vs classic classes

from dataclasses import dataclass, field
from utils.fake_factory import fake


# Classic class without comparison methods
class ClassicPersonBasic:
    """
    A classic Python class representing a person, without any custom
    comparison or hashing methods implemented.
    """

    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

    def __repr__(self):
        return f"ClassicPersonBasic(name='{self.name}', age={self.age}, email='{self.email}')"


# Classic class with manual comparison methods
class ClassicPersonWithComparison:
    """
    A classic Python class with manually implemented comparison methods
    (__eq__, __lt__) and hashing (__hash__) to demonstrate how dataclasses
    automate this functionality.
    """
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

    def __repr__(self):
        return f"ClassicPersonWithComparison(name='{self.name}', age={self.age}, email='{self.email}')"

    def __eq__(self, other):
        if not isinstance(other, ClassicPersonWithComparison):
            return NotImplemented
        return (self.name, self.age, self.email) == (other.name, other.age, other.email)

    def __lt__(self, other):
        if not isinstance(other, ClassicPersonWithComparison):
            return NotImplemented
        return (self.name, self.age) < (other.name, other.age)

    def __hash__(self):
        return hash((self.name, self.age, self.email))


# Basic dataclass (automatic comparison)
@dataclass
class DataPersonBasic:
    name: str
    age: int
    email: str


# Dataclass with custom ordering
@dataclass(order=True)
class DataPersonOrdered:
    name: str
    age: int
    email: str


# Dataclass with unsafe hashing (mutable but hashable)
@dataclass(unsafe_hash=True)
class DataPersonUnsafeHash:
    name: str
    age: int
    email: str


# Dataclass with partial field comparison
@dataclass
class DataPersonPartialCompare:
    name: str
    age: int
    email: str
    internal_id: str = field(compare=False)  # Exclude from comparisons


# Dataclass for priority queue usage
@dataclass(order=True)
class DataTask:
    priority: int
    description: str = field(compare=False)  # Only compare by priority


if __name__ == '__main__':
    print("=== Comparison and Hashing ===")

    # Create test instances
    classic_basic1 = ClassicPersonBasic("Alice", 30, "alice@email.com")
    classic_basic2 = ClassicPersonBasic("Alice", 30, "alice@email.com")

    classic_comp1 = ClassicPersonWithComparison("Alice", 30, "alice@email.com")
    classic_comp2 = ClassicPersonWithComparison("Alice", 30, "alice@email.com")

    data_basic1 = DataPersonBasic("Alice", 30, "alice@email.com")
    data_basic2 = DataPersonBasic("Alice", 30, "alice@email.com")

    print("\n--- Basic Equality ---")
    print(f"Classic basic equality: {classic_basic1 == classic_basic2}")  # False (object identity)
    print(f"Classic with comparison: {classic_comp1 == classic_comp2}")   # True (custom __eq__)
    print(f"Dataclass basic equality: {data_basic1 == data_basic2}")     # True (automatic __eq__)

    print(f"\nObject identity check:")
    print(f"Classic basic is same: {classic_basic1 is classic_basic2}")
    print(f"Dataclass basic is same: {data_basic1 is data_basic2}")

    # Ordering examples
    print("\n--- Ordering ---")

    try:
        result = classic_basic1 < classic_basic2
        print(f"Classic basic ordering: {result}")
    except TypeError as e:
        print(f"Classic basic ordering error: {e}")

    print(f"Classic with comparison ordering: {ClassicPersonWithComparison('Alice', 25, 'alice@email.com') < classic_comp1}")

    data_ordered1 = DataPersonOrdered("Alice", 25, "alice@email.com")
    data_ordered2 = DataPersonOrdered("Bob", 30, "bob@email.com")
    print(f"Dataclass ordered: {data_ordered1 < data_ordered2}")

    # Hashing examples
    print("\n--- Hashing ---")

    try:
        hash_classic_basic = hash(classic_basic1)
        print(f"Classic basic hash: {hash_classic_basic}")
    except TypeError as e:
        print(f"Classic basic hash error: {e}")

    print(f"Classic with comparison hash: {hash(classic_comp1)}")

    try:
        hash_data_basic = hash(data_basic1)
        print(f"Dataclass basic hash: {hash_data_basic}")
    except TypeError as e:
        print(f"Dataclass basic hash error: {e}")

    data_unsafe_hash = DataPersonUnsafeHash("Alice", 30, "alice@email.com")
    print(f"Dataclass unsafe hash: {hash(data_unsafe_hash)}")

    # Set operations
    print("\n--- Set Operations ---")

    # Classic comparison objects can be in sets
    classic_set = {classic_comp1, classic_comp2, ClassicPersonWithComparison("Bob", 25, "bob@email.com")}
    print(f"Classic set size: {len(classic_set)}")  # 2 (Alice objects are equal)

    # Unsafe hash dataclass can be in sets
    unsafe_hash_set = {
        data_unsafe_hash,
        DataPersonUnsafeHash("Alice", 30, "alice@email.com"),
        DataPersonUnsafeHash("Bob", 25, "bob@email.com")
    }
    print(f"Unsafe hash set size: {len(unsafe_hash_set)}")

    # Partial field comparison
    print("\n--- Partial Field Comparison ---")
    partial1 = DataPersonPartialCompare("Alice", 30, "alice@email.com", "ID123")
    partial2 = DataPersonPartialCompare("Alice", 30, "alice@email.com", "ID456")
    print(f"Partial compare (different internal_id): {partial1 == partial2}")  # True (internal_id ignored)

    # Priority queue example
    print("\n--- Priority Queue Usage ---")
    tasks = [
        DataTask(3, "Low priority task"),
        DataTask(1, "High priority task"),
        DataTask(2, "Medium priority task"),
        DataTask(1, "Another high priority task")
    ]

    tasks.sort()
    print("Sorted tasks by priority:")
    for task in tasks:
        print(f"  {task}")

    # Demonstrate field-level comparison control
    task1 = DataTask(1, "Task A")
    task2 = DataTask(1, "Task B")
    print(f"\nSame priority tasks equal: {task1 == task2}")  # True (description not compared)