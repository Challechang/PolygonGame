# coding:utf-8
from numpy import *
import Tkinter as tk

def isNum(n):
    try:
        num = int(n)
        return num
    except:
        return -1
def getRotateMatrix(theta):
    rotateMatrix = array([[cos(theta),-sin(theta)],
                          [sin(theta),cos(theta)]])
    return rotateMatrix
class Node():
    __id         = 0
    __idInCanvas = [0,0]
    __num        = 0
    __x          = 0
    __y          = 0
    def setId(self,id):
        self.__id = id
    def getId(self):
        return self.__id
    def setIdInCanvas(self,idInCanvas):
        self.__idInCanvas = idInCanvas
    def getIdInCanvas(self):
        return self.__idInCanvas
    def setNum(self,num):
        self.__num = num
    def getNum(self):
        return self.__num
    def setX(self,x):
        self.__x = x
    def getX(self):
        return self.__x
    def setY(self,y):
        self.__y = y
    def getY(self):
        return self.__y

def getNewNode(id=0,idInCanvas=None,num=0,x=0,y=0):
    if idInCanvas==None:
        idInCanvas = [0,0]
    node = Node()
    node.setId(id)
    node.setIdInCanvas(idInCanvas)
    node.setNum(num)
    node.setX(x)
    node.setY(y)
    return node

class Line():
    __id            = 0
    __idInCanvas    = 0
    __idOprInCanvas = 0
    __idIdIncanvas  = 0
    __startX        = 0
    __startY        = 0
    __endX          = 0
    __endY          = 0
    __opr           = "+"
    __node1 = Node()
    __node2 = Node()
    def setId(self,id):
        self.__id = id;
    def getId(self):
        return self.__id
    def setIdInCanvas(self,idInCanvas):
        self.__idInCanvas = idInCanvas
    def getIdInCanvas(self):
        return self.__idInCanvas
    def setIdOprInCanvas(self,idOprInCanvas):
        self.__idOprInCanvas = idOprInCanvas
    def getIdOprInCanvas(self):
        return self.__idOprInCanvas
    def setIdIdInCanvas(self,idIdInCanvas):
        self.__idIdIncanvas = idIdInCanvas
    def getIdIdInCanvas(self):
        return self.__idIdIncanvas
    def setStartX(self,startX):
        self.__startX = startX
    def getStartX(self):
        return self.__startX
    def setStartY(self,startY):
        self.__startY = startY
    def getStartY(self):
        return self.__startY
    def setEndX(self,endX):
        self.__endX = endX
    def getEndX(self):
        return self.__endX
    def setEndY(self,endY):
        self.__endY = endY
    def getEndY(self):
        return self.__endY
    def setOpr(self,opr):
        self.__opr = opr
    def getOpr(self):
        return self.__opr
    def setNode1(self,node1):
        self.__node1 = node1
    def getNode1(self):
        return self.__node1
    def setNode2(self,node2):
        self.__node2 = node2
    def getNode2(self):
        return self.__node2

def getNewLine(id,startX,startY,endX,endY,node1=None,node2=None):
    line = Line()
    line.setId(id)
    line.setStartX(startX)
    line.setStartY(startY)
    line.setEndX(endX)
    line.setEndY(endY)
    line.setNode1(node1)
    line.setNode2(node2)
    return line

def calLines(n,width,height):
    lines        = []
    nodes        = []
    centerX      = width/2;
    centerY      = height/2;
    center       = array([centerX,centerY])
    theta        = 2*pi/n
    rotateMatrix = getRotateMatrix(theta)
    length       = 150
    startX       = centerX + length
    startY       = centerY
    startMatrix = array([startX-centerX,startY-centerY])
    for i in range(n):
        endMatrix = dot(rotateMatrix,startMatrix) + center
        endX = endMatrix[0]
        endY = endMatrix[1]
        node1 = getNewNode(id=i,num=i,x=startX,y=startY)
        line = getNewLine(i, startX, startY, endX, endY,node1)
        lines.append(line)   
        startX = endX
        startY = endY
        startMatrix = array([startX-centerX,startY-centerY])
    for i in range(n):
        if i==n-1:
            lines[i].setNode2(lines[0].getNode1())
        else:
            lines[i].setNode2(lines[i+1].getNode1())
    return lines

def calXY(startX,startY,endX,endY):
    if startX != endX:
        k = abs((endY - startY)/(startX - endX))
    else:
        k = -1
    if k==0:
        x1,x2 = (startX+endX)/2 ,(startX+endX)/2
        y1,y2 = endY - 20, endY + 20
    elif k==-1: 
        x1,x2 = (startX+endX)/2 - 20,(startX+endX)/2 + 20
        y1,y2 = (startY+endY)/2, (startY+endY)/2
    elif k>1:
        x1,x2 = (startX+endX)/2 - 20,(startX+endX)/2 + 20
        y1,y2 = (startY+endY)/2 - 10, (startY+endY)/2 + 10
    else:
        x1,x2 = (startX+endX)/2 - 10,(startX+endX)/2 + 10
        y1,y2 = (startY+endY)/2 - 20, (startY+endY)/2 + 20  
    return x1,x2,y1,y2