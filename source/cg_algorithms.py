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
            for y in range(y0, y1 + 1):
                result.append([x0, y])
        else:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1 - y0) / (x1 - x0)
            for x in range(x0, x1 + 1):
                result.append([x, int(y0 + k * (x - x0))])
    elif algorithm == 'DDA':
        if x0 == x1:
            for y in range(min(y0, y1), max(y0, y1) + 1):
                result.append([x0, y])
        elif y0 == y1:
            for x in range(min(x0, x1), max(x0, x1) + 1):
                result.append([x, y0])
        else:
            k = (y1 - y0) / (x1 - x0)
            if abs(k) <= 1:
                if x0 > x1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                y = y0
                for x in range(x0, x1 + 1):
                    y = y + k
                    result.append([int(x), int(y)])
            else:
                if y0 > y1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                x = x0
                for y in range(y0, y1 + 1):
                    x = x + 1 / k
                    result.append([int(x), int(y)])
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
            y = y0
            p = 2 * dy - dx
            result.append([x0, y0])
            for x in range(x0 + 1, x1 + 1):
                if p < 0:
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
            x = x0
            p = 2 * dx - dy
            result.append([x0, y0])
            for y in range(y0 + 1, y1 + 1):
                if p < 0:
                    p = p + dx2
                else:  # p > 0
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


def draw_ellipse(p_list):
    """绘制椭圆（采用中点圆生成算法）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    x0, y0, x1, y1 = p_list[0][0], p_list[0][1], p_list[1][0], p_list[1][1],
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    rx, ry = abs(x1 - x0) / 2, abs(y1 - y0) / 2
    # print(cx, cy, rx, ry)
    # 椭圆方程为 (x - cx)^2 / rx^2 + (y - cy)^2 / ry^2 = 1 (无论焦点在x轴y轴)
    x, y = 0, ry
    result.append([int(cx + x), int(cy + y)])
    p1 = ry * ry - rx * rx * ry + rx * rx / 4
    while rx * rx * y > ry * ry * x:
        if p1 < 0:
            x, y = x + 1, y
            p1 = p1 + 2 * ry * ry * x + ry * ry
        else:
            x, y = x + 1, y - 1
            p1 = p1 + 2 * ry * ry * x - 2 * rx * rx * y + ry * ry
        result.append([int(cx + x), int(cy + y)])
        result.append([int(cx - x), int(cy + y)])
        result.append([int(cx + x), int(cy - y)])
        result.append([int(cx - x), int(cy - y)])
    p2 = ry * ry * (x + 1/2) * (x + 1/2) + rx * rx * (y - 1) * (y - 1) - rx * rx * ry * ry
    while y > 0:
        if p2 > 0:
            x, y = x, y - 1
            p2 = p2 - 2 * rx * rx * y + rx * rx
        else:
            x, y = x + 1, y - 1
            p2 = p2 + 2 * ry * ry * x - 2 * rx * rx * y + rx * rx
        result.append([int(cx + x), int(cy + y)])
        result.append([int(cx - x), int(cy + y)])
        result.append([int(cx + x), int(cy - y)])
        result.append([int(cx - x), int(cy - y)])
    return result


def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    # result = []
    # if algorithm == 'Bezier':
    #     for i in range(len(p_list)):
    #
    # elif algorithm == 'B-spline':
    # return result



def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
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
    pass


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    pass


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
    pass
