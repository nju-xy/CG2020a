#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import cg_algorithms as alg
import numpy as np
from PIL import Image

if __name__ == '__main__':
    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    os.makedirs(output_dir, exist_ok=True)

    item_dict = {}
    pen_color = np.zeros(3, np.uint8)
    width = 0
    height = 0
    lineno = 0

    with open(input_file, 'r') as fp:
        # line = fp.readline()
        # while line:
        for line in fp:
            line = line.strip().split(' ')
            lineno = lineno + 1
            n = len(line)
            if line[0] == 'resetCanvas':
                width = int(line[1])
                height = int(line[2])
                item_dict.clear()
            elif line[0] == 'saveCanvas':
                if n != 2:
                    print("第", lineno, "行错误：saveCanvas参数数量错误")
                    continue
                save_name = line[1]
                canvas = np.zeros([height, width, 3], np.uint8)
                canvas.fill(255)
                for item_type, p_list, algorithm, color in item_dict.values():
                    if item_type == 'line':
                        pixels = alg.draw_line(p_list, algorithm)
                        for x, y in pixels:
                            canvas[y, x] = color
                    elif item_type == 'polygon':
                        pixels = alg.draw_polygon(p_list, algorithm)
                        for x, y in pixels:
                            canvas[y, x] = color
                    elif item_type == 'polyline':
                        pixels = alg.draw_polyline(p_list, algorithm)
                        for x, y in pixels:
                            canvas[y, x] = color
                    elif item_type == 'ellipse':
                        pixels = alg.draw_ellipse(p_list)
                        for x, y in pixels:
                            canvas[y, x] = color
                    elif item_type == 'curve':
                        pixels = alg.draw_curve(p_list, algorithm)
                        for x, y in pixels:
                            canvas[y, x] = color
                Image.fromarray(canvas).save(os.path.join(output_dir, save_name + '.bmp'), 'bmp')
            elif line[0] == 'setColor':
                if n != 4:
                    print("第", lineno, "行错误：setColor参数数量错误")
                    continue
                pen_color[0] = int(line[1])
                pen_color[1] = int(line[2])
                pen_color[2] = int(line[3])
            elif line[0] == 'drawLine':
                if n != 7:
                    print("第", lineno, "行错误：drawLine参数数量错误")
                    continue
                item_id = line[1]
                x0 = int(line[2])
                y0 = int(line[3])
                x1 = int(line[4])
                y1 = int(line[5])
                algorithm = line[6]
                if algorithm != 'DDA' and algorithm != 'Bresenham' and algorithm != 'Naive':
                    print("第", lineno, "行错误：不允许的算法：", algorithm)
                else:
                    item_dict[item_id] = ['line', [[x0, y0], [x1, y1]], algorithm, np.array(pen_color)]
            elif line[0] == 'drawPolygon':
                if n < 5 or n % 2 == 0:
                    print("第", lineno, "行错误：drawPolygon参数数量错误")
                    continue
                item_id = line[1]
                t = 2
                p_list = []
                n1 = int((n - 3) / 2)
                algorithm = line[n - 1]
                for i in range(0, n1):
                    p_list.append([int(line[i * 2 + 2]), int(line[i * 2 + 3])])
                if algorithm != 'DDA' and algorithm != 'Bresenham' and algorithm != 'Naive':
                    print("第", lineno, "行错误：不允许的算法：", algorithm)
                else:
                    item_dict[item_id] = ['polygon', p_list, algorithm, np.array(pen_color)]
            elif line[0] == 'drawPolyline':
                if n < 5 or n % 2 == 0:
                    print("第", lineno, "行错误：drawPolyline参数数量错误")
                    continue
                item_id = line[1]
                t = 2
                p_list = []
                n1 = int((n - 3) / 2)
                algorithm = line[n - 1]
                for i in range(0, n1):
                    p_list.append([int(line[i * 2 + 2]), int(line[i * 2 + 3])])
                if algorithm != 'DDA' and algorithm != 'Bresenham' and algorithm != 'Naive':
                    print("第", lineno, "行错误：不允许的算法：", algorithm)
                else:
                    item_dict[item_id] = ['polyline', p_list, algorithm, np.array(pen_color)]
            elif line[0] == 'drawEllipse':
                if n != 6:
                    print("第", lineno, "行错误：drawEllipse参数数量错误")
                    continue
                item_id = line[1]
                x0 = int(line[2])
                y0 = int(line[3])
                x1 = int(line[4])
                y1 = int(line[5])
                item_dict[item_id] = ['ellipse', [[x0, y0], [x1, y1]], "center", np.array(pen_color)]
            elif line[0] == 'drawCurve':
                if n < 5 or n % 2 == 0:
                    print("drawPolygon参数数量错误")
                    continue
                item_id = line[1]
                t = 2
                p_list = []
                n1 = int((n - 3) / 2)
                algorithm = line[n - 1]
                for i in range(0, n1):
                    p_list.append([int(line[i * 2 + 2]), int(line[i * 2 + 3])])
                if algorithm != 'Bezier' and algorithm != 'B-spline':
                    print("第", lineno, "行错误：不允许的算法：", algorithm)
                else:
                    item_dict[item_id] = ['curve', p_list, algorithm, np.array(pen_color)]
            elif line[0] == 'translate':
                if n != 4:
                    print("第", lineno, "行错误：translate参数数量错误")
                    continue
                item_id = line[1]
                dx = int(line[2])
                dy = int(line[3])
                if item_id not in item_dict.keys():
                    print("第", lineno, "行错误：不存在图元", item_id)
                else:
                    p_list = item_dict[item_id][1]
                    item_dict[item_id][1] = alg.translate(p_list, dx, dy)
            elif line[0] == 'rotate':
                if n != 5:
                    print("第", lineno, "行错误：rotate参数数量错误")
                    continue
                item_id = line[1]
                x = int(line[2])
                y = int(line[3])
                r = int(line[4])
                if item_id not in item_dict.keys():
                    print("第", lineno, "行错误：不存在图元", item_id)
                elif item_dict[item_id][0] == 'ellipse':
                    print("第", lineno, "行错误：禁止对椭圆进行旋转")
                else:
                    p_list = item_dict[item_id][1]
                    item_dict[item_id][1] = alg.rotate(p_list, x, y, r)
            elif line[0] == 'scale':
                if n != 5:
                    print("第", lineno, "行错误：scale参数数量错误")
                    continue
                item_id = line[1]
                x = int(line[2])
                y = int(line[3])
                s = float(line[4])
                if item_id not in item_dict.keys():
                    print("第", lineno, "行错误：不存在图元", item_id)
                else:
                    p_list = item_dict[item_id][1]
                    item_dict[item_id][1] = alg.scale(p_list, x, y, s)
            elif line[0] == 'clip':
                if n != 7:
                    print("第", lineno, "行错误：clip参数数量错误")
                    continue
                item_id = line[1]
                x0 = int(line[2])
                y0 = int(line[3])
                x1 = int(line[4])
                y1 = int(line[5])
                algorithm = line[6]
                if algorithm != 'Cohen-Sutherland' and algorithm != 'Liang-Barsky':
                    print("第", lineno, "行错误：不存在算法", algorithm)
                elif item_id not in item_dict.keys():
                    print("第", lineno, "行错误：不存在图元", item_id)
                elif item_dict[item_id][0] != 'line':
                    print("第", lineno, "行错误：禁止对线段以外的图元进行裁剪")
                else:
                    p_list = item_dict[item_id][1]
                    ret = alg.clip(p_list, x0, y0, x1, y1, algorithm)
                    if ret:
                        item_dict[item_id][1] = ret
                    else:
                        del item_dict[item_id]
            else:
                print("第", lineno, "行错误：未知的指令")
            # ...
            # line = fp.readline()
