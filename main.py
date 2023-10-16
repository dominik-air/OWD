import numpy as np
from typing import Iterable


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


def distance_between_points(p1: Point, p2: Point):
    return np.sum(np.square(p1.x - p2.x))


def create_points_from_datapoints(datapoints: Iterable[tuple[int]]) -> list[Point]:
    return [Point(np.array(dp)) for dp in datapoints]


def ideal_point_method(points: Iterable[Point]) -> list[Point]:
    xmin = []
    for i in range(points[0].dim):
        min_i = min(points, key=lambda p: p.x[i]).x[i]
        xmin.append(min_i)
    xmin = Point(np.array(xmin))
    dists_with_indices = [
        (distance_between_points(xmin, p), i) for i, p in enumerate(points)
    ]
    dists_with_indices.sort(key=lambda x: x[0])
    indices = [i for _, i in dists_with_indices]

    m = 0
    M = len(points)
    non_dominated_points = []
    active_points = [True] * len(points)
    while m <= M:
        if not active_points[indices[m]]:
            m += 1
            continue

        for i, p in enumerate(points):
            if points[indices[m]] <= p:
                active_points[i] = False
        active_points[indices[m]] = False
        non_dominated_points.append(points[indices[m]])

        M -= 1
        m += 1
    return non_dominated_points


if __name__ == "__main__":
    test_datapoints = [
        (5, 5),
        (3, 6),
        (4, 4),
        (5, 3),
        (3, 3),
        (1, 8),
        (3, 4),
        (4, 5),
        (3, 10),
        (6, 6),
        (4, 1),
        (3, 5),
    ]

    points = create_points_from_datapoints(test_datapoints)
    non_dominated_points = ideal_point_method(points)
    expected_non_dominated_points = [
        Point(np.array([3, 3])),
        Point(np.array([4, 1])),
        Point(np.array([1, 8])),
    ]

    assert len(non_dominated_points) == len(expected_non_dominated_points)

    for actual, expected in zip(non_dominated_points, expected_non_dominated_points):
        print(actual, expected)
        assert actual == expected
