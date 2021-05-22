import random
from typing import List, Tuple, Optional

_EPSILON = 1e-14


def _hypotenuse(base: float, side: float) -> float:
    """Calculate the hypotenuse with other two sides known."""

    return (base ** 2 + side ** 2) ** 0.5


def make_circle(points: List[Tuple[float, float]]) -> Tuple[float, float, float]:
    """Execute the main algorithm to find the smallest enclosing circle for specified 2D points."""

    # Convert to float and randomize order
    shuffled = [(float(x), float(y)) for x, y in points]
    random.shuffle(shuffled)

    # Progressively add points to circle or recompute circle
    c = None
    for (i, p) in enumerate(shuffled):
        if c is None or not is_in_circle(c, p):
            c = _make_circle_one_point(shuffled[: i + 1], p)

    return c


def _make_circle_one_point(points: List[Tuple[float, float]], p: Tuple[float, float]) -> Tuple[float, float, float]:
    """Find the smallest enclosing circle knowing one boundary point."""

    c = (p[0], p[1], 0.0)
    for (i, q) in enumerate(points):
        if not is_in_circle(c, q):
            if c[2] == 0.0:
                c = make_circle_by_diameter_points(p, q)
            else:
                c = _make_circle_two_points(points[: i + 1], p, q)

    return c


def _make_circle_two_points(points: List[Tuple[float, float]], p: Tuple[float, float], q: Tuple[float, float]) -> \
        Tuple[float, float, float]:
    """Find the smallest enclosing circle knowing two boundary points."""

    circ = make_circle_by_diameter_points(p, q)
    left = None
    right = None
    px, py = p
    qx, qy = q

    # For each point not in the two-point circle
    for r in points:
        if is_in_circle(circ, r):
            continue

        # Form a circumscribed circle and classify it on left or right side
        cross = _cross_product(px, py, qx, qy, r[0], r[1])
        c = make_circumscribed_circle(p, q, r)
        if c is None:
            continue
        elif cross > 0.0 and (
                left is None or _cross_product(px, py, qx, qy, c[0], c[1]) > _cross_product(px, py, qx, qy, left[0],
                                                                                            left[1])):
            left = c
        elif cross < 0.0 and (
                right is None or _cross_product(px, py, qx, qy, c[0], c[1]) < _cross_product(px, py, qx, qy, right[0],
                                                                                             right[1])):
            right = c

    # Select which circle to return
    if left is None and right is None:
        return circ
    elif left is None:
        return right
    elif right is None:
        return left
    else:
        return left if (left[2] <= right[2]) else right


def make_circumscribed_circle(a: Tuple[float, float], b: Tuple[float, float], c: Tuple[float, float]) -> \
        Optional[Tuple[float, float, float]]:
    """Make circle out of three points."""

    ox = (min(a[0], b[0], c[0]) + max(a[0], b[0], c[0])) / 2
    oy = (min(a[1], b[1], c[1]) + max(a[1], b[1], c[1])) / 2
    ax = a[0] - ox
    ay = a[1] - oy
    bx = b[0] - ox
    by = b[1] - oy
    cx = c[0] - ox
    cy = c[1] - oy
    d = (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by)) * 2.0
    if d == 0.0:
        return None

    x = ox + ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    y = oy + ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    ra = _hypotenuse(x - a[0], y - a[1])
    rb = _hypotenuse(x - b[0], y - b[1])
    rc = _hypotenuse(x - c[0], y - c[1])

    return x, y, max(ra, rb, rc)


def is_in_circle(c: Tuple[float, float, float], p: Tuple[float, float]) -> bool:
    """Check if point is inside circle."""

    return c is not None and _hypotenuse(p[0] - c[0], p[1] - c[1]) <= c[2] + _EPSILON


def make_circle_by_diameter_points(a: Tuple[float, float], b: Tuple[float, float]) -> Tuple[float, float, float]:
    """Knowing two points create a circle that will have them on its diameter."""

    cx = (a[0] + b[0]) / 2
    cy = (a[1] + b[1]) / 2
    r0 = _hypotenuse(cx - a[0], cy - a[1])
    r1 = _hypotenuse(cx - b[0], cy - b[1])

    return cx, cy, max(r0, r1)


def _cross_product(x0: float, y0: float, x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculate doubled signed area of the triangle specified by entry points."""

    return (x1 - x0) * (y2 - y0) - (y1 - y0) * (x2 - x0)


def smallest_enclosing_circle_naive(points: List[Tuple[float, float]]) -> Optional[Tuple[float, float, float]]:
    """Returns the smallest enclosing circle in O(n^4) time using the naive algorithm."""

    # Degenerate cases
    if len(points) == 0:
        return None
    elif len(points) == 1:
        return points[0][0], points[0][1], 0

    # Try all unique pairs
    result = None
    for i in range(len(points)):
        p = points[i]
        for j in range(i + 1, len(points)):
            q = points[j]
            c = make_circle_by_diameter_points(p, q)
            if (result is None or c[2] < result[2]) and \
                    all(is_in_circle(c, r) for r in points):
                result = c
    if result is not None:
        return result

    # Try all unique triples
    for i in range(len(points)):
        p = points[i]
        for j in range(i + 1, len(points)):
            q = points[j]
            for k in range(j + 1, len(points)):
                r = points[k]
                c = make_circumscribed_circle(p, q, r)
                if c is not None and (result is None or c[2] < result[2]) and \
                        all(is_in_circle(c, s) for s in points):
                    result = c

    if result is None:
        raise AssertionError()

    return result
