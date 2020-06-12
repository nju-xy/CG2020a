#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 本文件只允许依赖math库
import math


def draw_line(p_list, algorithm):
    """绘制线段

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'，此处的'Naive'仅作为示例，测试时不会出现
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = []
    if algorithm == 'Naive':
        if x0 == x1:
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            for y in range(y0, y1 + 1):
                result.append([x0, y])
        else:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1 - y0) / (x1 - x0)
            for x in range(x0, x1 + 1):
                result.append([x, int(y0 + k * (x - x0))])
    elif algorithm == 'DDA':
        if y1 == y0 and x1 == x0:
            # 两个端点重合，可能不算线段，但是保险起见我特判一下吧
            result.append([x0, y0])
        elif abs(y1 - y0) <= abs(x1 - x0):
            # 若线段斜率绝对值小于等于1，则x方向取样
            k = (y1 - y0) / (x1 - x0)
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            y = y0
            for x in range(x0, x1 + 1):
                result.append([int(x), int(y)])
                y = y + k
        else:  # abs(y1 - y0) > abs(x1 - x0)
            # 若线段斜率绝对值大于1(或者斜率不存在)， 则y方向取样
            k = (x1 - x0) / (y1 - y0)
            # 这里的k实际上是斜率的倒数
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            x = x0
            for y in range(y0, y1 + 1):
                result.append([int(x), int(y)])
                x = x + k
    elif algorithm == 'Bresenham':
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        if dx == 0:
            for y in range(min(y0, y1), max(y0, y1) + 1):
                result.append([x0, y])
        elif dy == 0:
            for x in range(min(x0, x1), max(x0, x1) + 1):
                result.append([x, y0])
        elif dx == dy:  # 对角线
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            if y0 < y1:
                uy = 1
            else:
                uy = -1
            for x in range(0, dx + 1):
                result.append([x0 + x, y0 + uy * x])
        elif dy < dx:  # |m| < 1
            dx2, dy2 = 2 * dx, 2 * dy
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            # 确保 x0 < x1
            if y0 < y1:
                uy = 1
            else:
                uy = -1
            # uy是y更新的增量方向
            y = y0
            p = 2 * dy - dx
            result.append([x0, y0])
            for x in range(x0 + 1, x1 + 1):
                if p <= 0:
                    p = p + dy2
                else:  # p > 0
                    y = y + uy
                    p = p + dy2 - dx2
                result.append([x, y])
        else:  # |m| > 1
            dx2, dy2 = 2 * dx, 2 * dy
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            # 确保 y0 < y1
            if x0 < x1:
                ux = 1
            else:
                ux = -1
            # ux是x更新的增量方向
            x = x0
            p = 2 * dx - dy  # 决策参数p
            result.append([x0, y0])
            for y in range(y0 + 1, y1 + 1):
                if p < 0:
                    p = p + dx2
                else:  # p >= 0
                    x = x + ux
                    p = p + dx2 - dy2
                result.append([x, y])
    return result


def draw_polygon(p_list, algorithm):
    """绘制多边形

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    for i in range(len(p_list)):
        line = draw_line([p_list[i - 1], p_list[i]], algorithm)
        result += line
    return result


def draw_polyline(p_list, algorithm):
    """绘制折线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    for i in range(1, len(p_list)):
        line = draw_line([p_list[i - 1], p_list[i]], algorithm)
        result += line
    return result


def draw_ellipse(p_list):
    """绘制椭圆（采用中点圆生成算法）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    # print(p_list)
    result = []
    x0, y0, x1, y1 = p_list[0][0], p_list[0][1], p_list[1][0], p_list[1][1]
    if y0 == y1:
        # print("嘤")
        return draw_line(p_list, 'Bresenham')
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    rx, ry = abs(x1 - x0) / 2, abs(y1 - y0) / 2
    # 椭圆方程为 (x - cx)^2 / rx^2 + (y - cy)^2 / ry^2 = 1 (无论焦点在x轴y轴)
    x, y = 0, ry
    result.append([int(cx + x), int(cy + y)])
    result.append([int(cx - x), int(cy - y)])
    p1 = ry * ry - rx * rx * ry + rx * rx / 4
    while rx * rx * y > ry * ry * x:
        # print('1:', x, y, p1)
        result.append([int(cx + x), int(cy + y)])
        result.append([int(cx - x), int(cy + y)])
        result.append([int(cx + x), int(cy - y)])
        result.append([int(cx - x), int(cy - y)])
        if p1 < 0:
            x, y = x + 1, y
            p1 = p1 + 2 * ry * ry * x + ry * ry
        else:
            x, y = x + 1, y - 1
            p1 = p1 + 2 * ry * ry * x - 2 * rx * rx * y + ry * ry
    p2 = ry * ry * (x + 1 / 2) * (x + 1 / 2) + rx * rx * (y - 1) * (y - 1) - rx * rx * ry * ry
    while y >= 0:
        # print('2:', x, y, p2)
        result.append([int(cx + x), int(cy + y)])
        result.append([int(cx - x), int(cy + y)])
        result.append([int(cx + x), int(cy - y)])
        result.append([int(cx - x), int(cy - y)])
        if p2 > 0:
            x, y = x, y - 1
            p2 = p2 - 2 * rx * rx * y + rx * rx
        else:
            x, y = x + 1, y - 1
            p2 = p2 + 2 * ry * ry * x - 2 * rx * rx * y + rx * rx
    while x <= rx:
        result.append([int(cx + x), int(cy)])
        result.append([int(cx - x), int(cy)])
        x = x + 1
    return result


def draw_curve(p_list, algorithm, n_steps=1000):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :param n_steps: (int) 采样的点的个数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    n = len(p_list) - 1  # n次Bezier曲线, n+1个控制点
    if algorithm == "Bezier":
        # u = 0
        # step = 0.00005
        # step = 1 / n_steps  # 默认0.001
        points = []
        # p = []
        # for i in range(0, n + 1):
        #     p.append([p_list[i][0], p_list[i][1]])
        # while u <= 1:
        for t in range(0, n_steps + 1):
            u = t / n_steps
            p = []
            for i in range(0, n + 1):
                p.append([p_list[i][0], p_list[i][1]])
            # 使用de Casteljau算法,
            # P[i][r] = (1 - u) P[i][r - 1] + u P[i + 1][r - 1]
            # 曲线上的点为P(u) = P[0][n]
            for r in range(1, n + 1):
                for i in range(0, n - r + 1):
                    p[i][0] = (1 - u) * p[i][0] + u * p[i + 1][0]
                    p[i][1] = (1 - u) * p[i][1] + u * p[i + 1][1]
            # u = u + step
            # result.append([int(p[0][0]), int(p[0][1])])
            if len(points) == 0:
                result.append([int(p[0][0]), int(p[0][1])])
            else:
                result += draw_line([points[-1], [int(p[0][0]), int(p[0][1])]], 'Bresenham')
            points.append([int(p[0][0]), int(p[0][1])])
        # print(result)
        return result
    elif algorithm == "B-spline":  # 三次均匀B样条曲线, 4阶. k = 3
        # step = 0.0001
        if n < 3:
            return []
        step = (n - 2) / n_steps  # 默认1000
        u = 3
        points = []
        while u <= n + 1:
            # P(u) = sum_{i=0}^n P[i]B[i][4](u), u in [k, n+1]
            # 首先计算B[i][1]: (0 <= i <= n + k) 即0 <= i <= n + 3
            # if u in [i, i+1), B[i][1] = 1; else B[i][1] = 0
            b = []
            for i in range(0, n + 4):
                if i <= u < i + 1:
                    b.append(1)
                else:
                    b.append(0)
            # k > 1时, B[i][k](u) = (u-i)/(k-1) N[i][k-1](u)
            #                       + (i+k-u)/(k-1) N[i+1][k-1](u)
            # 最终求得 B[i][4](u), 0 <= i <= n
            for k in range(2, 5):
                for i in range(0, n + 5 - k):
                    b[i] = b[i] * (u - i) / (k - 1) + b[i + 1] * (i + k - u) / (k - 1)
            x, y = 0, 0
            for i in range(0, n + 1):
                x = x + p_list[i][0] * b[i]
                y = y + p_list[i][1] * b[i]
            u = u + step
            # result.append([int(x), int(y)])
            if len(points) == 0:
                result.append([int(x), int(y)])
            else:
                result += draw_line([points[-1], [int(x), int(y)]], 'Bresenham')
            points.append([int(x), int(y)])
        return result


def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    # 将要平移的图元的所有控制点都进行平移
    # 对于点(x, y), 平移(dx, dy)的结果为(x+dx, y+dy)
    result = []
    for [x, y] in p_list:
        x, y = x + dx, y + dy
        result.append([x, y])
    return result


def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    # 将要平移的图元（非椭圆）的所有控制点都进行旋转
    # 对于点(x1, y1), 绕点(x, y)旋转r°的结果为
    # (x+(x1-x)*cos(r)-(y1-y)*sin(r), y+(x1-x)*sin(r)+(y1-y)*cos(r))
    result = []
    r = r * math.pi / 180
    for [x1, y1] in p_list:
        x1, y1 = x + (x1 - x) * math.cos(r) - (y1 - y) * math.sin(r), \
                 y + (x1 - x) * math.sin(r) + (y1 - y) * math.cos(r)
        result.append([int(x1), int(y1)])
    return result


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    # 将要平移的图元的所有控制点都进行缩放。
    # 对于点(x, y), 相对于缩放中心(x_f, y_f)以缩放倍数s缩放（一致缩放）的结果为(x_1,y_1)，其中
    # x_1=x_f+(x-x_f)* s = x*s+x_f*(1-s)
    # y_1=y_f+(y-y_f)* s = y*s+y_f*(1-s)
    result = []
    for [x1, y1] in p_list:
        x1, y1 = x + (x1 - x) * s, y + (y1 - y) * s
        result.append([int(x1), int(y1)])
    return result


def clip(p_list, x_min, y_min, x_max, y_max, algorithm):
    """线段裁剪

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param x_min: 裁剪窗口左上角x坐标
    :param y_min: 裁剪窗口左上角y坐标
    :param x_max: 裁剪窗口右下角x坐标
    :param y_max: 裁剪窗口右下角y坐标
    :param algorithm: (string) 使用的裁剪算法，包括'Cohen-Sutherland'和'Liang-Barsky'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1]]) 裁剪后线段的起点和终点坐标
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    if algorithm == "Cohen-Sutherland":
        pos0 = (x0 < x_min) + ((x0 > x_max) << 1) + ((y0 < y_min) << 2) + ((y0 > y_max) << 3)
        pos1 = (x1 < x_min) + ((x1 > x_max) << 1) + ((y1 < y_min) << 2) + ((y1 > y_max) << 3)
        if pos0 == 0 and pos1 == 0:
            return p_list
        elif pos0 & pos1 != 0:
            return []
        else:  # 依次检查和每个边界的交点
            # print(pos0, pos1)
            if pos0 & 1:  # 左(x1 != x0)
                y0 = y0 + (y1 - y0) * (x_min - x0) / (x1 - x0)
                x0 = x_min
            elif pos0 & 2:  # 右(x1 != x0)
                y0 = y0 + (y1 - y0) * (x_max - x0) / (x1 - x0)
                x0 = x_max
            pos0 = (x0 < x_min) + ((x0 > x_max) << 1) + ((y0 < y_min) << 2) + ((y0 > y_max) << 3)
            if pos0 & 8:  # 上(y1 != y0)
                x0 = x0 + (x1 - x0) * (y_max - y0) / (y1 - y0)
                y0 = y_max
            elif pos0 & 4:  # 下(y1 != y0)
                x0 = x0 + (x1 - x0) * (y_min - y0) / (y1 - y0)
                y0 = y_min
            pos0 = (x0 < x_min) + ((x0 > x_max) << 1) + ((y0 < y_min) << 2) + ((y0 > y_max) << 3)

            # 另一个端点
            if pos0 == 0 and pos1 == 0:
                return [[int(x0), int(y0)], [int(x1), int(y1)]]
            elif pos0 & pos1 != 0:
                return []
            if pos1 & 1:  # 左(x1 != x0)
                y1 = y0 + (y1 - y0) * (x_min - x0) / (x1 - x0)
                x1 = x_min
            elif pos1 & 2:  # 右(x1 != x0)
                y1 = y0 + (y1 - y0) * (x_max - x0) / (x1 - x0)
                x1 = x_max
            pos1 = (x1 < x_min) + ((x1 > x_max) << 1) + ((y1 < y_min) << 2) + ((y1 > y_max) << 3)
            if pos1 & 8:  # 上(y1 != y0)
                x1 = x0 + (x1 - x0) * (y_max - y0) / (y1 - y0)
                y1 = y_max
            elif pos1 & 4:  # 下(y1 != y0)
                x1 = x0 + (x1 - x0) * (y_min - y0) / (y1 - y0)
                y1 = y_min
            # print(x0, y0, x1, y1)
            return [[int(x0), int(y0)], [int(x1), int(y1)]]
    elif algorithm == "Liang-Barsky":
        dx, dy = x0 - x1, y0 - y1
        # 裁剪条件:
        # x_min <= x1 + u dx <= x_max
        # y_min <= y1 + u dy <= y_max
        p = [-dx, dx, -dy, dy]
        q = [x1 - x_min, x_max - x1, y1 - y_min, y_max - y1]
        if p[0] == 0:  # 和裁剪边界平行, 即p[1] == 0
            assert (dy != 0)
            if q[0] < 0 or q[1] < 0:  # 完全在边界外
                return []
            else:  # 进一步判断
                u1, u2 = q[2] / p[2], q[3] / p[3]
                u1, u2 = min(u1, u2), max(u1, u2)
                u1, u2 = max(0, u1), min(1, u2)
                if u1 > u2:
                    return []
                return [[int(x1 + u1 * dx), int(y1 + u1 * dy)], [int(x1 + u2 * dx), int(y1 + u2 * dy)]]
        if p[2] == 0:  # 和裁剪边界平行, 即p[3] == 0
            if q[2] < 0 or q[3] < 0:  # 完全在边界外
                return []
            else:  # 进一步判断
                u1, u2 = q[0] / p[0], q[1] / p[1]
                u1, u2 = min(u1, u2), max(u1, u2)
                u1, u2 = max(0, u1), min(1, u2)
                if u1 > u2:
                    return []
                return [[int(x1 + u1 * dx), int(y1 + u1 * dy)], [int(x1 + u2 * dx), int(y1 + u2 * dy)]]
        u1, u2 = 0, 1
        for k in range(0, 4):
            if p[k] < 0:
                u1 = max(q[k] / p[k], u1)
            elif p[k] > 0:
                u2 = min(q[k] / p[k], u2)
        if u1 > u2:
            return []
        else:
            return [[int(x1 + u1 * dx), int(y1 + u1 * dy)], [int(x1 + u2 * dx), int(y1 + u2 * dy)]]
