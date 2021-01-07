import matplotlib.pyplot as plt 
import numpy as np
import math
import random


def lsm_line(x, y):
    n = len(x)
    sx = np.sum(x)
    sy = np.sum(y)
    sxy = np.sum(x * y)
    sxx = np.sum(x * x)
    
    a = (n * sxy - sx * sy) / (n * sxx - (sx * sx))
    b = (sy - a * sx) / n

    return lambda _x, a = a, b = b: a * _x + b, [a, b]


def lsm_parabola(x, y):
    n = len(x)
    sx = 2 * np.sum(x)
    x2 = x * x
    x3 = x2 * x
    x4 = x3 * x
    sx = np.sum(x)
    sy = np.sum(y)
    sxy = np.sum(x * y)
    sx2 = np.sum(x2)
    sx3 = np.sum(x3)
    sx4 = np.sum(x4)
    syx2 = np.sum(y * x2)

    mat = np.array([
        [sx4, sx3, sx2], # a
        [sx3, sx2, sx], # b
        [sx2, sx, n] # c
    ])

    vec = np.array([syx2, sxy, sy])

    a, b, c = np.linalg.solve(mat, vec)

    return lambda _x, a = a, b = b, c = c: a * _x * _x + b * _x + c, [a, b, c]

def fault(f, _x, _y):
    fl = 0
    for x, y in zip(_x, _y):
        fl += (y - f(x)) ** 2

    return fl / len(_x)


def draw_func(f, start, end, res = 100):
    x = np.linspace(start, end, res)
    y = np.array([f(_x) for _x in x])
    return x, y


if __name__ == "__main__":

    x = np.array([
        1.92,
        2.84,
        3.76,
        4.68,
        5.60,
        6.52,
        7.44,
        8.36
    ])

    y = np.array([
        1.48,
        2.69,
        4.07,
        5.67,
        7.42,
        9.35,
        11.36,
        13.54
    ])


    plt.style.use("ggplot")

    ax1 : plt.Axes
    ax2 : plt.Axes
    fig, (ax1, ax2) = plt.subplots(2, 1)

    ax1.set_title("$y = ax + b$")
    ax2.set_title("$y = ax^2 + bx + c$")

    ax1.plot(x, y, " o", c = "b", label = "заданные точки")
    ax2.plot(x, y, " o", c = "b", label = "заданные точки")

    f_line, line_p = lsm_line(x, y)
    f_parabola, parabola_p = lsm_parabola(x, y)

    ax1.plot(*draw_func(f_line, x[0], x[-1], 100), label = "МНК линия")
    ax2.plot(*draw_func(f_parabola, x[0], x[-1], 100), label = "МНК парабола")

    a, b = line_p
    ax1.text(0.05, 0.9, f"$y = {a:.5f}x {b:+.5f}$\n$\Delta = {fault(f_line, x, y)}$", transform = ax1.transAxes, verticalalignment='top', bbox = {"alpha" : 0.5})

    a, b, c = parabola_p
    ax2.text(0.05, 0.9, f"$y = {a:.5f}x^2 {b:+.5f}x {c:+.5f}$\n$\Delta = {fault(f_parabola, x, y)}$", transform = ax2.transAxes, verticalalignment='top', bbox = {"alpha" : 0.5})

    ax1.legend(loc = "lower right")
    ax2.legend(loc = "lower right")

    plt.show()
