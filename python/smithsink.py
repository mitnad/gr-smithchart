#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2014 Mitul Vekariya <vekariya93@gmail.com>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy as np
from gnuradio import gr;

from PyQt4 import Qt, QtCore, QtGui
from PyQt4 import QtCore as Qc
import PyQt4.Qwt5 as Qwt

# data points necessary to draw circles
center_x = np.zeros(21)	
center_y = np.zeros(21)
circle_radii_x = np.zeros(21) 
circle_radii_y = np.zeros(21) 

# data points to draw Re(Z) circles
datapoints_x = np.array([1,0.909090909091,0.833333333333,0.769230769231,0.714285714286,0.666666666667,0.625,0.588235294118,
0.555555555556,0.5,0.454545454545,0.416666666667,0.384615384615,0.357142857143,0.333333333333,0.25,0.2,0.166666666667,0.0909090909091,
0.047619047619,0.0196078431373])

# data points to draw Im(z) circles
datapoints_y = np.array([10.0,5.0,3.33333333333,2.5,2.0,1.66666666667,1.42857142857,1.25,1.0,0.833333333333,0.714285714286,0.625,
0.555555555556,0.5,0.333333333333,0.25,0.2,0.1,0.05,0.02])

qp = QtGui.QPainter()

class smithsink(gr.sync_block,QtGui.QWidget):
    
    def __init__(self,blkname="smithchart"):
        gr.sync_block.__init__(self,blkname,[],[])
        Qwt.QwtPlot.__init__(self)

        self.initUI()
    
    def initUI(self):
		self.setGeometry(0,0,500,500)
		self.setWindowTitle('Smith Chart')		
		self.show()
	
    def paintEvent(self, e):
		
		qp.begin(self)
		self.drawCircles()
		qp.end()

    def drawCircles(self):
		
		min_size = min(self.width(),self.height())
		# Circular region for clipping
		r1 = QtGui.QRegion(Qc.QRect((self.width() - min_size)/2, (self.height() - min_size)/2, min_size,min_size), 		
			QtGui.QRegion.Ellipse)
	        qp.setClipRegion(r1)
		
		# calculate radius of Re(z) circles from data point
		for x in range (21):
			circle_radii_x[x] = min_size*datapoints_x[x]
			
		# # calculate radius of Re(z) circles from data point
		for x in range (20):			
			circle_radii_y[x] = min_size*datapoints_y[x]
		
		pen = QtGui.QPen(Qc.Qt.black, 5, Qc.Qt.SolidLine)
	        qp.setPen(pen)
		
		p = Qc.QPoint(self.width()/2 + min_size/2 - circle_radii_x[0]/2, self.height()/2)
		qp.drawEllipse(p,circle_radii_x[0]/2, circle_radii_x[0]/2)
		
		pen = QtGui.QPen(Qc.Qt.darkGray, 1, Qc.Qt.SolidLine)
       		qp.setPen(pen)
		
		# draw Re(z) circles
		for x in range (1,21):
			p = Qc.QPoint(self.width()/2 + min_size/2 - circle_radii_x[x]/2, self.height()/2)
			qp.drawEllipse(p,circle_radii_x[x]/2, circle_radii_x[x]/2)
		
		# draw Im(z) circles
		for x in range (20):
			p = Qc.QPoint(self.width()/2 + min_size/2, self.height()/2 - circle_radii_y[x]/2)
			qp.drawEllipse(p,circle_radii_y[x]/2,circle_radii_y[x]/2)
			p = Qc.QPoint(self.width()/2 + min_size/2, self.height()/2 + circle_radii_y[x]/2)
			qp.drawEllipse(p,circle_radii_y[x]/2,circle_radii_y[x]/2)
		
		# draw line passing through Y - axis (circle having INFINITE radius)
		qp.drawLine((self.width()-min_size)/2,min_size/2,(self.width()+min_size)/2,min_size/2)
				
    def work(self, input_items, output_items):
	        pass


