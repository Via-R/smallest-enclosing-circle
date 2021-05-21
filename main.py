from typing import List

import algorithm
import matplotlib.pyplot as plt
import random
from scipy.stats import truncnorm


def get_truncated_normal(mean: float = 0, sd: float = 1, low: float = 0, upp: float = 10):
    return truncnorm((low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)


def read_from_file():
    with open("input.txt", "r") as f:
        point_lines = f.readlines()
    output = []
    for point_line in point_lines:
        point = [float(p) for p in point_line.strip("\n").split()]
        output.append(point)

    return output


def draw(points, circle):
    xs = []
    ys = []
    for p in points:
        xs.append(p[0])
        ys.append(p[1])

    plt.figure(figsize=(6, 6))

    plt.plot(xs, ys, "og")
    plt.xlim(-1.5, 1.5)
    plt.ylim(-1.5, 1.5)

    circle_img = plt.Circle((circle[0], circle[1]), circle[2], color='r', fill=False)
    plt.gca().add_patch(circle_img)

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Enclosing circle')
    plt.show()


def generate_input(points_amount: int = 88) -> List[List[float]]:
    generator = get_truncated_normal(mean=0, sd=0.3, low=-1, upp=1)
    return [[generator.rvs(), generator.rvs()] for _ in range(points_amount)]


def main():
    # input_source = input(
    #     "Please select input source (type 1 or 2):\n1) input.txt file\n2) random generation\nChoice: "
    # ).lower()
    # if input_source == "1":
    #     points = read_from_file()
    # elif input_source == "2":
    #     points = generate_input()
    # else:
    #     print("Invalid choice, please try again")
    #     return
    points = generate_input()
    circle = algorithm.make_circle(points)
    draw(points, circle)


if __name__ == "__main__":
    main()
