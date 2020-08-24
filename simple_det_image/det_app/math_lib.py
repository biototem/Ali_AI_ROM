import numpy as np


def calc_abc_from_line_2d(x0, y0, x1, y1):
    a = y0 - y1
    b = x1 - x0
    c = x0*y1 - x1*y0
    return a, b, c


def get_line_cross_point(line1, line2):
    # x1y1x2y2
    a0, b0, c0 = calc_abc_from_line_2d(*line1)
    a1, b1, c1 = calc_abc_from_line_2d(*line2)
    D = a0 * b1 - a1 * b0
    if D == 0:
        return None
    x = (b0 * c1 - b1 * c0) / D
    y = (a1 * c0 - a0 * c1) / D
    # print(x, y)
    return x, y


def calc_angle_2(v1, v2):
    '''
    支持大于180度计算
    :param v1:
    :param v2:
    :return:
    '''
    r = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1, 2) * np.linalg.norm(v2, 2)))
    deg = r * 180 / np.pi

    a1 = np.array([*v1, 0])
    a2 = np.array([*v2, 0])

    a3 = np.cross(a1, a2)

    if np.sign(a3[2]) > 0:
        deg = 360 - deg

    return deg