import numpy as np


class Point:
    """A point in a multi-dimensional space."""

    def __init__(self, x: np.array) -> None:
        self.x: np.array = x
        self.dim: int = x.shape[0]

    def __str__(self) -> str:
        return f"({self.x})"

    def __repr__(self) -> str:
        return f"Point({self.x})"

    def __eq__(self, other: "Point") -> bool:
        return all(self.x == other.x)

    def __le__(self, other: "Point") -> bool:
        return all(self.x <= other.x)

    def __ge__(self, other: "Point") -> bool:
        return all(self.x >= other.x)

    def to_numpy(self) -> np.ndarray:
        """Converts the point to a numpy array."""
        return self.x
