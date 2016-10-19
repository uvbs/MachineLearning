import numpy as np
import matplotlib.pyplot as plt


class GradientDecent:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.m = len(self.x)
        self.a = 10.0
        self.b = 2.0
        self.c = 0.0
        self.learn_rate = 0.0000000001

    def algorithm(self, x):
        return self.a * (x ** 2) + self.b * x + self.c

    def costfuntion(self):
        J = 0
        for i in range(self.m):
            J += (self.algorithm(self.x[i]) - self.y[i]) ** 2
        return (1.0 / (2 * self.m)) * J

    def update(self):
        temp_a = self.a
        temp_b = self.b
        temp_c = self.c
        partial_of_a = 0
        partial_of_b = 0
        partial_of_c = 0
        for i in range(self.m):
            partial_of_a += 2 * (self.algorithm(x[i] - y[i])) * (self.x[i] ** 2)
            partial_of_b += 2 * (self.algorithm(x[i] - y[i])) * self.x[i]
            partial_of_c += 2 * (self.algorithm(x[i] - y[i])) * 1
        self.a = temp_a - 1.0 / self.m * self.learn_rate * partial_of_a
        self.b = temp_b - 1.0 / self.m * self.learn_rate * partial_of_b
        self.c = temp_c - 1.0 / self.m * self.learn_rate * partial_of_c

    def plot_algorithm(self):
        plt.figure(1)
        x = np.linspace(0, 10, 100)
        y = [self.algorithm(_) for _ in x]
        plt.plot(x, y, c='r')

    def scatter_data(self):
        plt.figure(1)
        plt.scatter(self.x, self.y, s=1)


def getdata():
    x = []
    y = []
    dataset = [(_.replace("\n", "")).strip().split() for _ in open("data.txt", "r")]
    while dataset:
        data = dataset.pop()
        y.append(data.pop())
        x.append(data.pop())
    x = map(float, x)
    y = map(float, y)
    return x, y


class main():
    def __init__(self, x, y):
        self.g = GradientDecent(x, y)

    def run(self):
        a = self.g.costfuntion()
        b = self.g.costfuntion()
        while a - b >= 0:
            a = self.g.costfuntion()
            print a
            self.g.update()
            b = self.g.costfuntion()
        print self.g.a, self.g.b, self.g.c
        self.g.plot_algorithm()
        self.g.scatter_data()
        ax = plt.subplot(111)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Apply GradientDecent")
        plt.sca(ax)
        plt.show()


if __name__ == '__main__':
    x, y = getdata()
    main = main(x, y)
    main.run()
