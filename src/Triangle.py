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
	newpt = Point(xmid+2*dmax,ymid - dmax)
	ptlist.append(newpt)

	#寻找Delaunay三角形
	triangle = Triangle(ptlist[ptnum],ptlist[ptnum+1],ptlist[ptnum+2])
	trianglelist[0] = triangle
	complete[0] = False

	ntri = 0

	for i in range(ptnum):
		#不断插入新节点
		nedge = -1
		j = -1
		while j < ntri:
			#判断在哪一个三角形外接圆里面
			j += 1
			if not complete[j] and trianglelist[j]:
				inc = trianglelist[j].inCircle(ptlist[i])
				if inc:
					edgeslist[0][nedge+1] = trianglelist[j].v1
					edgeslist[1][nedge+1] = trianglelist[j].v2
					edgeslist[0][nedge+2] = trianglelist[j].v2
					edgeslist[1][nedge+2] = trianglelist[j].v3
					edgeslist[0][nedge+3] = trianglelist[j].v3
					edgeslist[1][nedge+3] = trianglelist[j].v1
					nedge += 3
					trianglelist[j] = trianglelist[ntri]
					complete[j] = complete[ntri]

					j - = 1
					ntri -= 1


		#同时处于对于一个三角形外接圆里面，那么就把公共边删掉
		for j in range(nedge):
			if edgeslist[0][j] and edgeslist[1][j]:
				for k in range(j+1,nedge+1):
					if edgeslist[0][k] and edgeslist[1][k]:
						if edgeslist[0][j] == edgeslist[1][k]:
							if edgeslist[1][j] == edgeslist[0][k]:
								edgeslist[0][j] = None
								edgeslist[0][k] = None
								edgeslist[1][j] = None
								edgeslist[1][k] = None
		
		for j in range(nedge+1):
			if edgeslist[0][j] and edgeslist[1][j]:
				ntri += 1
				trianglelist[ntri] = Triangle(edgeslist[0][j],edgeslist[1][j],ptlist[i])
				complete[ntri] = False
	#将新生成的三角形放入list
	i = -1
	while i< ntri:
		i += 1
		if trianglelist[i]:
			if not (trianglelist[i].v1 in ptlist[0:ptnum] and trianglelist[i].v2 in ptlist[0:ptnum] \
				and trianglelist[i].v3 in ptlist[0:ptnum]):
				trianglelist[i] = trianglelist[ntri]
				i -= 1
				ntri -= 1
				print i
		else:
			trianglelist[i] = trianglelist[ntri]
			i -= 1
			ntri -= 1
	return trianglelist[:ntri+1]


