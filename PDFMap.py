# Copyright (c) 2012, Dustin Sampson 
# All rights reserved. 

# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met: 
# 
#  * Redistributions of source code must retain the above copyright notice, 
#    this list of conditions and the following disclaimer. 
#  * Redistributions in binary form must reproduce the above copyright 
#    notice, this list of conditions and the following disclaimer in the 
#    documentation and/or other materials provided with the distribution. 
#  * Neither the name of Dustin Sampson nor the names of its 
#    contributors may be used to endorse or promote products derived from 
#    this software without specific prior written permission. 
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.

import Image, ImageDraw
from xml.dom import minidom
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Frame

class MapObject:
	"""A super class for the Small graphic objects to be used in marking up a map file."""
	def __init__(self,x,y,c):
		self.startx = x
		self.starty = y
		self.color = c
		
	def draw(self,image):
		pass

	 
class MapObjectFactory:
	"""A Factory Class that takes an xml.dom.minidom ElementNode as an argument, and returns an object that inherits from the MapObject super class."""

	def __init__(self):
		self.name = "MapObjectFactory"

	# factory method. Reads an XML Node and Figures out what kind of object we want to make.
	# labreport Canvas class does not like unicode strings for color, so these are cast to string.
	def createMapObject(self, node):		
		if node._get_localName() == "line":
			startx = int(node.getElementsByTagName("startx")[0].childNodes[0].data)
			starty = int(node.getElementsByTagName("starty")[0].childNodes[0].data)
			endx = int(node.getElementsByTagName("endx")[0].childNodes[0].data)
			endy = int(node.getElementsByTagName("endy")[0].childNodes[0].data)
			color = str(node.getElementsByTagName("color")[0].childNodes[0].data)
			thickness = int(node.getElementsByTagName("thickness")[0].childNodes[0].data)
			return Line(startx,starty,endx,endy,color,thickness)

		elif node._get_localName() == "circle":
			startx = int(node.getElementsByTagName("startx")[0].childNodes[0].data)
			starty = int(node.getElementsByTagName("starty")[0].childNodes[0].data)
			radius = int(node.getElementsByTagName("radius")[0].childNodes[0].data)
			color = str(node.getElementsByTagName("color")[0].childNodes[0].data)
			thickness = int(node.getElementsByTagName("thickness")[0].childNodes[0].data)
			return Circle(startx,starty,radius,color,thickness)
			
		elif node._get_localName() == "fillcircle":
			startx = int(node.getElementsByTagName("startx")[0].childNodes[0].data)
			starty = int(node.getElementsByTagName("starty")[0].childNodes[0].data)
			radius = int(node.getElementsByTagName("radius")[0].childNodes[0].data)
			strokecolor = str(node.getElementsByTagName("strokecolor")[0].childNodes[0].data)
			fillcolor = str(node.getElementsByTagName("fillcolor")[0].childNodes[0].data)
			thickness = int(node.getElementsByTagName("thickness")[0].childNodes[0].data)
			return FillCircle(startx,starty,radius,strokecolor,fillcolor,thickness)

		elif node._get_localName() == "rectangle":
			startx = int(node.getElementsByTagName("startx")[0].childNodes[0].data)
			starty = int(node.getElementsByTagName("starty")[0].childNodes[0].data)
			endx = int(node.getElementsByTagName("endx")[0].childNodes[0].data)
			endy = int(node.getElementsByTagName("endy")[0].childNodes[0].data)
			color = str(node.getElementsByTagName("color")[0].childNodes[0].data)
			thickness = int(node.getElementsByTagName("thickness")[0].childNodes[0].data)
			return Rectangle(startx,starty,endx,endy,color,thickness)
			
		elif node._get_localName() == "fillrectangle":
			startx = int(node.getElementsByTagName("startx")[0].childNodes[0].data)
			starty = int(node.getElementsByTagName("starty")[0].childNodes[0].data)
			endx = int(node.getElementsByTagName("endx")[0].childNodes[0].data)
			endy = int(node.getElementsByTagName("endy")[0].childNodes[0].data)
			strokecolor = str(node.getElementsByTagName("strokecolor")[0].childNodes[0].data)
			fillcolor = str(node.getElementsByTagName("fillcolor")[0].childNodes[0].data)
			stroke = int(node.getElementsByTagName("stroke")[0].childNodes[0].data)
			thickness = int(node.getElementsByTagName("thickness")[0].childNodes[0].data)
			return FillRectangle(startx,starty,endx,endy,strokecolor,fillcolor,stroke,thickness)

		elif node._get_localName() == "polygon":
			xlist = []
			ylist = []
			templist = str(node.getElementsByTagName("xlist")[0].childNodes[0].data).rsplit(",")
			for item in templist:
				xlist.append(int(item))
			templist = str(node.getElementsByTagName("ylist")[0].childNodes[0].data).rsplit(",")
			for item in templist:
				ylist.append(int(item))
			del templist
			color = str(node.getElementsByTagName("color")[0].childNodes[0].data)
			thickness = int(node.getElementsByTagName("thickness")[0].childNodes[0].data)
			return Polygon(xlist, ylist, color, thickness)

		elif node._get_localName() == "fillpolygon":
			xlist = []
			ylist = []
			templist = str(node.getElementsByTagName("xlist")[0].childNodes[0].data).rsplit(",")
			for item in templist:
				xlist.append(int(item))
			templist = str(node.getElementsByTagName("ylist")[0].childNodes[0].data).rsplit(",")
			for item in templist:
				ylist.append(int(item))
			del templist
			strokecolor = str(node.getElementsByTagName("strokecolor")[0].childNodes[0].data)
			fillcolor = str(node.getElementsByTagName("fillcolor")[0].childNodes[0].data)
			thickness = int(node.getElementsByTagName("thickness")[0].childNodes[0].data)
			return FillPolygon(xlist, ylist, strokecolor, fillcolor, thickness)
			
		elif node._get_localName() == "mapimage":
			path = node.getElementsByTagName("path")[0].childNodes[0].data
			startx = int(node.getElementsByTagName("startx")[0].childNodes[0].data)
			starty = int(node.getElementsByTagName("starty")[0].childNodes[0].data)
			return MapImage(path,startx,starty)

		elif node._get_localName() == "text":
			data = node.getElementsByTagName("string")[0].toxml()
			startx = int(node.getElementsByTagName("startx")[0].childNodes[0].data)
			starty = int(node.getElementsByTagName("starty")[0].childNodes[0].data)
			width = int(node.getElementsByTagName("width")[0].childNodes[0].data)
			height = int(node.getElementsByTagName("height")[0].childNodes[0].data)
			fontsize = int(node.getElementsByTagName("fontsize")[0].childNodes[0].data)
			return MapText(data,startx,starty,width,height,fontsize)

		elif node._get_localName() == "fillroundrectangle":
			startx = int(node.getElementsByTagName("startx")[0].childNodes[0].data)
			starty = int(node.getElementsByTagName("starty")[0].childNodes[0].data)
			endx = int(node.getElementsByTagName("endx")[0].childNodes[0].data)
			endy = int(node.getElementsByTagName("endy")[0].childNodes[0].data)
			radius = int(node.getElementsByTagName("radius")[0].childNodes[0].data)
			strokecolor = str(node.getElementsByTagName("strokecolor")[0].childNodes[0].data)
			fillcolor = str(node.getElementsByTagName("fillcolor")[0].childNodes[0].data)
			thickness = int(node.getElementsByTagName("thickness")[0].childNodes[0].data)
			return FillRoundRectangle(startx,starty,endx,endy,radius,strokecolor,fillcolor,thickness)
			
		elif node._get_localName() == "roundrectangle":
			startx = int(node.getElementsByTagName("startx")[0].childNodes[0].data)
			starty = int(node.getElementsByTagName("starty")[0].childNodes[0].data)
			endx = int(node.getElementsByTagName("endx")[0].childNodes[0].data)
			endy = int(node.getElementsByTagName("endy")[0].childNodes[0].data)
			radius = int(node.getElementsByTagName("radius")[0].childNodes[0].data)
			color = str(node.getElementsByTagName("color")[0].childNodes[0].data)
			thickness = int(node.getElementsByTagName("thickness")[0].childNodes[0].data)
			return RoundRectangle(startx,starty,endx,endy,radius,color,thickness)
			
		elif node._get_localName() == "ellipse":
			startx = int(node.getElementsByTagName("startx")[0].childNodes[0].data)
			starty = int(node.getElementsByTagName("starty")[0].childNodes[0].data)
			endx = int(node.getElementsByTagName("endx")[0].childNodes[0].data)
			endy = int(node.getElementsByTagName("endy")[0].childNodes[0].data)
			color = str(node.getElementsByTagName("color")[0].childNodes[0].data)
			thickness = int(node.getElementsByTagName("thickness")[0].childNodes[0].data)
			return Ellipse(startx,starty,endx,endy,color,thickness)
			
		elif node._get_localName() == "arc":
			startx = int(node.getElementsByTagName("startx")[0].childNodes[0].data)
			starty = int(node.getElementsByTagName("starty")[0].childNodes[0].data)
			endx = int(node.getElementsByTagName("endx")[0].childNodes[0].data)
			endy = int(node.getElementsByTagName("endy")[0].childNodes[0].data)
			color = str(node.getElementsByTagName("color")[0].childNodes[0].data)
			thickness = int(node.getElementsByTagName("thickness")[0].childNodes[0].data)
			return Arc(startx,starty,endx,endy,color,thickness)
			
		elif node._get_localName() == "fillellipse":
			startx = int(node.getElementsByTagName("startx")[0].childNodes[0].data)
			starty = int(node.getElementsByTagName("starty")[0].childNodes[0].data)
			endx = int(node.getElementsByTagName("endx")[0].childNodes[0].data)
			endy = int(node.getElementsByTagName("endy")[0].childNodes[0].data)
			strokecolor = str(node.getElementsByTagName("strokecolor")[0].childNodes[0].data)
			fillcolor = str(node.getElementsByTagName("fillcolor")[0].childNodes[0].data)
			thickness = int(node.getElementsByTagName("thickness")[0].childNodes[0].data)
			return FillEllipse(startx,starty,endx,endy,strokecolor,fillcolor,thickness)
			
		elif node._get_localName() == "fillwedge":
			startx = int(node.getElementsByTagName("startx")[0].childNodes[0].data)
			starty = int(node.getElementsByTagName("starty")[0].childNodes[0].data)
			endx = int(node.getElementsByTagName("endx")[0].childNodes[0].data)
			endy = int(node.getElementsByTagName("endy")[0].childNodes[0].data)
			angle = int(node.getElementsByTagName("angle")[0].childNodes[0].data)
			extent = int(node.getElementsByTagName("extent")[0].childNodes[0].data)
			strokecolor = str(node.getElementsByTagName("strokecolor")[0].childNodes[0].data)
			fillcolor = str(node.getElementsByTagName("fillcolor")[0].childNodes[0].data)
			thickness = int(node.getElementsByTagName("thickness")[0].childNodes[0].data)
			return FillWedge(startx,starty,endx,endy,angle, extent, strokecolor,fillcolor,thickness)
			
		elif node._get_localName() == "wedge":
			startx = int(node.getElementsByTagName("startx")[0].childNodes[0].data)
			starty = int(node.getElementsByTagName("starty")[0].childNodes[0].data)
			endx = int(node.getElementsByTagName("endx")[0].childNodes[0].data)
			endy = int(node.getElementsByTagName("endy")[0].childNodes[0].data)
			angle = int(node.getElementsByTagName("angle")[0].childNodes[0].data)
			extent = int(node.getElementsByTagName("extent")[0].childNodes[0].data)
			color = str(node.getElementsByTagName("color")[0].childNodes[0].data)
			thickness = int(node.getElementsByTagName("thickness")[0].childNodes[0].data)
			return Wedge(startx,starty,endx,endy,angle, extent, color,thickness)


		# if the class is not a recognizable MapObject, just return the parent class
		# with a 'pass' draw function.0
		else:
			return MapObject(0,0,"BLUE")	#this does nothing
			
class Line:
	"""A Line class to be used in marking up a map file."""
	def __init__(self,x,y,x2,y2,c,th):
		self.startx = x
		self.starty = y
		self.endx = x2
		self.endy = y2
		self.color = c
		self.thickness = th
		
	def draw(self,canvas):
		canvas.setStrokeColor(self.color)
		canvas.setLineWidth(self.thickness)
		canvas.line(self.startx, self.starty, self.endx, self.endy)
		#ImageDraw.Draw(image).line((self.startx, self.starty, self.endx, self.endy), fill=self.color, width=self.width)

class Rectangle:
	"""A Line class to be used in marking up a map file."""
	def __init__(self,x,y,x2,y2,c,th):
		self.startx = x
		self.starty = y
		self.width = x2 - x
		self.height = y2 - y
		self.color = c
		self.thickness = th
		
	def draw(self,canvas):
		canvas.setStrokeColor(self.color)
		canvas.setLineWidth(self.thickness)
		canvas.rect(self.startx, self.starty, self.width, self.height, stroke=1, fill=0)
		#ImageDraw.Draw(image).line((self.startx, self.starty, self.endx, self.endy), fill=self.color, width=self.width)

class FillRectangle:
	"""A Line class to be used in marking up a map file."""
	def __init__(self,x,y,x2,y2,sc,fc,s,th):
		self.startx = x
		self.starty = y
		self.width = x2 - x
		self.height = y2 - y
		self.strokecolor = sc
		self.fillcolor = fc
		self.s = s
		self.thickness = th
		
	def draw(self,canvas):
		canvas.setLineWidth(self.thickness)
		canvas.setStrokeColor(self.strokecolor)
		canvas.setFillColor(self.fillcolor)
		canvas.rect(self.startx, self.starty, self.width, self.height, stroke=self.s, fill=1)
		#ImageDraw.Draw(image).line((self.startx, self.starty, self.endx, self.endy), fill=self.color, width=self.width)

class Circle:
	'''A Circle class to be used in marking up a map graphic.'''
	def __init__(self,x,y,r,c,th):
		self.startx = x
		self.starty = y
		self.radius = r
		self.color = c
		self.thickness = th

	def draw(self,canvas):
		canvas.setLineWidth(self.thickness)
		canvas.setStrokeColor(self.color)
		canvas.circle(self.startx, self.starty, self.radius)
		#canvas.ellipse(self.startx - self.radius, self.starty - self.radius, self.startx + self.radius, self.starty + self.radius)
		#ImageDraw.Draw(image).ellipse((self.startx-self.radius,self.starty-self.radius,self.startx+self.radius,self.starty+self.radius), fill=self.color)
	 
class FillCircle:
	'''A Circle class to be used in marking up a map graphic.'''
	def __init__(self,x,y,r,sc,fc,th):
		self.startx = x
		self.starty = y
		self.radius = r
		self.strokecolor = sc
		self.fillcolor = fc
		self.thickness = th

	def draw(self,canvas):
		canvas.setLineWidth(self.thickness)
		canvas.setStrokeColor(self.strokecolor)
		canvas.setFillColor(self.fillcolor)
		canvas.circle(self.startx, self.starty, self.radius, stroke=1, fill=1)
		#canvas.ellipse(self.startx - self.radius, self.starty - self.radius, self.startx + self.radius, self.starty + self.radius, stroke=1, fill=1)
		#ImageDraw.Draw(image).ellipse((self.startx-self.radius,self.starty-self.radius,self.startx+self.radius,self.starty+self.radius), fill=self.color)

class Polygon:
	'''A Polygon that draws a path between x and y points.'''
	def __init__(self, xlist, ylist, color, thickness):
		self.xlist = xlist
		self.ylist = ylist
		self.color = color
		self.thickness = thickness

	def draw(self,canvas):
		canvas.setStrokeColor(self.color)
		canvas.setLineWidth(self.thickness)
		p = canvas.beginPath()
		p.moveTo(self.xlist[0],self.ylist[0])
		for index in range(self.xlist.__len__()):
			p.lineTo(self.xlist[index],self.ylist[index])
		# if the first x,y is not the last x,y, then we need to close the path 
		if self.xlist[0] != self.xlist[self.xlist.__len__()-1] and self.ylist[0] != self.ylist[self.ylist.__len__()-1]: 
			p.close()
		canvas.drawPath(p)

class FillPolygon:
	'''A Polygon that draws a path between x and y points.'''
	def __init__(self, xlist, ylist, strokecolor, fillcolor, thickness):
		self.xlist = xlist
		self.ylist = ylist
		self.strokecolor = strokecolor
		self.fillcolor = fillcolor
		self.thickness = thickness
		
	def draw(self,canvas):
		canvas.setStrokeColor(self.strokecolor)
		canvas.setFillColor(self.fillcolor)
		canvas.setLineWidth(self.thickness)
		p = canvas.beginPath()
		p.moveTo(self.xlist[0],self.ylist[0])
		for index in range(self.xlist.__len__()):
			p.lineTo((self.xlist[index]),self.ylist[index])
		# if the first x,y is not the last x,y, then we need to close the path 
		if self.xlist[0] != self.xlist[self.xlist.__len__()-1] and self.ylist[0] != self.ylist[self.ylist.__len__()-1]:
			p.close()
		canvas.drawPath(p, stroke=1, fill=1)

class MapImage:
	'''A PIL Image to be drawn on the PDF canvas at an specified x and y coordinate.'''
	def __init__(self,path,x,y):
		self.mi = Image.open(path)
		self.startx = x
		self.starty = y

	def draw(self,canvas):
		canvas.drawInlineImage(self.mi, self.startx, self.starty, width=0, height=0)
		#image.paste(self.mi,(self.startx, self.starty))

class MapText:
	'''A text block bounded by a frame. Uses the reportlabs platypus library.'''
	def __init__(self,string,x,y,width,height,fontsize):
		self.string = string
		self.startx = x
		self.starty = y
		self.height = height
		self.width = width
		self.fontsize = fontsize
	# 
	def draw(self,canvas):
		f = Frame(self.startx, self.starty - self.height + 10, self.width, self.height)
		styles = getSampleStyleSheet()
		styleN = styles['Normal']
		styleN.fontSize = self.fontsize
		styleN.leading = int(1.1 * self.fontsize)
		data = []
		data.append(Paragraph(self.string, styleN))
		f.addFromList(data,canvas)

class FillRoundRectangle:
	"""A Rectangle class that draws solid rectangles with rounded corners."""
	def __init__(self,x,y,x2,y2,r,sc,fc,th):
		self.startx = x
		self.starty = y
		self.width = x2 - x
		self.height = y2 - y
		self.radius = r
		self.strokecolor = sc
		self.fillcolor = fc
		self.thickness = th
		
	def draw(self,canvas):
		canvas.setLineWidth(self.thickness)
		canvas.setStrokeColor(self.strokecolor)
		canvas.setFillColor(self.fillcolor)
		canvas.roundRect(self.startx, self.starty, self.width, self.height, self.radius, stroke=1, fill=1)
		
class RoundRectangle:
	"""A Rectangle class that draws the outline of a rectangle with rounded corners."""
	def __init__(self,x,y,x2,y2,r,c,th):
		self.startx = x
		self.starty = y
		self.width = x2 - x
		self.height = y2 - y
		self.radius = r
		self.color = c
		self.thickness = th
		
	def draw(self,canvas):
		canvas.setLineWidth(self.thickness)
		canvas.setStrokeColor(self.color)
		canvas.roundRect(self.startx, self.starty, self.width, self.height, self.radius, stroke=1, fill=0)
		
class Arc:
	'''An Arc class to be used in marking up a map graphic.'''
	def __init__(self,x,y,x2,y2,c,th):
		self.startx = x
		self.starty = y
		self.endx = x2
		self.endy = y2
		self.color = c
		self.thickness = th

	def draw(self,canvas):
		canvas.setLineWidth(self.thickness)
		canvas.setStrokeColor(self.color)
		canvas.arc(self.startx, self.starty, self.endx, self.endy)
		
		
		
class FillEllipse:
	'''A Ellipse class to be used in marking up a map graphic.'''
	def __init__(self,x,y,x2,y2,sc,fc,th):
		self.startx = x
		self.starty = y
		self.endx = x2
		self.endy = y2
		self.strokecolor = sc
		self.fillcolor = fc
		self.thickness = th
	
	def draw(self,canvas):
		canvas.setLineWidth(self.thickness)
		canvas.setStrokeColor(self.strokecolor)
		canvas.setFillColor(self.fillcolor)
		canvas.ellipse(self.startx, self.starty, self.endx, self.endy, stroke=1, fill=1)
		
class Ellipse:
	'''A Ellipse class to be used in marking up a map file.'''
	def __init__(self,x,y,x2,y2,c,th):
		self.startx = x
		self.starty = y
		self.endx = x2
		self.endy = y2
		self.color = c
		self.thickness = th
		
	def draw(self,canvas):
		canvas.setLineWidth(self.thickness)
		canvas.setStrokeColor(self.color)
		canvas.ellipse(self.startx, self.starty, self.endx, self.endy, stroke=1, fill=0)
		
class FillWedge:
	'''A wedge class to be used in marking up a map graphic.'''
	def __init__(self,x,y,x2,y2,a,ext,sc,fc,th):
		self.startx = x
		self.starty = y
		self.endx = x2
		self.endy = y2
		self.startAng = a
		self.extent = ext
		self.strokecolor = sc
		self.fillcolor = fc
		self.thickness = th
	
	def draw(self,canvas):
		canvas.setLineWidth(self.thickness)
		canvas.setStrokeColor(self.strokecolor)
		canvas.setFillColor(self.fillcolor)
		canvas.wedge(self.startx, self.starty, self.endx, self.endy, self.startAng, self.extent, stroke=1, fill=1)

class Wedge:
	'''A Line class to be used in marking up a map file.'''
	def __init__(self,x,y,x2,y2,a,ext,c,th):
		self.startx = x
		self.starty = y
		self.endx = x2
		self.endy = y2
		self.startAng = a
		self.extent = ext
		self.color = c
		self.thickness = th
		
	def draw(self,canvas):
		canvas.setLineWidth(self.thickness)
		canvas.setStrokeColor(self.color)
		canvas.wedge(self.startx, self.starty, self.endx, self.endy, self.startAng, self.extent, stroke=1, fill=0)		



