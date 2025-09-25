# Inheritance patterns: dataclasses vs classic classes

from dataclasses import dataclass
from utils.fake_factory import fake


# Classic class inheritance
class ClassicVehicle:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year

    def __str__(self):
        return f"{self.year} {self.brand} {self.model}"

    def start_engine(self):
        return f"{self.brand} engine started"


class ClassicCar(ClassicVehicle):
    def __init__(self, brand, model, year, doors, transmission):
        super().__init__(brand, model, year)
        self.doors = doors
        self.transmission = transmission

    def __str__(self):
        return f"{super().__str__()} ({self.doors} doors, {self.transmission})"


class ClassicElectricCar(ClassicCar):
    def __init__(self, brand, model, year, doors, transmission, battery_capacity):
        super().__init__(brand, model, year, doors, transmission)
        self.battery_capacity = battery_capacity

    def start_engine(self):
        return f"{self.brand} electric motor activated"

    def __str__(self):
        return f"{super().__str__()} - {self.battery_capacity}kWh battery"


# Dataclass inheritance
@dataclass
class DataVehicle:
    brand: str
    model: str
    year: int

    def start_engine(self):
        return f"{self.brand} engine started"


@dataclass
class DataCar(DataVehicle):
    doors: int
    transmission: str

    def __str__(self):
        return f"{self.year} {self.brand} {self.model} ({self.doors} doors, {self.transmission})"


@dataclass
class DataElectricCar(DataCar):
    battery_capacity: int

    def start_engine(self):
        return f"{self.brand} electric motor activated"

    def __str__(self):
        return f"{super().__str__()} - {self.battery_capacity}kWh battery"


if __name__ == '__main__':
    print("=== Classic Class Inheritance ===")

    # Classic inheritance requires manual __init__ chaining
    classic_car = ClassicCar("Toyota", "Camry", 2023, 4, "automatic")
    classic_electric = ClassicElectricCar("Tesla", "Model 3", 2023, 4, "automatic", 75)

    print(f"Classic car: {classic_car}")
    print(f"Classic electric: {classic_electric}")
    print(f"Classic car engine: {classic_car.start_engine()}")
    print(f"Classic electric engine: {classic_electric.start_engine()}")

    print("\n=== Dataclass Inheritance ===")

    # Dataclass inheritance automatically handles field inheritance
    data_car = DataCar("Honda", "Civic", 2023, 4, "manual")
    data_electric = DataElectricCar("Nissan", "Leaf", 2023, 4, "automatic", 60)

    print(f"Data car: {data_car}")
    print(f"Data electric: {data_electric}")
    print(f"Data car engine: {data_car.start_engine()}")
    print(f"Data electric engine: {data_electric.start_engine()}")

    # Show automatic __repr__ in dataclasses
    print(f"\nAutomatic repr - Data car: {repr(data_car)}")
    print(f"Automatic repr - Data electric: {repr(data_electric)}")

    # Field access is the same for both
    print(f"\nField access - Classic: brand={classic_car.brand}, doors={classic_car.doors}")
    print(f"Field access - Data: brand={data_car.brand}, doors={data_car.doors}")

    print(f"\nInheritance hierarchy:")
    print(f"Classic electric car MRO: {ClassicElectricCar.__mro__}")
    print(f"Data electric car MRO: {DataElectricCar.__mro__}")