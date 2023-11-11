from .point import Point
from numpy import zeros_like, norm



def estimate_ideal_point(points: list[Point]) -> Point:
    y = zeros_like(points[0].x)
    for i in range(points[0].dim):
        y[i] = min(p.x[i] for p in points)
    return Point(y)

def scalarisation(
        points: list[Point], 
        ideal_point: [Point | None] = None,
        metric: callable = norm,
        ) -> Point:
    if ideal_point is None: 
        ideal_point = estimate_ideal_point(points)
    return min(points, key=lambda p: metric(p.x-ideal_point.x))
