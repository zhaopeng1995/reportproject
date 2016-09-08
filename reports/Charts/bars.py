#!/usr/bin/python3
# encoding:utf-8

import math

from reportlab.graphics.charts.barcharts import HorizontalBarChart
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics.shapes import Drawing
from reportlab.platypus import Spacer

from reportlab.lib.colors import deepskyblue
from reportlab.lib.pagesizes import A4, inch
from reportlab.lib.units import cm

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from Charts.categories import percent_category


class BaseHorizontalBarChart(object):
    pdfmetrics.registerFont(TTFont('simsun', 'simsun.ttc'))

    def __init__(self, width=A4[0], height=A4[1] * 0.25, leftMargin=inch, rightMargin=inch,
                 axis_font_size=10, axis_font_name='simsun',
                 ):
        self.axis_font_name = axis_font_name
        self.axis_font_size = axis_font_size
        self.width = width
        self.height = height
        self.chart_width = self.width - leftMargin - rightMargin
        self.chart_height = self.height

        self.chart = HorizontalBarChart()
        self.chart.x = 0
        self.chart.y = 0

        self.chart.width = self.chart_width
        self.chart.height = self.chart_height
        self.chart.bars.strokeColor = None
        # 设置柱状图的柱子颜色
        self.chart.bars[0].fillColor = deepskyblue

        # 设置在柱状图后增加该坐标的值
        self.chart.barLabelFormat = '%0.2f'
        self.chart.barLabels.boxAnchor = 'w'  # 锚点,用不好..
        self.chart.barLabels.dx = 0.1 * cm  # 柱状图的值向右偏移0.1CM

        # 设置柱状图的柱宽
        self.chart.barWidth = height * 0.05

        self.title = Label()
        self.x_unit = Label()
        self.y_unit = Label()

        self.title.setText('')
        self.x_unit.setText('')
        self.y_unit.setText('')

        self.x_unit.fontName = self.axis_font_name
        self.y_unit.fontName = self.axis_font_name

    def add_title(self, title='', title_font_size=18, title_font_name='simsun'):
        if title:
            self.title.setText(title)
            self.title.setOrigin(0, 0)
            self.title.dx = 0.5 * self.chart_width
            self.title.dy = self.chart.height + title_font_size
            self.title.fontName = title_font_name
            self.title.fontSize = title_font_size
        else:
            self.title.fontSize = 0

    def add_category_axis(self, category_names=None, axis_unit=None):
        # 设置纵坐标轴
        self.chart.categoryAxis.labels.fontName = self.axis_font_name
        self.chart.categoryAxis.labels.fontSize = self.axis_font_size
        self.chart.categoryAxis.categoryNames = category_names
        if category_names:
            self.chart.height = len(category_names) * self.axis_font_size * 2
            self.chart_height = self.chart.height
            # print(self.chart_height)
            self.height = self.chart.height + getattr(self.title, 'fontSize')

        if axis_unit:
            # 纵坐标轴单位
            self.y_unit.setText(axis_unit)
            self.y_unit.setOrigin(0, 0)
            self.y_unit.dy = self.chart.height + self.axis_font_size
            self.y_unit.dx = -1 * self.axis_font_size * math.floor(len(axis_unit) / 2)

    def add_values(self, values, axis_unit=None):

        min_value = 0
        max_value = max(values)
        if max_value >= 50:
            step = 10
        else:
            step = 5

        # 设置横坐标轴
        self.chart.valueAxis.labels.fontName = self.axis_font_name
        self.chart.valueAxis.labels.fontSize = self.axis_font_size
        self.chart.valueAxis.valueMin = min_value
        self.chart.valueAxis.valueMax = min(divmod(max_value, step)[0] * step + step, 100)
        self.chart.valueAxis.valueStep = step

        if values:
            self.chart.data = [values]
        else:
            self.data = [0 for _ in range(len(self.chart.categoryAxis.categoryNames))]
        # self.chart.data = values

        if axis_unit:
            self.x_unit.setText(axis_unit)
            self.x_unit.setOrigin(0, 0)
            if len(axis_unit) == 1:
                self.x_unit.dx = self.chart_width + self.axis_font_size
            else:
                self.x_unit.dx = self.chart_width + self.axis_font_size * math.floor(len(axis_unit) / 2)

    def show(self):
        ret = list()
        print(self.width, self.height)
        print(self.chart_width, self.chart_height)
        print(self.chart.width, self.chart.height)
        draw = Drawing(self.width, self.height)
        draw.add(self.title)
        draw.add(self.chart)
        draw.add(self.x_unit)
        draw.add(self.y_unit)
        spacer = Spacer(self.chart_width, getattr(self.title, 'fontSize') * 2 + self.axis_font_size)
        ret.append(spacer)
        ret.append(draw)
        # Spacer(chart_width, title_font_size * 2 + axis_font_size), d)
        return self.ret


# TODO: 先考虑要不要写这个方法,可能是饼图
def cpu_avg_load_distribution(template, percent):
    width = getattr(template, 'pagesize')[0] - getattr(template, 'leftMargin') - getattr(template, 'rightMargin')
    draw = base_horizon_bar(data=percent, category_names=percent_category, page_width=width,
                            x_unit_text='%', y_unit_text='%', title='CPU均值负载分布')

    return draw


# TODO: 用类HorizonBar写这个方法
def resource_status(template, usage):
    """
    :param template:
    :param usage: 需要为字典,{'disk':(size, used_rate),
                             'memory': (total_size, used_rate),
                             'vcpu': (total_count, used_rate)
                            }
                  或者为list or tuple : [(磁盘总大小, 使用率), (内存总大小, 使用率), (VCPU总数, 使用率)]

    :return:
    """
    width = getattr(template, 'pagesize')[0]
    left_margin = getattr(template, 'leftMargin')
    right_margin = getattr(template, 'rightMargin')
    used_rate = list()
    cate_name = list()

    if isinstance(usage, dict):
        used_rate.extend([usage.get('disk')[1],
                          usage.get('memory')[1],
                          usage.get('vcpu')[1]])
        cate_name.extend(['%s磁盘' % usage.get('disk')[0],
                          '%s内存' % usage.get('memory')[0],
                          '%sVCPU' % usage.get('vcpu')[0]])
    elif isinstance(usage, list) or isinstance(usage, tuple):
        used_rate.extend([usage[0][1], usage[1][1], usage[2][1]])
        cate_name.extend(['%s磁盘' % usage[0][0],
                          '%s内存' % usage[1][0],
                          '%sVCPU' % usage[2][0]])

    d = BaseHorizontalBarChart(width=width, leftMargin=left_margin, rightMargin=right_margin)

    d.add_category_axis(cate_name)
    d.add_values(used_rate, '%')
    d.add_title(title='资源使用总况', title_font_size=18)

    # draw = base_horizon_bar(data=used_rate, category_names=cate_name, page_width=width,
    #                         x_unit_text='%', title='资源使用总况')

    return d.show()


if __name__ == '__main__':
    from reportlab.platypus import SimpleDocTemplate

    # from reportlab.lib.pagesizes import A4

    element = list()
    #
    percent = [0 for _ in range(10)]
    doc = SimpleDocTemplate('test.pdf', pagesize=A4)
    data = (0.079949, 0.083669, 0.088432, 0.091872, 0.162868, 0.170801, 0.173111, 0.185593, 0.188660, 0.193463,
            0.197778, 0.220361, 0.248728, 0.254675, 0.256276, 0.265426, 0.267474, 0.268247, 0.284910, 0.287455,
            0.311435, 0.322448, 0.328376, 0.348196, 0.360490, 0.362725, 0.366116, 0.400883, 0.443047, 0.445541,
            0.462481, 0.482165, 0.499453, 0.539923, 0.561005, 0.564949, 0.572787, 0.588897, 0.599173, 0.612498,
            0.614381, 0.621003, 0.624884, 0.627763, 0.628897, 0.674407, 0.702716, 0.835000, 0.883067, 0.921886,
            0.923420, 0.935129, 0.935969, 1.090649, 1.100490, 1.119021, 1.123721, 1.183650, 1.303634, 1.343178,
            1.552474, 1.622784, 1.712455, 1.793257, 1.827254, 1.921028, 2.004098, 2.200465, 2.372413, 2.456765,
            2.489201, 2.506770, 3.048222, 3.475369, 4.000696, 4.479436, 5.368843, 6.754158, 31.797532, 31.830696,
            31.883479, 32.001289, 32.536512)
    for i in data:
        if i > 100:
            continue
        # print(i, (int(i), 10)[0])
        percent[divmod(int(i), 10)[0]] += 1

    print(percent)
    total = sum(percent)
    percent = [i / total * 100 for i in percent]
    # percent.reverse()
    # print(percent)
    #
    # # percent = (0, 10, 20, 20, 97, 20, 0, 0, 0, 0)
    usage = [('2.5T', 70), ('400G', 50), ('200', 45)]
    # draw1 = cpu_avg_load_distribution(doc, percent)
    # draw = resource_status(doc, usage)
    # # width = doc.pagesize[0] - doc.leftMargin - doc.rightMargin
    # # width = getattr(doc, 'pagesize')[0] - getattr(doc, 'leftMargin') - getattr(doc, 'rightMargin')
    # # draw = base_horizon_bar(data=percent, category_names=percent_category, color=deepskyblue, page_width=width,
    # #                         title='CPU均值负载分布')
    #
    # element.extend(draw)
    # element.extend(draw1)
    # draw = HorizonBar()
    # draw.add_category_axis(percent_category)
    # draw.add_title('fuck')
    # draw.add_category_axis(percent_category)
    # draw.add_values(percent, '元')
    # draw.add_category_axis(percent_category, '777')

    # element.extend(draw.show())
    # element.extend(draw.show())
    element.extend(resource_status(doc, usage))
    doc.build(element)
