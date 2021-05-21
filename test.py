import random
import unittest
import algorithm
from typing import List, Tuple


class SmallestEnclosingCircleTest(unittest.TestCase):
    """Basic tests for smallest enclosing circle algorithm."""

    _EPSILON = 1e-12  # epsilon used to compare if results are comparatively equal

    @staticmethod
    def _make_random_points(n: int) -> List[Tuple[float, float]]:
        """Create random input of points either discretely or normally."""

        if random.random() < 0.2:  # Discrete lattice (to have a chance of duplicated points)
            return [(random.randrange(10), random.randrange(10)) for _ in range(n)]
        else:  # Gaussian distribution
            return [(random.gauss(0, 1), random.gauss(0, 1)) for _ in range(n)]

    def test_matching_naive_algorithm(self) -> None:
        """Check that current algorithm gives the same results as the naive approach."""

        trials = 1000
        for _ in range(trials):
            points = self._make_random_points(random.randint(1, 30))
            reference = algorithm.smallest_enclosing_circle_naive(points)
            actual = algorithm.make_circle(points)
            self.assertAlmostEqual(actual[0], reference[0], delta=self._EPSILON)
            self.assertAlmostEqual(actual[1], reference[1], delta=self._EPSILON)
            self.assertAlmostEqual(actual[2], reference[2], delta=self._EPSILON)

    def test_translation(self) -> None:
        """Check that if initial points are moved around (translated linearly) the result won't change.

         Points are moved by gaussian random shift with lambda=0 and sigma=1."""

        trials = 100
        checks = 10
        for _ in range(trials):
            points = self._make_random_points(random.randint(1, 300))
            reference = algorithm.make_circle(points)

            for _ in range(checks):
                dx = random.gauss(0, 1)
                dy = random.gauss(0, 1)
                newpoints = [(x + dx, y + dy) for (x, y) in points]

                translated = algorithm.make_circle(newpoints)
                self.assertAlmostEqual(translated[0], reference[0] + dx, delta=self._EPSILON)
                self.assertAlmostEqual(translated[1], reference[1] + dy, delta=self._EPSILON)
                self.assertAlmostEqual(translated[2], reference[2], delta=self._EPSILON)

    def test_scaling(self) -> None:
        """Check that if initial points are moved around (scaled) the result won't change.

        Points are scaled by having coordinated multiplied by random gaussian shift with lambda=0 and sigma=1."""

        trials = 100
        checks = 10
        for _ in range(trials):
            points = self._make_random_points(random.randint(1, 300))
            reference = algorithm.make_circle(points)

            for _ in range(checks):
                scale = random.gauss(0, 1)
                newpoints = [(x * scale, y * scale) for x, y in points]

                scaled = algorithm.make_circle(newpoints)
                self.assertAlmostEqual(scaled[0], reference[0] * scale, delta=self._EPSILON)
                self.assertAlmostEqual(scaled[1], reference[1] * scale, delta=self._EPSILON)
                self.assertAlmostEqual(scaled[2], reference[2] * abs(scale), delta=self._EPSILON)


if __name__ == "__main__":
    unittest.main()
