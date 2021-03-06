#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import math
import cg_algorithms as alg
from typing import Optional
from PyQt5.QtWidgets import (
    QFileDialog,
    QInputDialog,
    QColorDialog,
    QApplication,
    QMainWindow,
    qApp,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QListWidget,
    QHBoxLayout,
    QWidget,
    QStyleOptionGraphicsItem)
from PyQt5.QtGui import QPainter, QMouseEvent, QColor, QPen, QTransform
from PyQt5.QtCore import QRectF, Qt


class MyCanvas(QGraphicsView):
    """
    画布窗体类，继承自QGraphicsView，采用QGraphicsView、QGraphicsScene、QGraphicsItem的绘图框架
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.main_window = None
        self.list_widget = None
        self.item_dict = {}
        self.selected_id = ''

        self.action_stack = []
        self.status = ''
        self.drawing = 0
        self.temp_algorithm = ''
        self.temp_id = ''
        self.temp_item = None
        self.assist_item = None
        self.double_click = 0
        self.pen_color = QColor(0, 0, 0)
        self.pen_width = 1

    def start_draw_line(self, algorithm):
        if self.drawing != 0:
            return
        self.status = 'line'
        self.temp_algorithm = algorithm
        # self.temp_id = item_id

    def start_draw_polygon(self, algorithm):
        if self.drawing != 0:
            return
        self.status = 'polygon'
        self.temp_algorithm = algorithm
        # self.temp_id = item_id

    def start_draw_ellipse(self, algorithm):
        if self.drawing != 0:
            return
        self.status = 'ellipse'
        self.temp_algorithm = algorithm
        # self.temp_id = item_id

    def start_draw_curve(self, algorithm):
        if self.drawing != 0:
            return
        self.status = 'curve'
        self.temp_algorithm = algorithm
        # self.temp_id = item_id

    def start_draw_polyline(self, algorithm):
        if self.drawing != 0:
            return
        self.status = 'polyline'
        self.temp_algorithm = algorithm
        # self.temp_id = item_id

    def start_pencil(self, algorithm):
        if self.drawing != 0:
            return
        self.status = 'pencil'
        self.temp_algorithm = algorithm
        # self.temp_id = item_id

    def start_translate(self, algorithm):
        if self.drawing == 0 and self.selected_id != '':
            self.status = 'translate'
            self.temp_algorithm = algorithm

    def start_rotate(self, algorithm):
        if self.drawing == 0 and self.selected_id != '':
            self.status = 'rotate'
            self.temp_algorithm = algorithm

    def start_scale(self, algorithm):
        if self.drawing == 0 and self.selected_id != '':
            self.status = 'scale'
            self.temp_algorithm = algorithm

    def start_clip(self, algorithm):
        if self.drawing == 0 and self.selected_id != '':
            self.status = 'clip'
            self.temp_algorithm = algorithm

    def start_copy(self):
        if self.drawing == 0 and self.selected_id != '':
            last_act = ['copy', self.temp_id]
            self.action_stack.append(last_act)
            copied_item = self.item_dict[self.selected_id]
            new_p_list = [[x + 20, y + 20] for [x, y] in copied_item.p_list]
            self.temp_item = MyItem(self.temp_id, copied_item.item_type, new_p_list, copied_item.algorithm,
                                    copied_item.item_color, copied_item.pen_width)
            self.item_dict[self.temp_id] = self.temp_item
            self.scene().addItem(self.item_dict[self.temp_id])
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
            self.updateScene([self.sceneRect()])

    def start_delete(self):
        if self.drawing == 0 and self.selected_id != '':
            last_act = ['delete', self.selected_id]
            self.action_stack.append(last_act)
            self.scene().removeItem(self.item_dict[self.selected_id])
            # self.list_widget.takeItem(int(self.selected_id))
            self.updateScene([self.sceneRect()])

    def start_undo(self):
        if len(self.action_stack):
            last_act = self.action_stack[-1]
            self.action_stack.pop(-1)
            if last_act[0] == "translate" or last_act[0] == "scale" or last_act[0] == "rotate" or \
                    last_act[0] == "clip":
                last_id, last_p_list = last_act[1], last_act[2]
                last_item = self.item_dict[last_id]
                # self.scene().removeItem(self.item_dict[last_id])
                last_item.p_list = last_p_list
                self.updateScene([self.sceneRect()])
            elif last_act[0] == "delete":
                last_id = last_act[1]
                self.scene().addItem(self.item_dict[last_id])
                self.updateScene([self.sceneRect()])
            elif last_act[0] == "line" or last_act[0] == "polygon" or last_act[0] == "polyline" or \
                    last_act[0] == "curve" or last_act[0] == "pencil" or last_act[0] == "ellipse" or \
                    last_act[0] == "copy":
                last_id = last_act[1]
                self.scene().removeItem(self.item_dict[last_id])
                self.list_widget.takeItem(int(last_id))
                self.main_window.delete_id()
                self.temp_id = str(int(self.temp_id) - 1)
        # mark

    def finish_draw(self):
        self.temp_id = self.main_window.get_id()
        self.temp_item = None
        self.drawing = 0

    def clear_selection(self):
        # print('clear_selection')
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.selected_id = ''

    def selection_changed(self, selected):
        if self.drawing != 0:
            return
        self.main_window.statusBar().showMessage('图元选择： %s' % selected)
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.item_dict[self.selected_id].update()
        if selected in self.item_dict:
            self.selected_id = selected
            self.item_dict[selected].selected = True
            self.item_dict[selected].update()
            self.status = ''
        self.updateScene([self.sceneRect()])

    def mousePressEvent(self, event: QMouseEvent) -> None:  # mark
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm, self.pen_color,
                                    self.pen_width)
            self.scene().addItem(self.temp_item)
            last_act = ['line', self.temp_id]
            self.action_stack.append(last_act)
        elif self.status == 'polygon':
            if self.temp_item is None:
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]],
                                        self.temp_algorithm, self.pen_color, self.pen_width, 0)
                self.scene().addItem(self.temp_item)
                last_act = ['polygon', self.temp_id]
                self.action_stack.append(last_act)
            else:
                self.temp_item.p_list.append([x, y])
            self.drawing = 1
        elif self.status == 'curve':
            if self.temp_item is None:
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y]],
                                        self.temp_algorithm, self.pen_color, self.pen_width)
                self.scene().addItem(self.temp_item)
                self.assist_item = MyItem(self.selected_id, 'polyline', self.temp_item.p_list, 'Bresenham',
                                          QColor(255, 0, 0))
                self.scene().addItem(self.assist_item)
                last_act = ['line', self.temp_id]
                self.action_stack.append(last_act)
            else:
                self.temp_item.p_list.append([x, y])
            self.drawing = 1
        elif self.status == 'polyline':
            if self.temp_item is None:
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]],
                                        self.temp_algorithm, self.pen_color, self.pen_width)
                self.scene().addItem(self.temp_item)
                last_act = ['line', self.temp_id]
                self.action_stack.append(last_act)
            else:
                self.temp_item.p_list.append([x, y])
            self.drawing = 1
        elif self.status == 'pencil':
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]],
                                    self.temp_algorithm, self.pen_color, self.pen_width)
            self.scene().addItem(self.temp_item)
            last_act = ['line', self.temp_id]
            self.action_stack.append(last_act)
        elif self.status == 'ellipse':
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm, self.pen_color,
                                    self.pen_width)
            self.scene().addItem(self.temp_item)
            last_act = ['line', self.temp_id]
            self.action_stack.append(last_act)
        elif self.status == 'translate':
            if self.selected_id != '':
                ori_p_list = self.item_dict[self.selected_id].p_list
                self.temp_item = MyItem(self.selected_id, self.status, [[x, y], [x, y], ori_p_list])
                last_act = ["translate", self.selected_id, ori_p_list]
                self.action_stack.append(last_act)
        elif self.status == 'rotate':
            if self.selected_id != '':
                cx, cy = self.item_dict[self.selected_id].center()
                ori_p_list = self.item_dict[self.selected_id].p_list
                self.temp_item = MyItem(self.selected_id, self.status, [[cx, cy], [x, y], [x, y], ori_p_list])
                last_act = ["translate", self.selected_id, ori_p_list]
                self.action_stack.append(last_act)
        elif self.status == 'scale':
            if self.selected_id != '':
                cx, cy = self.item_dict[self.selected_id].center()
                ori_p_list = self.item_dict[self.selected_id].p_list
                self.temp_item = MyItem(self.selected_id, self.status, [[cx, cy], [x, y], [x, y], ori_p_list])
                last_act = ["translate", self.selected_id, ori_p_list]
                self.action_stack.append(last_act)
        elif self.status == 'clip':
            if self.selected_id != '' and self.item_dict[self.selected_id].item_type == 'line':
                self.assist_item = MyItem(self.selected_id, self.status, [[x, y], [x, y]], self.temp_algorithm,
                                          QColor(255, 0, 0))
                self.scene().addItem(self.assist_item)
                ori_p_list = self.item_dict[self.selected_id].p_list
                last_act = ["translate", self.selected_id, ori_p_list]
                self.action_stack.append(last_act)
        elif self.status == '':
            choose_item = self.scene().itemAt(x, y, QTransform())
            if choose_item is not None:
                self.list_widget.setCurrentRow(int(choose_item.id))
        self.updateScene([self.sceneRect()])
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:  # 不解决双击会有很多问题
        # print("double click")
        self.double_click = 1
        if self.status == 'polygon' and self.temp_item:
            self.temp_item.p_list[-1] = self.temp_item.p_list[0]
            self.temp_item.end = 1
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
            self.updateScene([self.sceneRect()])
        elif self.status == 'curve' and self.temp_item:
            # print(self.temp_item.p_list)
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.scene().removeItem(self.assist_item)
            self.updateScene([self.sceneRect()])
            self.assist_item = None
            self.finish_draw()
        elif self.status == 'polyline' and self.temp_item:
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        super().mouseDoubleClickEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:  # mark
        # print("move")
        if self.double_click == 1:
            return
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'polygon':
            self.temp_item.p_list[-1] = [x, y]
        elif self.status == 'ellipse':
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'curve':
            pass
        elif self.status == 'polyline':
            self.temp_item.p_list[-1] = [x, y]
        elif self.status == 'pencil':
            self.temp_item.p_list.append([x, y])
        elif self.status == 'translate':
            if self.selected_id != '':
                x0, y0 = self.temp_item.p_list[0]
                ori_p_list = self.temp_item.p_list[2]
                self.temp_item.p_list[1] = [x, y]
                dx, dy = int(x - x0), int(y - y0)
                self.item_dict[self.selected_id].item_translate(ori_p_list, dx, dy)
                self.updateScene([self.sceneRect()])
        elif self.status == 'rotate':
            if self.selected_id != '' and self.item_dict[self.selected_id].item_type != 'ellipse':
                cx, cy = self.temp_item.p_list[0]
                x0, y0 = self.temp_item.p_list[1]
                ori_p_list = self.temp_item.p_list[3]
                self.temp_item.p_list[2] = [x, y]
                dx0, dy0, dx1, dy1 = x0 - cx, y0 - cy, x - cx, y - cy
                if dx0 != 0 and dx1 != 0:
                    r0, r1 = math.atan2(dy0, dx0), math.atan2(dy1, dx1)
                    r = int((r1 - r0) * 180)
                    self.item_dict[self.selected_id].item_rotate(ori_p_list, cx, cy, r)
                    self.updateScene([self.sceneRect()])
        elif self.status == 'scale':
            if self.selected_id != '':
                cx, cy = self.temp_item.p_list[0]
                x0, y0 = self.temp_item.p_list[1]
                ori_p_list = self.temp_item.p_list[3]
                self.temp_item.p_list[2] = [x, y]
                if x0 == cx and y0 == cy:
                    pass
                else:
                    s = ((x - cx) * (x - cx) + (y - cy) * (y - cy)) / ((x0 - cx) * (x0 - cx) + (y0 - cy) * (y0 - cy))
                    s = math.sqrt(s)
                    self.item_dict[self.selected_id].item_scale(ori_p_list, cx, cy, s)
                    self.updateScene([self.sceneRect()])
        elif self.status == 'clip':
            if self.selected_id != '' and self.item_dict[self.selected_id].item_type == 'line':
                self.assist_item.p_list[1] = [x, y]
        self.updateScene([self.sceneRect()])
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:  # mark
        # print("release")
        if self.double_click == 1:
            self.double_click = 0
            return
        if self.status == 'line':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        elif self.status == 'polygon':
            threshold = 10
            if abs(self.temp_item.p_list[-1][0] - self.temp_item.p_list[0][0]) + abs(
                    self.temp_item.p_list[-1][0] - self.temp_item.p_list[0][0]) <= threshold and len(
                self.temp_item.p_list) > 2:
                self.temp_item.p_list[-1] = self.temp_item.p_list[0]
                self.temp_item.end = 1
                self.item_dict[self.temp_id] = self.temp_item
                self.list_widget.addItem(self.temp_id)
                self.finish_draw()
                self.updateScene([self.sceneRect()])
        elif self.status == 'curve' or self.status == 'polyline':
            pass
        elif self.status == 'pencil':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        elif self.status == 'ellipse':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        elif self.status == 'scale' or self.status == 'translate' or self.status == 'rotate':
            if self.selected_id != '':
                self.temp_item = None
        elif self.status == 'clip':
            if self.selected_id != '' and self.item_dict[self.selected_id].item_type == 'line':
                x0, y0 = self.assist_item.p_list[0]
                x1, y1 = self.assist_item.p_list[1]
                x_min, y_min, x_max, y_max = min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)
                self.item_dict[self.selected_id].item_clip(x_min, y_min, x_max, y_max, self.temp_algorithm)
                self.scene().removeItem(self.assist_item)
                self.updateScene([self.sceneRect()])
                self.assist_item = None
        super().mouseReleaseEvent(event)


class MyItem(QGraphicsItem):
    """
    自定义图元类，继承自QGraphicsItem
    """

    def __init__(self, item_id: str, item_type: str, p_list: list, algorithm: str = '',
                 item_color: QColor = QColor(0, 0, 0), pen_width: int = 1, end: int = 0,
                 parent: QGraphicsItem = None):
        """

        :param item_id: 图元ID
        :param item_type: 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        :param p_list: 图元参数
        :param algorithm: 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        :param parent:
        :param end: 该图元绘制是否已经结束（我加的）
        """
        super().__init__(parent)
        self.id = item_id  # 图元ID
        self.item_type = item_type  # 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        self.p_list = p_list  # 图元参数
        self.algorithm = algorithm  # 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        self.selected = False
        self.end = end
        self.item_color = item_color
        self.pen_width = pen_width

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem,
              widget: Optional[QWidget] = ...) -> None:  # mark
        item_pixels = []
        if self.item_type == 'line' and self.p_list:
            item_pixels = alg.draw_line(self.p_list, self.algorithm)
        elif self.item_type == 'polygon':
            if self.end == 1:
                item_pixels = alg.draw_polygon(self.p_list, self.algorithm)
            else:
                item_pixels = alg.draw_polyline(self.p_list, self.algorithm)
        elif self.item_type == 'ellipse':
            item_pixels = alg.draw_ellipse(self.p_list)
        elif self.item_type == 'curve':
            item_pixels = alg.draw_curve(self.p_list, self.algorithm)
        elif self.item_type == 'polyline':
            item_pixels = alg.draw_polyline(self.p_list, self.algorithm)
        elif self.item_type == 'pencil':
            item_pixels = alg.draw_polyline(self.p_list, 'Bresenham')
        elif self.item_type == 'clip':  # 画一个矩形而已
            x_min, y_min, x_max, y_max = self.p_list[0][0], self.p_list[0][1], self.p_list[1][0], self.p_list[1][1]
            item_pixels = alg.draw_polygon([[x_min, y_min], [x_min, y_max], [x_max, y_max], [x_max, y_min]],
                                           'Bresenham')
        for p in item_pixels:
            # painter.setPen(self.item_color)
            pen = QPen(self.item_color, self.pen_width, Qt.SolidLine)
            painter.setPen(pen)
            painter.drawPoint(*p)
        if self.selected:
            painter.setPen(QColor(255, 0, 0))
            if self.p_list:
                painter.drawRect(self.boundingRect())

    def boundingRect(self) -> QRectF:  # mark
        if len(self.p_list) == 0:
            return QRectF(0, 0, 0, 0)
        if self.item_type == 'line' or self.item_type == 'ellipse' or self.item_type == 'clip':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'polygon' or self.item_type == 'polyline' or self.item_type == 'curve' \
                or self.item_type == 'pencil':
            x_min, y_min = self.p_list[0]
            x_max, y_max = self.p_list[0]
            for x, y in self.p_list:
                x_min = min(x_min, x)
                x_max = max(x_max, x)
                y_min = min(y_min, y)
                y_max = max(y_max, y)
            return QRectF(x_min - 1, y_min - 1, x_max - x_min + 2, y_max - y_min + 2)

    def center(self):
        if len(self.p_list) == 0:
            return [0, 0]
        if self.item_type == 'line' or self.item_type == 'ellipse':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            return [(x0 + x1) / 2, (y0 + y1) / 2]
        elif self.item_type == 'polygon' or self.item_type == 'polyline' or self.item_type == 'curve' \
                or self.item_type == 'pencil':
            x_min, y_min = self.p_list[0]
            x_max, y_max = self.p_list[0]
            for x, y in self.p_list:
                x_min = min(x_min, x)
                x_max = max(x_max, x)
                y_min = min(y_min, y)
                y_max = max(y_max, y)
            return [(x_min + x_max) / 2, (y_min + y_max) / 2]

    def item_translate(self, p_list, dx, dy):
        self.prepareGeometryChange()
        self.p_list = alg.translate(p_list, dx, dy)

    def item_rotate(self, p_list, cx, cy, r):
        self.prepareGeometryChange()
        self.p_list = alg.rotate(p_list, cx, cy, r)

    def item_scale(self, p_list, cx, cy, s):
        self.prepareGeometryChange()
        self.p_list = alg.scale(p_list, cx, cy, s)

    def item_clip(self, x_min, y_min, x_max, y_max, algorithm):
        self.prepareGeometryChange()
        if self.p_list:
            self.p_list = alg.clip(self.p_list, x_min, y_min, x_max, y_max, algorithm)


class MainWindow(QMainWindow):
    """
    主窗口类
    """

    def __init__(self):
        super().__init__()
        self.item_cnt = 0

        # 使用QListWidget来记录已有的图元，并用于选择图元。注：这是图元选择的简单实现方法，更好的实现是在画布中直接用鼠标选择图元
        self.list_widget = QListWidget(self)
        self.list_widget.setMinimumWidth(200)

        # 使用QGraphicsView作为画布
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 600, 600)
        self.canvas_widget = MyCanvas(self.scene, self)
        self.canvas_widget.setFixedSize(600 + 2, 600 + 2)
        self.canvas_widget.main_window = self
        self.canvas_widget.list_widget = self.list_widget
        self.canvas_widget.temp_id = self.get_id()

        # 设置菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')
        # set_pen_act = file_menu.addAction('设置画笔')
        set_pen_act = file_menu.addMenu('设置画笔')
        set_pen_color_act = set_pen_act.addAction('设置颜色')
        set_pen_width_act = set_pen_act.addAction('设置粗细')
        reset_canvas_act = file_menu.addAction('重置画布')
        save_canvas_act = file_menu.addAction('保存画布')
        exit_act = file_menu.addAction('退出')
        draw_menu = menubar.addMenu('绘制')
        pencil_act = draw_menu.addAction('铅笔')
        line_menu = draw_menu.addMenu('线段')
        line_naive_act = line_menu.addAction('Naive')
        line_dda_act = line_menu.addAction('DDA')
        line_bresenham_act = line_menu.addAction('Bresenham')
        polygon_menu = draw_menu.addMenu('多边形')
        polygon_dda_act = polygon_menu.addAction('DDA')
        polygon_bresenham_act = polygon_menu.addAction('Bresenham')
        ellipse_act = draw_menu.addAction('椭圆')
        curve_menu = draw_menu.addMenu('曲线')
        curve_bezier_act = curve_menu.addAction('Bezier')
        curve_b_spline_act = curve_menu.addAction('B-spline')
        polyline_menu = draw_menu.addMenu('折线')
        polyline_dda_act = polyline_menu.addAction('DDA')
        polyline_bresenham_act = polyline_menu.addAction('Bresenham')
        edit_menu = menubar.addMenu('编辑')
        translate_act = edit_menu.addAction('平移')
        rotate_act = edit_menu.addAction('旋转')
        scale_act = edit_menu.addAction('缩放')
        clip_menu = edit_menu.addMenu('裁剪')
        clip_cohen_sutherland_act = clip_menu.addAction('Cohen-Sutherland')
        clip_liang_barsky_act = clip_menu.addAction('Liang-Barsky')
        copy_act = edit_menu.addAction('复制粘贴')
        delete_act = edit_menu.addAction('删除')
        choose_act = menubar.addAction('鼠标选中')
        undo_act = menubar.addAction('撤销')

        # 连接信号和槽函数 mark
        # set_pen_act.triggered.connect(self.set_pen_color_action)
        set_pen_color_act.triggered.connect(self.set_pen_color_action)
        set_pen_width_act.triggered.connect(self.set_pen_width_action)
        reset_canvas_act.triggered.connect(self.reset_canvas_action)
        save_canvas_act.triggered.connect(self.save_canvas_action)
        undo_act.triggered.connect(self.undo_action)
        exit_act.triggered.connect(qApp.quit)
        pencil_act.triggered.connect(self.pencil_action)
        line_naive_act.triggered.connect(self.line_naive_action)
        line_dda_act.triggered.connect(self.line_dda_action)
        line_bresenham_act.triggered.connect(self.line_bresenham_action)
        polygon_dda_act.triggered.connect(self.polygon_dda_action)
        polygon_bresenham_act.triggered.connect(self.polygon_bresenham_action)
        polyline_dda_act.triggered.connect(self.polyline_dda_action)
        polyline_bresenham_act.triggered.connect(self.polyline_bresenham_action)
        ellipse_act.triggered.connect(self.ellipse_action)
        curve_bezier_act.triggered.connect(self.curve_bezier_action)
        curve_b_spline_act.triggered.connect(self.curve_b_spline_action)
        translate_act.triggered.connect(self.translate_action)
        rotate_act.triggered.connect(self.rotate_action)
        scale_act.triggered.connect(self.scale_action)
        copy_act.triggered.connect(self.copy_action)
        delete_act.triggered.connect(self.delete_action)
        clip_liang_barsky_act.triggered.connect(self.clip_liang_barsky_action)
        clip_cohen_sutherland_act.triggered.connect(self.clip_cohen_sutherland_action)
        choose_act.triggered.connect(self.choose_action)
        self.list_widget.currentTextChanged.connect(self.canvas_widget.selection_changed)

        # 设置主窗口的布局
        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.canvas_widget)
        self.hbox_layout.addWidget(self.list_widget, stretch=1)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.hbox_layout)
        self.setCentralWidget(self.central_widget)
        self.statusBar().showMessage('空闲')
        self.resize(600, 600)
        self.setWindowTitle('XY\'s CG Demo')

    def get_id(self):
        _id = str(self.item_cnt)
        self.item_cnt += 1
        return _id

    def delete_id(self):
        self.item_cnt -= 1

    def undo_action(self):
        if self.canvas_widget.drawing != 0:
            return
        self.canvas_widget.start_undo()
        self.statusBar().showMessage('撤销')

    def set_pen_color_action(self):
        if self.canvas_widget.drawing != 0:
            return
        color = QColorDialog.getColor()
        if color.isValid:  # 通过isValid()可以判断用户选择的颜色是否有效，若用户选择取消，isValid()将返回false
            self.canvas_widget.pen_color = color

    def set_pen_width_action(self):
        if self.canvas_widget.drawing != 0:
            return
        num1, ok1 = QInputDialog.getInt(self, '设置画笔宽度', '输入您的宽度(1～10)', 1, 1, 10, 1)
        if ok1:  # 通过isValid()可以判断用户选择的颜色是否有效，若用户选择取消，isValid()将返回false
            self.canvas_widget.pen_width = num1

    def choose_action(self):
        if self.canvas_widget.drawing != 0:
            return
        self.canvas_widget.status = ''

    def reset_canvas_action(self):
        if self.canvas_widget.drawing != 0:
            return
        num1, ok1 = QInputDialog.getInt(self, '获取宽度', '输入您的宽度(100～1000)', 600, 100, 1000, 1)
        if ok1:
            num2, ok2 = QInputDialog.getInt(self, '获取高度', '输入您的高度(100～1000)', 600, 100, 1000, 1)
        if ok1 and ok2:
            # 清空画布
            self.list_widget.clear()
            self.item_cnt = 0
            self.canvas_widget.action_stack = []
            self.canvas_widget.temp_id = self.get_id()
            # 更改画布大小
            self.scene = QGraphicsScene(self)
            self.scene.setSceneRect(0, 0, num1, num2)
            self.canvas_widget.setScene(self.scene)
            self.canvas_widget.setFixedSize(num1 + 2, num2 + 2)

    def save_canvas_action(self):
        if self.canvas_widget.drawing != 0:
            return
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, ok = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                   "Pictures (*.bmp)", options=options)
        if ok:
            filename = filename + ".bmp"
            # print(filename)
            pix_map = self.canvas_widget.grab(self.canvas_widget.sceneRect().toRect())
            pix_map.save(filename)

    def line_naive_action(self):
        if self.canvas_widget.drawing != 0:
            return
        self.canvas_widget.start_draw_line('Naive')
        self.statusBar().showMessage('Naive算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_dda_action(self):
        if self.canvas_widget.drawing != 0:
            return
        self.canvas_widget.start_draw_line('DDA')
        self.statusBar().showMessage('DDA算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_bresenham_action(self):
        if self.canvas_widget.drawing != 0:
            return
        self.canvas_widget.start_draw_line('Bresenham')
        self.statusBar().showMessage('Bresenham算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polygon_dda_action(self):
        if self.canvas_widget.drawing != 0:
            return
        self.canvas_widget.start_draw_polygon('DDA')
        self.statusBar().showMessage('DDA算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polygon_bresenham_action(self):
        if self.canvas_widget.drawing != 0:
            return
        self.canvas_widget.start_draw_polygon('Bresenham')
        self.statusBar().showMessage('Bresenham算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polyline_dda_action(self):
        if self.canvas_widget.drawing != 0:
            return
        self.canvas_widget.start_draw_polyline('DDA')
        self.statusBar().showMessage('DDA算法绘制折线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polyline_bresenham_action(self):
        if self.canvas_widget.drawing != 0:
            return
        self.canvas_widget.start_draw_polyline('Bresenham')
        self.statusBar().showMessage('Bresenham算法绘制折线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def pencil_action(self):
        if self.canvas_widget.drawing != 0:
            return
        self.canvas_widget.start_pencil('Pencil')
        self.statusBar().showMessage('铅笔')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def ellipse_action(self):
        if self.canvas_widget.drawing != 0:
            return
        self.canvas_widget.start_draw_ellipse('center')
        self.statusBar().showMessage('中心圆生成算法绘制椭圆')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_bezier_action(self):
        if self.canvas_widget.drawing != 0:
            return
        self.canvas_widget.start_draw_curve('Bezier')
        self.statusBar().showMessage('绘制Bezier曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_b_spline_action(self):
        if self.canvas_widget.drawing != 0:
            return
        self.canvas_widget.start_draw_curve('B-spline')
        self.statusBar().showMessage('绘制B-spline曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def copy_action(self):
        if self.canvas_widget.drawing != 0:
            return
        self.canvas_widget.start_copy()
        self.statusBar().showMessage('复制粘贴')

    def translate_action(self):
        if self.canvas_widget.drawing != 0:
            return
        self.canvas_widget.start_translate('平移')
        self.statusBar().showMessage('平移')

    def rotate_action(self):
        if self.canvas_widget.drawing != 0:
            return
        self.canvas_widget.start_rotate('旋转')
        self.statusBar().showMessage('旋转')

    def scale_action(self):
        if self.canvas_widget.drawing != 0:
            return
        self.canvas_widget.start_scale('缩放')
        self.statusBar().showMessage('缩放')

    def delete_action(self):
        if self.canvas_widget.drawing != 0:
            return
        self.canvas_widget.start_delete()
        self.statusBar().showMessage('删除')

    def clip_liang_barsky_action(self):
        if self.canvas_widget.drawing != 0:
            return
        self.canvas_widget.start_clip('Liang-Barsky')
        self.statusBar().showMessage('线段裁剪')

    def clip_cohen_sutherland_action(self):
        if self.canvas_widget.drawing != 0:
            return
        self.canvas_widget.start_clip('Cohen-Sutherland')
        self.statusBar().showMessage('线段裁剪')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
