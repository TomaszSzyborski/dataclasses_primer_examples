# Frozen/immutable instances: dataclasses vs classic classes

from dataclasses import dataclass, field
import hashlib
from typing import List


# Classic immutable class (manual implementation)
class ClassicImmutablePoint:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __setattr__(self, name, value):
        if hasattr(self, '_initialized') and self._initialized:
            raise AttributeError(f"Cannot modify immutable attribute '{name}'")
        super().__setattr__(name, value)

    def __delattr__(self, name):
        raise AttributeError(f"Cannot delete attribute '{name}' from immutable object")

    def __repr__(self):
        return f"ClassicImmutablePoint(x={self.x}, y={self.y})"

    def __eq__(self, other):
        if not isinstance(other, ClassicImmutablePoint):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def move(self, dx, dy):
        """Return a new point with offset coordinates"""
        return ClassicImmutablePoint(self.x + dx, self.y + dy)


# Frozen dataclass (automatic immutability)
@dataclass(frozen=True)
class DataImmutablePoint:
    x: float
    y: float

    def move(self, dx, dy):
        """Return a new point with offset coordinates"""
        return DataImmutablePoint(self.x + dx, self.y + dy)


# Classic class attempting immutability with properties
class ClassicPersonImmutable:
    def __init__(self, name, age, email):
        self._name = name
        self._age = age
        self._email = email
        self._initialized = True

    @property
    def name(self):
        return self._name

    @property
    def age(self):
        return self._age

    @property
    def email(self):
        return self._email

    def __setattr__(self, name, value):
        if hasattr(self, '_initialized') and self._initialized:
            raise AttributeError(f"Cannot modify immutable object")
        super().__setattr__(name, value)

    def __repr__(self):
        return f"ClassicPersonImmutable(name='{self.name}', age={self.age})"

    def __eq__(self, other):
        if not isinstance(other, ClassicPersonImmutable):
            return NotImplemented
        return (self.name, self.age, self.email) == (other.name, other.age, other.email)

    def __hash__(self):
        return hash((self.name, self.age, self.email))


# Frozen dataclass person
@dataclass(frozen=True)
class DataPersonImmutable:
    name: str
    age: int
    email: str

    def get_older(self, years=1):
        """Return a new person with increased age"""
        return DataPersonImmutable(self.name, self.age + years, self.email)


# Frozen dataclass with mutable fields (be careful!)
@dataclass(frozen=True)
class DataImmutableWithMutableField:
    name: str
    tags: List[str] = field(default_factory=list)

    def add_tag(self, tag):
        """This modifies the mutable field - dangerous!"""
        self.tags.append(tag)

    def with_tag(self, tag):
        """Safe way: return new instance with updated tags"""
        new_tags = self.tags.copy()
        new_tags.append(tag)
        return DataImmutableWithMutableField(self.name, new_tags)


# Classic configuration class with proper immutability
class ClassicConfiguration:
    def __init__(self, **kwargs):
        self._config = dict(kwargs)
        self._hash = None
        self._initialized = True

    def get(self, key, default=None):
        return self._config.get(key, default)

    def keys(self):
        return self._config.keys()

    def items(self):
        return self._config.items()

    def __setattr__(self, name, value):
        if hasattr(self, '_initialized') and self._initialized:
            raise AttributeError("Configuration is immutable")
        super().__setattr__(name, value)

    def __getitem__(self, key):
        return self._config[key]

    def __repr__(self):
        return f"ClassicConfiguration({self._config})"

    def __hash__(self):
        if self._hash is None:
            self._hash = hash(tuple(sorted(self._config.items())))
        return self._hash

    def with_update(self, **kwargs):
        """Return new configuration with updates"""
        new_config = self._config.copy()
        new_config.update(kwargs)
        return ClassicConfiguration(**new_config)


# Frozen dataclass configuration
@dataclass(frozen=True)
class DataConfiguration:
    host: str
    port: int
    debug: bool = False
    timeout: int = 30

    def with_update(self, **kwargs):
        """Return new configuration with updates"""
        current_values = {
            'host': self.host,
            'port': self.port,
            'debug': self.debug,
            'timeout': self.timeout
        }
        current_values.update(kwargs)
        return DataConfiguration(**current_values)


if __name__ == '__main__':
    print("=== Frozen/Immutable Instances ===")

    # Basic immutability test
    print("\n--- Basic Immutability ---")

    classic_point = ClassicImmutablePoint(10, 20)
    data_point = DataImmutablePoint(10, 20)

    print(f"Classic point: {classic_point}")
    print(f"Data point: {data_point}")

    # Try to modify (should fail)
    print("\n--- Attempting Modifications ---")

    try:
        classic_point.x = 30
        print("Classic point x modified")
    except AttributeError as e:
        print(f"Classic point modification blocked: {e}")

    try:
        data_point.x = 30
        print("Data point x modified")
    except AttributeError as e:
        print(f"Data point modification blocked: {e}")

    # Creating new instances via methods
    print("\n--- Creating New Instances ---")

    classic_moved = classic_point.move(5, 5)
    data_moved = data_point.move(5, 5)

    print(f"Classic moved point: {classic_moved}")
    print(f"Data moved point: {data_moved}")
    print(f"Original classic point unchanged: {classic_point}")
    print(f"Original data point unchanged: {data_point}")

    # Hashing (immutable objects can be hashed)
    print("\n--- Hashing Immutable Objects ---")

    print(f"Classic point hash: {hash(classic_point)}")
    print(f"Data point hash: {hash(data_point)}")

    # Use in sets and as dict keys
    point_set = {classic_point, data_point, ClassicImmutablePoint(10, 20)}
    print(f"Point set size: {len(point_set)}")

    point_dict = {classic_point: "classic", data_point: "data"}
    print(f"Point dict: {point_dict}")

    # Person examples
    print("\n--- Person Immutability ---")

    classic_person = ClassicPersonImmutable("Alice", 30, "alice@email.com")
    data_person = DataPersonImmutable("Alice", 30, "alice@email.com")

    print(f"Classic person: {classic_person}")
    print(f"Data person: {data_person}")

    # Age progression
    older_data_person = data_person.get_older(5)
    print(f"Older data person: {older_data_person}")
    print(f"Original data person unchanged: {data_person}")

    # Dangerous mutable fields example
    print("\n--- Mutable Fields in Frozen Classes (Dangerous!) ---")

    dangerous = DataImmutableWithMutableField("user1", ["tag1", "tag2"])
    print(f"Original: {dangerous}")

    # This modifies the original object (bad!)
    dangerous.add_tag("tag3")
    print(f"After add_tag (original modified!): {dangerous}")

    # Safe way to add tags
    safe_with_tag = DataImmutableWithMutableField("user2", ["tag1"]).with_tag("tag2")
    print(f"Safe tag addition: {safe_with_tag}")

    # Configuration examples
    print("\n--- Configuration Objects ---")

    classic_config = ClassicConfiguration(host="localhost", port=8080, debug=True)
    data_config = DataConfiguration(host="localhost", port=8080, debug=True)

    print(f"Classic config: {classic_config}")
    print(f"Data config: {data_config}")

    # Update configurations
    classic_prod_config = classic_config.with_update(debug=False, port=80)
    data_prod_config = data_config.with_update(debug=False, port=80)

    print(f"Classic prod config: {classic_prod_config}")
    print(f"Data prod config: {data_prod_config}")

    # Original configs unchanged
    print(f"Original classic config unchanged: {classic_config}")
    print(f"Original data config unchanged: {data_config}")

    # Show that frozen objects can be used as dict keys
    config_cache = {
        data_config: "development",
        data_prod_config: "production"
    }
    print(f"\nConfig cache: {config_cache}")

    # Equality comparison
    print(f"\n--- Equality Comparison ---")
    same_classic = ClassicImmutablePoint(10, 20)
    same_data = DataImmutablePoint(10, 20)

    print(f"Classic points equal: {classic_point == same_classic}")
    print(f"Data points equal: {data_point == same_data}")
    print(f"Cross-type equal: {classic_point == data_point}")  # Different types, so False