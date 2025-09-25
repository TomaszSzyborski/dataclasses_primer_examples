# Type hints and annotations: dataclasses vs classic classes

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union, Tuple, Any, ClassVar
from datetime import datetime, date
import inspect


# Classic class with type hints (manual)
class ClassicEmployee:
    company_name: ClassVar[str] = "TechCorp"  # Class variable

    def __init__(
        self,
        name: str,
        employee_id: int,
        salary: float,
        department: str,
        skills: List[str],
        manager: Optional['ClassicEmployee'] = None,
        hire_date: date = None
    ) -> None:
        self.name = name
        self.employee_id = employee_id
        self.salary = salary
        self.department = department
        self.skills = skills
        self.manager = manager
        self.hire_date = hire_date or date.today()
        self.performance_reviews: List[Dict[str, Any]] = []

    def add_skill(self, skill: str) -> None:
        if skill not in self.skills:
            self.skills.append(skill)

    def get_salary_info(self) -> Dict[str, Union[float, str]]:
        return {
            "amount": self.salary,
            "currency": "USD",
            "department": self.department
        }

    def assign_manager(self, manager: 'ClassicEmployee') -> bool:
        if manager.department == self.department:
            self.manager = manager
            return True
        return False

    def __repr__(self) -> str:
        return f"ClassicEmployee(name='{self.name}', id={self.employee_id})"


# Dataclass with automatic type annotations
@dataclass
class DataEmployee:
    company_name: ClassVar[str] = "TechCorp"  # Class variable
    name: str
    employee_id: int
    salary: float
    department: str
    skills: List[str]
    manager: Optional['DataEmployee'] = None
    hire_date: date = field(default_factory=date.today)
    performance_reviews: List[Dict[str, Any]] = field(default_factory=list)

    def add_skill(self, skill: str) -> None:
        if skill not in self.skills:
            self.skills.append(skill)

    def get_salary_info(self) -> Dict[str, Union[float, str]]:
        return {
            "amount": self.salary,
            "currency": "USD",
            "department": self.department
        }

    def assign_manager(self, manager: 'DataEmployee') -> bool:
        if manager.department == self.department:
            self.manager = manager
            return True
        return False


# Complex typing examples
class ClassicAnalytics:
    def __init__(self) -> None:
        self.metrics: Dict[str, List[float]] = {}
        self.metadata: Dict[str, Any] = {}

    def add_metric(
        self,
        name: str,
        values: List[Union[int, float]],
        tags: Optional[Dict[str, str]] = None
    ) -> None:
        self.metrics[name] = [float(v) for v in values]
        if tags:
            self.metadata[name] = tags

    def get_statistics(
        self,
        metric_name: str
    ) -> Tuple[float, float, float]:  # min, max, avg
        values = self.metrics.get(metric_name, [])
        if not values:
            return 0.0, 0.0, 0.0
        return min(values), max(values), sum(values) / len(values)

    def process_batch(
        self,
        data: List[Dict[str, Any]]
    ) -> Dict[str, List[float]]:
        results = {}
        for item in data:
            for key, value in item.items():
                if isinstance(value, (int, float)):
                    if key not in results:
                        results[key] = []
                    results[key].append(float(value))
        return results


@dataclass
class DataAnalytics:
    metrics: Dict[str, List[float]] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_metric(
        self,
        name: str,
        values: List[Union[int, float]],
        tags: Optional[Dict[str, str]] = None
    ) -> None:
        self.metrics[name] = [float(v) for v in values]
        if tags:
            self.metadata[name] = tags

    def get_statistics(
        self,
        metric_name: str
    ) -> Tuple[float, float, float]:  # min, max, avg
        values = self.metrics.get(metric_name, [])
        if not values:
            return 0.0, 0.0, 0.0
        return min(values), max(values), sum(values) / len(values)

    def process_batch(
        self,
        data: List[Dict[str, Any]]
    ) -> Dict[str, List[float]]:
        results = {}
        for item in data:
            for key, value in item.items():
                if isinstance(value, (int, float)):
                    if key not in results:
                        results[key] = []
                    results[key].append(float(value))
        return results


# Generic type hints
from typing import TypeVar, Generic

T = TypeVar('T')


class ClassicContainer(Generic[T]):
    def __init__(self, items: List[T]) -> None:
        self.items: List[T] = items

    def add(self, item: T) -> None:
        self.items.append(item)

    def get_all(self) -> List[T]:
        return self.items.copy()

    def filter_by_type(self, target_type: type) -> List[T]:
        return [item for item in self.items if isinstance(item, target_type)]


@dataclass
class DataContainer(Generic[T]):
    items: List[T] = field(default_factory=list)

    def add(self, item: T) -> None:
        self.items.append(item)

    def get_all(self) -> List[T]:
        return self.items.copy()

    def filter_by_type(self, target_type: type) -> List[T]:
        return [item for item in self.items if isinstance(item, target_type)]


# Forward reference examples
class ClassicNode:
    def __init__(
        self,
        value: Any,
        children: Optional[List['ClassicNode']] = None
    ) -> None:
        self.value = value
        self.children: List['ClassicNode'] = children or []

    def add_child(self, node: 'ClassicNode') -> None:
        self.children.append(node)

    def find_value(self, target: Any) -> Optional['ClassicNode']:
        if self.value == target:
            return self
        for child in self.children:
            result = child.find_value(target)
            if result:
                return result
        return None


@dataclass
class DataNode:
    value: Any
    children: List['DataNode'] = field(default_factory=list)

    def add_child(self, node: 'DataNode') -> None:
        self.children.append(node)

    def find_value(self, target: Any) -> Optional['DataNode']:
        if self.value == target:
            return self
        for child in self.children:
            result = child.find_value(target)
            if result:
                return result
        return None


def analyze_type_annotations(cls) -> Dict[str, Any]:
    """Analyze type annotations of a class"""
    annotations = {}

    # Get class annotations
    if hasattr(cls, '__annotations__'):
        annotations['class_fields'] = cls.__annotations__

    # Get method annotations
    method_annotations = {}
    for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
        if hasattr(method, '__annotations__'):
            method_annotations[name] = method.__annotations__

    annotations['methods'] = method_annotations
    return annotations


if __name__ == '__main__':
    print("=== Type Hints and Annotations ===")

    # Employee examples
    print("\n--- Employee Type Hints ---")

    classic_emp = ClassicEmployee(
        name="Alice Johnson",
        employee_id=1001,
        salary=75000.0,
        department="Engineering",
        skills=["Python", "JavaScript", "SQL"]
    )

    data_emp = DataEmployee(
        name="Bob Smith",
        employee_id=1002,
        salary=80000.0,
        department="Engineering",
        skills=["Java", "Spring", "Docker"]
    )

    print(f"Classic employee: {classic_emp}")
    print(f"Data employee: {data_emp}")

    # Manager assignment
    data_manager = DataEmployee(
        name="Carol Davis",
        employee_id=2001,
        salary=95000.0,
        department="Engineering",
        skills=["Leadership", "Architecture", "Python"]
    )

    success = data_emp.assign_manager(data_manager)
    print(f"Manager assignment successful: {success}")
    print(f"Employee manager: {data_emp.manager.name if data_emp.manager else 'None'}")

    # Analytics examples
    print("\n--- Analytics Type Hints ---")

    classic_analytics = ClassicAnalytics()
    data_analytics = DataAnalytics()

    # Add some metrics
    classic_analytics.add_metric("response_time", [0.1, 0.2, 0.15, 0.3], {"unit": "seconds"})
    data_analytics.add_metric("cpu_usage", [45.2, 67.8, 23.1, 89.4], {"unit": "percent"})

    classic_stats = classic_analytics.get_statistics("response_time")
    data_stats = data_analytics.get_statistics("cpu_usage")

    print(f"Classic stats (min, max, avg): {classic_stats}")
    print(f"Data stats (min, max, avg): {data_stats}")

    # Generic containers
    print("\n--- Generic Type Hints ---")

    str_container = DataContainer[str]()
    str_container.add("hello")
    str_container.add("world")
    print(f"String container: {str_container.get_all()}")

    int_container = DataContainer[int]()
    int_container.add(1)
    int_container.add(2)
    int_container.add(3)
    print(f"Int container: {int_container.get_all()}")

    # Node tree example
    print("\n--- Forward Reference Type Hints ---")

    root = DataNode("root")
    child1 = DataNode("child1")
    child2 = DataNode("child2")
    grandchild = DataNode("grandchild")

    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(grandchild)

    found = root.find_value("grandchild")
    print(f"Found node: {found.value if found else 'Not found'}")

    # Type annotation analysis
    print("\n--- Type Annotation Analysis ---")

    classic_annotations = analyze_type_annotations(ClassicEmployee)
    data_annotations = analyze_type_annotations(DataEmployee)

    print("Classic class annotations:")
    if 'class_fields' in classic_annotations:
        for field, annotation in classic_annotations['class_fields'].items():
            print(f"  {field}: {annotation}")
    else:
        print("  No class field annotations")

    print("\nDataclass annotations:")
    if 'class_fields' in data_annotations:
        for field, annotation in data_annotations['class_fields'].items():
            print(f"  {field}: {annotation}")

    # Show runtime type checking capabilities
    print("\n--- Runtime Type Information ---")

    print(f"Classic employee type hints: {ClassicEmployee.__init__.__annotations__}")
    print(f"Data employee field types: {DataEmployee.__annotations__}")

    # Demonstrate type hint benefits for IDEs and tools
    print("\n--- Type Hint Benefits ---")
    print("Benefits of type hints:")
    print("  - IDE autocompletion and error detection")
    print("  - Static type checking with mypy")
    print("  - Self-documenting code")
    print("  - Runtime type inspection")
    print("  - Better refactoring support")

    print("\nDataclass advantages:")
    print("  - Automatic field type annotations")
    print("  - Less boilerplate for typed fields")
    print("  - Built-in support for typing module")
    print("  - Field metadata with type information")