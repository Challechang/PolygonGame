# encoding:utf-8
from Tkinter import *
from FunctionCallback import *
from tkMessageBox import showerror
from tkMessageBox import  askyesno
from ImageTk import *
import copy
import polygon_game as plg
import tkFont

class MainFrame(Frame):

    initbarHeight   = 100
    initbarWidth    = 100
    resultbarHeight = 400
    resultbarWidth  = 200
    drawbarHeight   = 500
    drawbarWidth    = 500
    ovalRadius      = 25
    widgetWidth     = 10
    n               = -1
    lines           = []
    originLines     = []
    stackPreLines   = []
    stackNextLines  = []
    firstEdge       = True
    ERROR           = -1
    test            = 0
    intervalTime    = 1000

    def __init__(self,parent=None):
        Frame.__init__(self, parent)
#         self.pack(expand=YES,fill=BOTH)
        self.createWidgets()
        self.master.title("game")
    
    def createWidgets(self):
        self.createInitbar()
        self.createResultbar()
        self.createDrawbar()

    #接收用户输入的数据n
    def createInitbar(self):
        initbarWindow = PanedWindow(self.master,relief=RIDGE,
                                                orient=VERTICAL,
                                                width=self.resultbarWidth,
                                                height=self.initbarHeight)
        initbarWindow.grid(row=0,column=0)

        Label(initbarWindow, text="Input N",anchor=CENTER).grid(row=0,column=0,columnspan=2)
        getNEntry = Entry(initbarWindow)
        getNEntry.grid(row=1, column=0, columnspan=2)
        confirm = Button(initbarWindow, command=lambda:self.confirmGetN(getNEntry),
                                        text="Confirm",
                                        width=self.widgetWidth)
        confirm.grid(row=2,column=0,padx=10)
        inputData = Button(initbarWindow, text="Input Data",
                           command=self.getData,
                           width=self.widgetWidth)
        inputData.grid(row=2,column=1,pady=10,padx=10)
    
    def confirmGetN(self,getNEntry):
        self.n = getNEntry.get()
        if (isNum(self.n) == -1):
            self.n = -1
            showerror("error", "Data is not a Number!!!")
            return
        elif (isNum(self.n) < 1):
            self.n = -1
            showerror("error", "Number less than 1!!!")
            return
        else:
            self.n              = isNum(self.n)
            self.lines          = calLines(self.n, self.drawbarWidth, self.drawbarHeight)
            self.originLines    = copy.deepcopy(self.lines)
            self.stackPreLines  = []
            self.stackNextLines = []
            self.firstEdge      = True
            self.drawLines()
    def drawOprNextOrBack(self):
        self.canvas.create_rectangle(self.drawbarWidth * 1.0 / 3, self.drawbarHeight * 7.0 / 8,
                                     self.drawbarWidth * 1.0 / 3 + 60, self.drawbarHeight * 7.0 / 8 + 30,
                                     fill="black")
        preId = self.canvas.create_text(self.drawbarWidth * 1.0 / 3 + 30, self.drawbarHeight * 7.0 / 8 + 15,
                                        text="Previous",
                                        fill="yellow",
                                        activefill="white")

        self.canvas.create_rectangle(self.drawbarWidth * 2.0 / 3, self.drawbarHeight * 7.0 / 8,
                                     self.drawbarWidth * 2.0 / 3 + 60, self.drawbarHeight * 7.0 / 8 + 30,
                                     fill="black")
        nextId = self.canvas.create_text(self.drawbarWidth * 2.0 / 3 + 30, self.drawbarHeight * 7.0 / 8 + 15,
                                         text="Next",
                                         fill="yellow",
                                         activefill="white")

        self.canvas.tag_bind(preId, sequence="<Button-1>", func=self.preOprClick)
        self.canvas.tag_bind(nextId, sequence="<Button-1>", func=self.nextOprClick)

    def preOprClick(self,event):
        lenStackLines = len(self.stackPreLines)
        if lenStackLines==0:
            showerror("error","No previous!!!")
            return
        elif lenStackLines==1:
            self.firstEdge = True

        self.stackNextLines.append(copy.deepcopy(self.lines))
        self.lines = self.stackPreLines.pop()
        self.drawLines()

    def nextOprClick(self,event):
        lenStackLines = len(self.stackNextLines)
        if lenStackLines==0:
            showerror("error","No next!!!")
            return
        self.stackPreLines.append(copy.deepcopy(self.lines))
        self.lines = self.stackNextLines.pop()
        self.drawLines()

    def drawLines(self):
        self.canvas.delete("all")
        self.drawOprNextOrBack()
        for i in range(len(self.lines)):
            line = self.lines[i]
            (startX,startY,endX,endY) = (line.getStartX(), line.getStartY(),
                                         line.getEndX(), line.getEndY())
            idInCanvas = self.canvas.create_line((startX, startY, endX, endY), arrow=tk.BOTH,
                                                 width=3, smooth=True, activefill="white")
            line.setIdInCanvas(idInCanvas)
            x1,x2,y1,y2 = calXY(startX, startY, endX, endY)
            oprId = self.canvas.create_text(x1, y1,
                                            text=line.getOpr(),
                                            fill="blue",
                                            activefill="yellow")
            line.setIdOprInCanvas(oprId)
            idId = self.canvas.create_text(x2, y2,
                                           text=line.getId(),
                                           fill="blue",
                                           activefill="yellow")
            line.setIdIdInCanvas(idId)
            ovalId = self.canvas.create_oval(startX-self.ovalRadius, startY-self.ovalRadius,
                                             startX+self.ovalRadius, startY+self.ovalRadius,
                                             fill="black")
            numId = self.canvas.create_text(startX, startY,
                                            text=line.getNode1().getNum(),
                                            fill="yellow")
            line.getNode1().setIdInCanvas([ovalId,numId])
            if i==len(self.lines)-1:
                ovalId = self.canvas.create_oval(endX - self.ovalRadius, endY - self.ovalRadius,
                                                 endX + self.ovalRadius, endY + self.ovalRadius,
                                                 fill="black")
                numId = self.canvas.create_text(endX, endY,
                                                text=line.getNode2().getNum(),
                                                fill="yellow")
                line.getNode2().setIdInCanvas([ovalId,numId])
            def handler(event,i = line.getId()):
                return self.lineClick(event,i)
            self.canvas.tag_bind(idInCanvas,sequence="<Button-1>",func=handler)

    def lineClick(self, event, i):
        self.stackPreLines.append(copy.deepcopy(self.lines))         #将当前所有信息压入栈列表中
        self.stackNextLines = []
        self.removeLineIFromCanvas(i)

    def removeLineIFromCanvas(self, i):
        index, line = self.delLine(self.lines, i)  # 将第i条线从列表中删除
        if self.firstEdge:
            self.firstEdge = False
            self.delLineInCanvas(line)
            self.resortLines(self.lines, i)
            return

        node1 = line.getNode1()
        node2 = line.getNode2()
        opr = line.getOpr()
        num1 = node1.getNum()
        num2 = node2.getNum()
        x = node1.getX()
        y = node1.getY()
        if cmp(opr, "+") == 0:
            sum = num1 + num2
        elif cmp(opr, "*") == 0:
            sum = num1 * num2
        else:
            showerror("error", "Opr is not expected")
        node1.setNum(sum)
        # 查看Node1是否处于末端线段，如果是，直接返回，否则将当前Node1坐标设置给下一条直线的StartX和StartY
        activeLineLen = len(self.lines)
        if index == (activeLineLen):
            if activeLineLen == 0:
                self.canvas.create_oval(x - self.ovalRadius, y - self.ovalRadius,
                                        x + self.ovalRadius, y + self.ovalRadius,
                                        fill="black")
                self.canvas.create_text(x, y,
                                        text=node1.getNum(),
                                        fill="yellow")
                self.delNodeInCanvas(node2)
                self.delLineInCanvas(line)
            else:
                self.drawLines()
            return
        else:
            nextLine = self.lines[index]
        nextLine.setNode1(node1)
        nextLine.setStartX(x)
        nextLine.setStartY(y)
        self.drawLines()

    #把列表index开始的元素放置列表开头，其它依次放置
    def resortLines(self,lines,index):
        temp = lines[0:index]
        lenLines = len(lines)
        for i in range(lenLines-index):
            lines[i] = lines[index+i]
        j = 0
        for i in range(lenLines-index,lenLines):
            lines[i] = temp[j]
            j += 1

    def delLine(self,lines,id):
        for index in range(len(lines)):
            if lines[index].getId()==id:
                return index,lines.pop(index)
        return self.ERROR
    # 从canvas中删除一条线
    def delLineInCanvas(self,line):
        idInCanvas = line.getIdInCanvas()
        oprId      = line.getIdOprInCanvas()
        idId       = line.getIdIdInCanvas()
        self.canvas.delete(idInCanvas)
        self.canvas.delete(oprId)
        self.canvas.delete(idId)

    def delNodeInCanvas(self,node):
        idInCanvas = node.getIdInCanvas()
        self.canvas.delete(idInCanvas[0])
        self.canvas.delete(idInCanvas[1])

    def createResultbar(self):
        resultbarWindow = PanedWindow(self.master , relief=RIDGE,
                                                    width=self.resultbarWidth,
                                                    height=self.resultbarHeight)
        resultbarWindow.grid(row=1,column=0)
        showBestResult = Button(resultbarWindow,width=self.widgetWidth,
                                                text="Best Result",
                                                command=self.showBestResultClick)
        filename = 'D:\Python27\workspace\PolygonGame\src\images\pic.JPG'
        img = PhotoImage(file=filename)
        label = Label(resultbarWindow, image=img)

        resultbarWindow.add(showBestResult, sticky=N, pady=10)
        # resultbarWindow.add(label)

    def showBestResultClick(self):
        if (isNum(self.n) == -1):
            self.n = -1
            showerror("error", "Data is not a Number!!!")
            return
        if (isNum(self.n) < 1):
            self.n = -1
            showerror("error", "Number less than 1!!!")
            return
        for line in self.originLines:
            print line.getId()
        bestRemoveLineOrder = plg.dealBestPath(self.originLines)
        self.lines = copy.deepcopy(self.originLines)
        self.drawLines()
        self.firstEdge = True
        self.canvas.after(self.intervalTime, func=lambda: self.showBestResultAnimation(bestRemoveLineOrder))

    def showBestResultAnimation(self, bestRemoveLineOrder):
        if len(bestRemoveLineOrder) == 0:
            again = askyesno("Animation", "Animation finish,show again?")
            if again:
                self.showBestResultClick()
            else:
                return
        else:
            i = bestRemoveLineOrder.pop(0)
            self.removeLineIFromCanvas(i)
            self.canvas.after(self.intervalTime, func=lambda: self.showBestResultAnimation(bestRemoveLineOrder))

    def getData(self):
        linesLen = len(self.lines)
        if linesLen==0:
            showerror("error", "Input N First!")
            return
        getDataFrame = Toplevel()
        
        Label(getDataFrame, text="ID", width=5).grid(row=0,column=0)
        Label(getDataFrame, text="NUM", width=5).grid(row=0,column=1)
        Label(getDataFrame, text="+", width=5).grid(row=0,column=2)
        Label(getDataFrame, text="*", width=5).grid(row=0,column=3)
        global numsEntry,v
        numsEntry = []
        v = []
        for i in range(len(self.lines)):
            v.append(IntVar())
        for i in range(linesLen):
            Label(getDataFrame,text=str(i)).grid(row=i+1,column=0)
            num = Entry(getDataFrame,width=5)
            num.grid(row=i+1,column=1)
            Radiobutton(getDataFrame ,  variable=v[i],
                                        value=0,
                                        cursor="hand1",
                                        activebackground="gray",
                                        activeforeground="gray").grid(row=i+1,column=2)
            Radiobutton(getDataFrame ,  variable=v[i],
                                        value=1,
                                        cursor="hand1",
                                        activebackground="gray",
                                        activeforeground="gray").grid(row=i+1,column=3)
            numsEntry.append(num)
        confirm = Button(getDataFrame , text="confirm",
                                        command=lambda:self.inputDataConfirm(getDataFrame))
        confirm.grid(row=linesLen+1,column=1,columnspan=2)
        getDataFrame.focus_set()
        getDataFrame.grab_set()
        getDataFrame.wait_window()
    def inputDataConfirm(self,getDataFrame):
        global numsEntry,v
        nums = []
        error = False
        for entry in numsEntry:
            num = entry.get()
            try:
                num = int(num)
                nums.append(num)
            except:
                error = True
                showerror("error", "Null or Data is not Number！！！")
            if error:
                return   
        for i in range(len(nums)):
            self.lines[i].getNode1().setNum(nums[i])
            if v[i].get()==0:
                self.lines[i].setOpr("+")
            else:
                self.lines[i].setOpr("*")
        #更新原始输入数据
        self.originLines = copy.deepcopy(self.lines)
        self.drawLines()
        getDataFrame.destroy()
    def createDrawbar(self):
        drawbarWindow = PanedWindow(self.master,relief=RIDGE,
                                                width=self.drawbarWidth,
                                                height=self.drawbarHeight)
        drawbarWindow.grid(row=0, column=1, rowspan=2)
        
        self.canvas = Canvas(drawbarWindow ,width=self.drawbarWidth,
                                            height=self.drawbarHeight)
        myFont = tkFont.Font(size=36, weight="bold")
        self.canvas.create_text(self.drawbarWidth/2, self.drawbarHeight/3,
                                text="Polygon Game", font=myFont)
        self.canvas.create_text(self.drawbarWidth / 2, self.drawbarHeight / 2,
                                text="©2016 Challe, Float, Ivan, Michael. All Rights Reserved")
        drawbarWindow.add(self.canvas)

if __name__=='__main__':
    MainFrame().mainloop()