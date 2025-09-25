# Field validation and conversion: dataclasses vs classic classes

from dataclasses import dataclass, field
from typing import List, Union
import re
from datetime import datetime


# Classic class with manual validation
class ClassicUser:
    def __init__(self, username, email, age, tags=None):
        self.username = self._validate_username(username)
        self.email = self._validate_email(email)
        self.age = self._validate_age(age)
        self.tags = self._validate_tags(tags or [])
        self.created_at = datetime.now()

    def _validate_username(self, username):
        if not isinstance(username, str):
            raise TypeError("Username must be a string")
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters")
        if not username.isalnum():
            raise ValueError("Username must contain only alphanumeric characters")
        return username.lower()

    def _validate_email(self, email):
        if not isinstance(email, str):
            raise TypeError("Email must be a string")
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValueError("Invalid email format")
        return email.lower()

    def _validate_age(self, age):
        if isinstance(age, str) and age.isdigit():
            age = int(age)
        if not isinstance(age, int):
            raise TypeError("Age must be an integer")
        if age < 0 or age > 150:
            raise ValueError("Age must be between 0 and 150")
        return age

    def _validate_tags(self, tags):
        if not isinstance(tags, list):
            raise TypeError("Tags must be a list")
        validated_tags = []
        for tag in tags:
            if not isinstance(tag, str):
                raise TypeError("Each tag must be a string")
            validated_tags.append(tag.strip().lower())
        return validated_tags

    def __repr__(self):
        return f"ClassicUser(username='{self.username}', email='{self.email}', age={self.age})"


# Dataclass with __post_init__ validation
@dataclass
class DataUserPostInit:
    username: str
    email: str
    age: Union[int, str]
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(init=False)

    def __post_init__(self):
        self.username = self._validate_username(self.username)
        self.email = self._validate_email(self.email)
        self.age = self._validate_age(self.age)
        self.tags = self._validate_tags(self.tags)
        self.created_at = datetime.now()

    def _validate_username(self, username):
        if not isinstance(username, str):
            raise TypeError("Username must be a string")
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters")
        if not username.isalnum():
            raise ValueError("Username must contain only alphanumeric characters")
        return username.lower()

    def _validate_email(self, email):
        if not isinstance(email, str):
            raise TypeError("Email must be a string")
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValueError("Invalid email format")
        return email.lower()

    def _validate_age(self, age):
        if isinstance(age, str) and age.isdigit():
            age = int(age)
        if not isinstance(age, int):
            raise TypeError("Age must be an integer")
        if age < 0 or age > 150:
            raise ValueError("Age must be between 0 and 150")
        return age

    def _validate_tags(self, tags):
        if not isinstance(tags, list):
            raise TypeError("Tags must be a list")
        validated_tags = []
        for tag in tags:
            if not isinstance(tag, str):
                raise TypeError("Each tag must be a string")
            validated_tags.append(tag.strip().lower())
        return validated_tags


# Classic class with property-based validation
class ClassicProduct:
    def __init__(self, name, price, category="general"):
        self._name = None
        self._price = None
        self._category = None

        self.name = name
        self.price = price
        self.category = category

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if len(value.strip()) == 0:
            raise ValueError("Name cannot be empty")
        self._name = value.strip().title()

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if isinstance(value, str):
            try:
                value = float(value)
            except ValueError:
                raise ValueError("Price must be a valid number")
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number")
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = round(float(value), 2)

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        valid_categories = ["general", "electronics", "clothing", "books", "food"]
        if not isinstance(value, str):
            raise TypeError("Category must be a string")
        value = value.lower().strip()
        if value not in valid_categories:
            raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        self._category = value

    def __repr__(self):
        return f"ClassicProduct(name='{self.name}', price={self.price}, category='{self.category}')"


# Dataclass with property validation (hybrid approach)
@dataclass
class DataProduct:
    _name: str = field(repr=False)
    _price: float = field(repr=False)
    _category: str = field(default="general", repr=False)

    def __post_init__(self):
        # Use setters for validation
        temp_name = self._name
        temp_price = self._price
        temp_category = self._category

        # Clear fields to avoid setter conflicts
        object.__setattr__(self, '_name', None)
        object.__setattr__(self, '_price', None)
        object.__setattr__(self, '_category', None)

        # Set through properties for validation
        self.name = temp_name
        self.price = temp_price
        self.category = temp_category

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if len(value.strip()) == 0:
            raise ValueError("Name cannot be empty")
        object.__setattr__(self, '_name', value.strip().title())

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if isinstance(value, str):
            try:
                value = float(value)
            except ValueError:
                raise ValueError("Price must be a valid number")
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number")
        if value < 0:
            raise ValueError("Price cannot be negative")
        object.__setattr__(self, '_price', round(float(value), 2))

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        valid_categories = ["general", "electronics", "clothing", "books", "food"]
        if not isinstance(value, str):
            raise TypeError("Category must be a string")
        value = value.lower().strip()
        if value not in valid_categories:
            raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        object.__setattr__(self, '_category', value)


# Helper function for dataclass field conversion
def convert_to_int(value):
    """Convert string to int if possible"""
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return value


def validate_positive_int(value):
    """Validate that value is a positive integer"""
    if not isinstance(value, int):
        raise TypeError("Value must be an integer")
    if value <= 0:
        raise ValueError("Value must be positive")
    return value


# Dataclass with field conversion functions
@dataclass
class DataCounter:
    name: str
    count: int = field(default=1)

    def __post_init__(self):
        self.count = validate_positive_int(convert_to_int(self.count))
        self.name = self.name.strip().title()


if __name__ == '__main__':
    print("=== Field Validation and Conversion ===")

    # User validation examples
    print("\n--- User Validation ---")

    try:
        classic_user = ClassicUser("JohnDoe", "john@email.com", "25", ["python", "programming"])
        print(f"Classic user: {classic_user}")
        print(f"Tags: {classic_user.tags}")
    except (ValueError, TypeError) as e:
        print(f"Classic user error: {e}")

    try:
        data_user = DataUserPostInit("JohnDoe", "john@email.com", "25", ["python", "programming"])
        print(f"Data user: {data_user}")
        print(f"Tags: {data_user.tags}")
    except (ValueError, TypeError) as e:
        print(f"Data user error: {e}")

    # Test validation failures
    print("\n--- Validation Failures ---")

    try:
        ClassicUser("jo", "invalid-email", 200)
    except (ValueError, TypeError) as e:
        print(f"Classic validation error: {e}")

    try:
        DataUserPostInit("jo", "invalid-email", 200)
    except (ValueError, TypeError) as e:
        print(f"Data validation error: {e}")

    # Product validation with properties
    print("\n--- Product Property Validation ---")

    classic_product = ClassicProduct("  laptop computer  ", "999.99", "ELECTRONICS")
    data_product = DataProduct("  laptop computer  ", "999.99", "ELECTRONICS")

    print(f"Classic product: {classic_product}")
    print(f"Data product: name='{data_product.name}', price={data_product.price}, category='{data_product.category}'")

    # Test property setters
    print("\n--- Property Setter Validation ---")

    try:
        classic_product.price = "1299.95"
        print(f"Classic product price updated: {classic_product.price}")
    except (ValueError, TypeError) as e:
        print(f"Classic price error: {e}")

    try:
        data_product.price = "1299.95"
        print(f"Data product price updated: {data_product.price}")
    except (ValueError, TypeError) as e:
        print(f"Data price error: {e}")

    # Test invalid category
    try:
        classic_product.category = "invalid_category"
    except ValueError as e:
        print(f"Classic category error: {e}")

    try:
        data_product.category = "invalid_category"
    except ValueError as e:
        print(f"Data category error: {e}")

    # Counter with conversion
    print("\n--- Field Conversion ---")

    counter1 = DataCounter("  page views  ", "42")
    print(f"Counter 1: {counter1}")

    counter2 = DataCounter("Downloads", 100)
    print(f"Counter 2: {counter2}")

    try:
        DataCounter("Invalid", "not_a_number")
    except (ValueError, TypeError) as e:
        print(f"Counter conversion error: {e}")

    try:
        DataCounter("Negative", -5)
    except ValueError as e:
        print(f"Counter validation error: {e}")

    # Show differences in approach
    print("\n--- Validation Approach Comparison ---")
    print("Classic classes:")
    print("  - Manual validation in __init__")
    print("  - Property setters for ongoing validation")
    print("  - More control over when validation occurs")

    print("\nDataclasses:")
    print("  - __post_init__ for initialization validation")
    print("  - Properties still needed for setter validation")
    print("  - Less boilerplate for simple cases")
    print("  - More complex when combining with properties")