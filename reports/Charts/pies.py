#!/usr/bin/python3
# encoding:utf-8

from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics.shapes import Drawing
from reportlab.platypus import Spacer
from reportlab.lib.pagesizes import A4, inch
from reportlab.lib.units import cm
from reportlab.lib.colors import deepskyblue
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont



class BasePie(object):
    pdfmetrics.registerFont(TTFont('simsun', 'simsun.ttc'))

    def __init__(self, width=A4[0], height=A4[0]/2,
                 left_margin=0, right_margin=0, top_margin=0, bottom_margin=0,
                 label_font_size=10, label_font_name='simsun'):

        self.label_font_size = label_font_size
        self.label_font_name = label_font_name

        self.width = width
        self.height = height

        # self.chart_width = self.width
        # self.chart_height = self.height
        self.chart_width = self.chart_height = min(self.width - left_margin - right_margin,
                                                   self.height - top_margin - bottom_margin)
        self.chart = Pie()
        # self.chart.x = 0
        # self.chart.y = 0
        self.chart.x = (self.width - self.chart_width)/2
        self.chart.y = (self.height - self.chart_height)/2
        self.chart.width = self.chart_width
        self.chart.height = self.chart_height

        self.title = Label()

    def add_values(self, values):
        self.chart.data = values

    def add_labels(self, labels, unit=None):
        self.chart.labels = labels

    def add_title(self, title='', title_font_name='simsun', title_font_size=18):
        if title:
            self.title.setText(title)
            self.title.setOrigin(0, 0)
            self.title.dx = self.width/2
            # self.title.dy = self.height - (self.height - self.chart_height)/2
            self.title.dy = self.height + title_font_size * 2
            self.title.fontName = title_font_name
            self.title.fontSize = title_font_size
        else:
            self.title.fontSize = 0

    def show(self):
        ret = list()
        draw = Drawing(self.width, self.height)
        draw.add(self.title)
        draw.add(self.chart)
        # spacer = Spacer(self.chart_width, getattr(self.title, 'fontSize') * 2 + self.label_font_size)
        spacer = Spacer(self.chart_width, getattr(self.title, 'fontSize') * 4)
        ret.append(spacer)
        ret.append(draw)
        return ret


def cpu_avg_load_distribution(template, values, labels):

    left_margin = getattr(template, 'leftMargin')
    right_margin = getattr(template, 'rightMargin')
    top_margin = getattr(template, 'topMargin')
    bottom_margin = getattr(template, 'bottomMargin')

    width = getattr(template, 'pagesize')[0] - left_margin - right_margin
    height = getattr(template, 'pagesize')[0] / 4
    pie = BasePie(width=width, height=height,
                  # left_margin=left_margin, right_margin=right_margin,
                  # top_margin=top_margin, bottom_margin=bottom_margin
                  )
    pie.add_values(values)
    pie.add_labels(labels)
    pie.add_title('CPU均值负载分布')
    return pie.show()

if __name__ == '__main__':
    from reportlab.platypus import SimpleDocTemplate

    doc = SimpleDocTemplate('test.pdf', pagesize=A4)
    element = list()

    p = cpu_avg_load_distribution(doc, [1,2,4,2], ['10%-20%', '30%-40%', '50%-60%', '90%-100%'])
    # p = BasePie(A4[0] - 2 * inch, A4[0]/4)
    # p.add_values([1,2,4,2])
    # p.add_labels(['10%-20%', '30%-40%', '50%-60%', '90%-100%'])
    # p.add_labels(['a', 'b', 'c', 'd'])
    element.extend(p)
    element.extend(p)

    doc.build(element)