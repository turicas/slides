#!/usr/bin/env python
# coding: utf-8

'''Given a file dict_size.dat, this file calculates some information about data
(minimum, average and maximum values) and prepare data (x and y) to plot'''

data = [x.split('\t') for x in open('dict_size.dat').read().split('\n')]
data = [(int(x[0]), int(x[1])) for x in data if x[0].strip()]
l = [float(x[1]) / x[0] for x in data]
print('min: {:6.3f}, avg: {:6.3f}, max: {:6.3f}'
      .format(min(l), sum(l) / len(l), max(l)))
x = [e[0] for e in data]
y = [e[1] for e in data]
#plot(x, y)
