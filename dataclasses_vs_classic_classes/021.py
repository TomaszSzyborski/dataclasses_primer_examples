# Slots optimization: dataclasses vs classic classes

import sys
from dataclasses import dataclass
from utils.fake_factory import fake


# Classic class without slots
class ClassicPersonNoSlots:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

    def __repr__(self):
        return f"ClassicPersonNoSlots(name='{self.name}', age={self.age})"


# Classic class with slots
class ClassicPersonWithSlots:
    __slots__ = ['name', 'age', 'email']

    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

    def __repr__(self):
        return f"ClassicPersonWithSlots(name='{self.name}', age={self.age})"


# Regular dataclass (no slots)
@dataclass
class DataPersonNoSlots:
    name: str
    age: int
    email: str


# Dataclass with slots (Python 3.10+)
@dataclass(slots=True)
class DataPersonWithSlots:
    name: str
    age: int
    email: str


# Classic class with slots and methods
class ClassicBankAccountSlots:
    __slots__ = ['_balance', 'account_number', 'owner']

    def __init__(self, account_number, owner, initial_balance=0):
        self.account_number = account_number
        self.owner = owner
        self._balance = initial_balance

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount

    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            return True
        return False

    @property
    def balance(self):
        return self._balance

    def __repr__(self):
        return f"ClassicBankAccountSlots(account={self.account_number}, balance=${self.balance})"


# Dataclass with slots and methods
@dataclass(slots=True)
class DataBankAccountSlots:
    account_number: str
    owner: str
    _balance: float = 0

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount

    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            return True
        return False

    @property
    def balance(self):
        return self._balance


def measure_memory_usage(obj_list):
    """Measure approximate memory usage of objects"""
    total_size = 0
    for obj in obj_list:
        # Get size of the object itself
        total_size += sys.getsizeof(obj)

        # For non-slots objects, add __dict__ size
        if hasattr(obj, '__dict__'):
            total_size += sys.getsizeof(obj.__dict__)
            # Add sizes of values in __dict__
            for value in obj.__dict__.values():
                total_size += sys.getsizeof(value)

    return total_size


def test_attribute_access_speed():
    """Simple test to demonstrate attribute access patterns"""
    no_slots = ClassicPersonNoSlots("John", 30, "john@email.com")
    with_slots = ClassicPersonWithSlots("John", 30, "john@email.com")
    data_no_slots = DataPersonNoSlots("John", 30, "john@email.com")
    data_with_slots = DataPersonWithSlots("John", 30, "john@email.com")

    print("=== Attribute Access Patterns ===")

    # Normal attribute access
    print(f"No slots name: {no_slots.name}")
    print(f"With slots name: {with_slots.name}")
    print(f"Data no slots name: {data_no_slots.name}")
    print(f"Data with slots name: {data_with_slots.name}")

    # Try to add dynamic attributes
    print("\n--- Dynamic Attribute Assignment ---")

    try:
        no_slots.dynamic_attr = "This works"
        print(f"No slots dynamic attr: {no_slots.dynamic_attr}")
    except AttributeError as e:
        print(f"No slots error: {e}")

    try:
        with_slots.dynamic_attr = "This should fail"
        print(f"With slots dynamic attr: {with_slots.dynamic_attr}")
    except AttributeError as e:
        print(f"With slots error: {e}")

    try:
        data_no_slots.dynamic_attr = "This works"
        print(f"Data no slots dynamic attr: {data_no_slots.dynamic_attr}")
    except AttributeError as e:
        print(f"Data no slots error: {e}")

    try:
        data_with_slots.dynamic_attr = "This should fail"
        print(f"Data with slots dynamic attr: {data_with_slots.dynamic_attr}")
    except AttributeError as e:
        print(f"Data with slots error: {e}")


if __name__ == '__main__':
    print("=== Slots Optimization Comparison ===")

    # Create test data
    no_slots_list = [ClassicPersonNoSlots(fake.name(), fake.random_int(18, 80), fake.email()) for _ in range(1000)]
    with_slots_list = [ClassicPersonWithSlots(fake.name(), fake.random_int(18, 80), fake.email()) for _ in range(1000)]
    data_no_slots_list = [DataPersonNoSlots(fake.name(), fake.random_int(18, 80), fake.email()) for _ in range(1000)]
    data_with_slots_list = [DataPersonWithSlots(fake.name(), fake.random_int(18, 80), fake.email()) for _ in range(1000)]

    # Memory usage comparison
    print("\n--- Memory Usage (1000 objects) ---")
    no_slots_memory = measure_memory_usage(no_slots_list)
    with_slots_memory = measure_memory_usage(with_slots_list)
    data_no_slots_memory = measure_memory_usage(data_no_slots_list)
    data_with_slots_memory = measure_memory_usage(data_with_slots_list)

    print(f"Classic no slots: {no_slots_memory:,} bytes")
    print(f"Classic with slots: {with_slots_memory:,} bytes")
    print(f"Dataclass no slots: {data_no_slots_memory:,} bytes")
    print(f"Dataclass with slots: {data_with_slots_memory:,} bytes")

    savings_classic = ((no_slots_memory - with_slots_memory) / no_slots_memory) * 100
    savings_data = ((data_no_slots_memory - data_with_slots_memory) / data_no_slots_memory) * 100

    print(f"\nMemory savings:")
    print(f"Classic slots vs no slots: {savings_classic:.1f}%")
    print(f"Dataclass slots vs no slots: {savings_data:.1f}%")

    # Attribute access testing
    test_attribute_access_speed()

    # Slots with inheritance example
    print("\n--- Slots and Inheritance ---")

    class ClassicBaseSlots:
        __slots__ = ['base_attr']

        def __init__(self, base_attr):
            self.base_attr = base_attr

    class ClassicChildSlots(ClassicBaseSlots):
        __slots__ = ['child_attr']  # Must define slots in child too

        def __init__(self, base_attr, child_attr):
            super().__init__(base_attr)
            self.child_attr = child_attr

    @dataclass(slots=True)
    class DataBaseSlots:
        base_attr: str

    @dataclass(slots=True)
    class DataChildSlots(DataBaseSlots):
        child_attr: str

    classic_child = ClassicChildSlots("base", "child")
    data_child = DataChildSlots("base", "child")

    print(f"Classic child slots: {classic_child.base_attr}, {classic_child.child_attr}")
    print(f"Data child slots: {data_child.base_attr}, {data_child.child_attr}")

    # Banking example with slots
    print("\n--- Banking Example with Slots ---")
    classic_account = ClassicBankAccountSlots("ACC123", "Alice Johnson", 1000)
    data_account = DataBankAccountSlots("ACC456", "Bob Smith", 1500)

    print(f"Classic account: {classic_account}")
    print(f"Data account: {data_account}")

    classic_account.deposit(500)
    data_account.withdraw(200)

    print(f"After transactions:")
    print(f"Classic account: {classic_account}")
    print(f"Data account: {data_account}")

    # Show __slots__ attribute
    print(f"\n--- Slots Introspection ---")
    print(f"Classic slots: {ClassicPersonWithSlots.__slots__}")
    print(f"Data slots: {DataPersonWithSlots.__slots__}")