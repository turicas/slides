#!/usr/bin/env python
# coding: utf-8
# Based on <https://github.com/gregpinero/ArduinoPlot>
# Created by Álvaro Justen aka Turicas
# https://github.com/turicas

import serial
import matplotlib
import wx
matplotlib.use('WXAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas, \
        NavigationToolbar2WxAgg as NavigationToolbar
import pylab
import numpy as np


REFRESH_INTERVAL_MS = 50
XMIN = 0
XMAX = 100
YMIN = 0
YMAX = 1024

class GraphFrame(wx.Frame):
    """ The main frame of the application """
    title = 'Arduino from USB/Serial: analogRead'

    def __init__(self):
        wx.Frame.__init__(self, None, -1, self.title)
        self.data = []
        self.create_main_panel()
        self.redraw_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)
        self.redraw_timer.Start(REFRESH_INTERVAL_MS)
        self.arduino = serial.Serial('/dev/ttyACM0', 9600)

    def create_main_panel(self):
        self.panel = wx.Panel(self)
        self.init_plot()
        self.canvas = FigCanvas(self.panel, -1, self.fig)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.canvas, 1, flag=wx.LEFT | wx.TOP | wx.GROW)
        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)

    def init_plot(self):
        self.dpi = 100
        self.fig = Figure((10.0, 5.0), dpi=self.dpi)
        self.axes = self.fig.add_subplot(111)
        self.axes.set_axis_bgcolor('black')
        self.axes.set_title('Arduino Serial Data', size=12)
        pylab.setp(self.axes.get_xticklabels(), fontsize=8)
        pylab.setp(self.axes.get_yticklabels(), fontsize=8)
        self.plot_data = self.axes.plot(self.data, linewidth=1,
                                        color=(1, 1, 0))[0]
        self.axes.set_xbound(lower=XMIN, upper=XMAX)
        self.axes.set_ybound(lower=YMIN, upper=YMAX)
        self.axes.grid(True, color='gray')

    def draw_plot(self):
        pylab.setp(self.axes.get_xticklabels(), visible=True)
        self.plot_data.set_xdata(np.arange(len(self.data)))
        self.plot_data.set_ydata(np.array(self.data))
        self.canvas.draw()

    def read_data(self):
        data = self.arduino.readline().strip()
        if data:
            return int(data)
            return 5 * (int(data) / 1024.0)
        else:
            return None

    def on_redraw_timer(self, event):
        data = self.read_data()
        if data is not None:
            self.data.append(data)
        else:
            self.data.append(data[-1])
        if len(self.data) > XMAX:
            self.data.pop(0)
        self.draw_plot()

    def on_exit(self, event):
        self.Destroy()

if __name__ == '__main__':
    app = wx.PySimpleApp()
    app.frame = GraphFrame()
    app.frame.Show()
    app.MainLoop()
