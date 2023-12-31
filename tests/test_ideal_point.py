import numpy as np
from app.algorithms.ideal_point import ideal_point_method
from app.algorithms.point import Point, create_points_from_datapoints


def test_ideal_point_method():
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

    assert all(p in non_dominated_points for p in expected_non_dominated_points)
    assert all(p in expected_non_dominated_points for p in non_dominated_points)
