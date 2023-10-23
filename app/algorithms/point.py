from typing import Iterable
import numpy as np

class Point:
    """A point in a multi-dimensional space."""
    global_point_counter: int = 0
    global_coordinate_counter: int = 0

    def __init__(self, x: np.array) -> None:
        self.x: np.array = x
        self.dim: int = x.shape[0]

    def __neg__(self) -> "Point":
        return Point(-self.x)
    
    def __str__(self) -> str:
        return f"({self.x})"

    def __repr__(self) -> str:
        return f"Point({self.x})"

    def __eq__(self, other: "Point") -> bool:
        self.__class__.global_point_counter += 1
        predicate = self.x == other.x
        self.__class__.global_coordinate_counter += np.argmin(predicate) + 1
        return np.all(predicate)

    def __le__(self, other: "Point") -> bool:
        self.__class__.global_point_counter += 1
        predicate = self.x <= other.x
        self.__class__.global_coordinate_counter += np.argmin(predicate) + 1
        return np.all(predicate)

    def __ge__(self, other: "Point") -> bool:
        self.__class__.global_point_counter += 1
        predicate = self.x >= other.x
        self.__class__.global_coordinate_counter += np.argmin(predicate) + 1
        return np.all(predicate)

    def to_numpy(self) -> np.ndarray:
        """Converts the point to a numpy array."""
        return self.x
    
    @classmethod
    def reset_counter(cls) -> None:
        cls.global_point_counter = 0
        cls.global_coordinate_counter = 0

    @classmethod
    def get_global_point_counter(cls) -> int:
        return cls.global_point_counter
    
    @classmethod
    def get_global_coordinate_counter(cls) -> int:
        return cls.global_coordinate_counter


def create_points_from_datapoints(datapoints: Iterable[tuple[int]]) -> list[Point]:
    return [Point(np.array(dp)) for dp in datapoints]
