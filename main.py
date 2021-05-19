import algorithm
import matplotlib.pyplot as plt


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
    plt.xlim(-0.5, 1.5)
    plt.ylim(-0.5, 1.5)

    circle_img = plt.Circle((circle[0], circle[1]), circle[2], color='r', fill=False)
    plt.gca().add_patch(circle_img)

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Enclosing circle')
    plt.show()


def main():
    points = read_from_file()
    circle = algorithm.make_circle(points)
    draw(points, circle)


if __name__ == "__main__":
    main()
