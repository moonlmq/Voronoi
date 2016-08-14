# -*- coding:utf-8 -*-
"""
实现Delaunay三角形
"""
import math
import numpy as np

#定义点
class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y

#定义三角形
class Triangle:
	def __init__(self,v1,v2,v3):
		self.v1 = v1
		self.v2 = v2
		self.v3 = v3

	#获得三角形顶点
	def getVertices(self):
		return (self.v1,self.v2,self.v3)
	
	#获得三角形圆心与半径
	def getCenterAndRadius(self):
		v1 = self.v1
		v2 = self.v2
		v3 = self.v3

		#计算三角形两条边的垂直平分线斜率
		m1 = -(v1.x-v2.x)/(v1.y-v2.y)
		m2 = -(v2.x-v3.x)/(v2.y-v3.y)
		#垂直平分点
		x1 = (v1.x+v2.x)/2
		y1 = (v1.y+v2.y)/2
		x2 = (v2.x+v3.x)/2
		y2 = (v2.y+v3.y)/2
		#求圆心坐标
		xc = (m1x1-m2x2+y2-y1)/(m1-m2)
		yc = m1*xc+y1-m1*x1

		self.center = Point(xc,yc)
		#求半径
		dx = (v1.x-xc)*(v1.x-xc)
		dy = (v1.y-yc)*(v1.y-yc)

		self.rad = math.sqrt(dx+dy)

	def inCircle(self,v):
		dx = (v.x-self.center.x)*(v.x-self.center.x)
		dy = (v.y-self.center.y)*(v.y-self.center.y)
		d = math.sqrt(dx+dy)

		rx = (v1.x-self.center.x)*(v1.x-self.center.x)
		ry = (v1.y-self.center.y)*(v1.y-self.center.y)
		r = math.sqrt(rx,ry)
		if r >= d:
			return True
		else:
			return False


MAXSIZE = 15000
#获得Delaunay三角形
def getDelaunay(ptlist):
	trianglelist = [None]*MAXSIZE
	complete = [False]*MAXSIZE
	for i in range(MAXSIZE):
		complete.append(False)
	edgeslist = [[None]*MAXSIZE for row in xrange(2)]

	#构建超级三角形（包含所有点）
	xmin = ptlist[0].x
	ymin = ptlist[0].y

	xmax = xmin
	ymax = ymin

	ptnum = len(ptlist)
	for i in xrange(1,ptnum):
		if ptlist[i].x < xmin:
			xmin = ptlist[i].x
		if ptlist[i].x >xmax:
			xmax = ptlist[i].x
		if ptlist[i].y < ymin:
			ymin = ptlist[i].y
		if ptlist[i].y> ymax:
			ymax = ptlist[i].y

	dx = xmax - xmin
	dy = ymax - ymin
	if dx > dy:
		dmax = dx
	else:
		dmax = dy
	xmid = (xmax + xmin)/2
	ymid = (ymax + ymin)/2

	newpt = Point(xmid - 2*dmax,ymid-dmax)
	ptlist.append(newpt)
	newpt = Point(xmid, ymid+2*dmax)
	ptlist.append(newpt)
	newpt = Point(xmid+2*dmax,)
