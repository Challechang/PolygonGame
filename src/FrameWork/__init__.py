# encoding:utf-8
from Tkinter import *
from FunctionCallback import *
from tkMessageBox import showerror
from tkMessageBox import  askyesno
import copy
import polygon_game as plg
import tkFont
import random


class MainFrame(Frame):

    initbarHeight   = 100
    initbarWidth    = 200
    resultbarHeight = 370
    resultbarWidth  = 197
    drawbarHeight   = 500
    drawbarWidth    = 500
    ovalRadius      = 27
    widgetWidth     = 20
    n               = -1
    lines           = []
    originLines     = []
    stackPreLines   = []
    stackNextLines  = []
    ERROR           = -1
    test            = 0
    intervalTime    = 1000
    isPlaying       = False
    firstEdge       = True
    initLine        = False
    isPauseClick    = False
    background      = "white"
    widgetColor     = "white"
    playX           = 100
    playY           = 210
    playRadius      = 60

    def __init__(self,parent=None):
        Frame.__init__(self, parent)
#         self.pack(expand=YES,fill=BOTH)
        self.myFont = tkFont.Font(size=13)
        self.createWidgets()
        self.master.title("game")
    
    def createWidgets(self):
        self.createMenubar()
        self.createInitbar()
        self.createResultbar()
        self.createDrawbar()

    def createMenubar(self):
        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)
        self.fileMenu()
        self.editMenu()

    def fileMenu(self):
        file = Menu(self.menubar, bg=self.widgetColor)
        file.add_command(label='Home', command=self.returnHome, underline=0)
        file.add_command(label='Open...', command=self.notdone, underline=0)
        file.add_command(label='Quit', command=self.master.destroy, underline=0)
        self.menubar.add_cascade(label='File', menu=file, underline=0)

    def editMenu(self):
        edit = Menu(self.menubar, bg=self.widgetColor)
        edit.add_command(label='Cut', command=self.notdone, underline=0)
        edit.add_command(label='Paste', command=self.notdone, underline=0)
        self.menubar.add_cascade(label='Edit', menu=edit, underline=0)

    #     打开文件菜单回调函数
    def returnHome(self):
        self.createWidgets()

    def capVideo(self):
        showerror('error', "not done yet!!!")

    def notdone(self):
        showerror('error', "not done yet!!!")

    #接收用户输入的数据n
    def createInitbar(self):
        initbarWindow = PanedWindow(self.master, relief=RIDGE,
                                    orient=VERTICAL, width=self.initbarWidth,
                                    height=self.initbarHeight, bg=self.background)
        initbarWindow.grid(row=0, column=0)

        Label(initbarWindow, text="Input N", anchor=CENTER,
              bg=self.widgetColor).grid(row=0, column=0, columnspan=2)
        getNEntry = Entry(initbarWindow, bd="5", width=26)
        getNEntry.grid(row=1, column=0, columnspan=2)
        confirm = Button(initbarWindow, command=lambda: self.confirmGetN(getNEntry),
                         text="Confirm", width=self.widgetWidth, bg=self.widgetColor)
        confirm.grid(row=2, column=0, pady=5)
        inputData = Button(initbarWindow, text="Input Data", command=self.getData,
                           width=self.widgetWidth, bg=self.widgetColor)
        inputData.grid(row=3, column=0, padx=10, pady=3)
    
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
            self.initLine       = True
            self.drawLines()
    def drawOprNextOrBack(self):
        self.canvas.create_rectangle(self.drawbarWidth * 1.0 / 3, self.drawbarHeight * 7.0 / 8,
                                     self.drawbarWidth * 1.0 / 3 + 60, self.drawbarHeight * 7.0 / 8 + 30,
                                     fill="black")
        preId = self.canvas.create_text(self.drawbarWidth * 1.0 / 3 + 30, self.drawbarHeight * 7.0 / 8 + 15,
                                        text="Previous",
                                        fill="yellow",
                                        activefill="blue")

        self.canvas.create_rectangle(self.drawbarWidth * 2.0 / 3, self.drawbarHeight * 7.0 / 8,
                                     self.drawbarWidth * 2.0 / 3 + 60, self.drawbarHeight * 7.0 / 8 + 30,
                                     fill="black")
        nextId = self.canvas.create_text(self.drawbarWidth * 2.0 / 3 + 30, self.drawbarHeight * 7.0 / 8 + 15,
                                         text="Next",
                                         fill="yellow",
                                         activefill="blue")

        self.canvas.tag_bind(preId, sequence="<Button-1>", func=self.preOprClick)
        self.canvas.tag_bind(nextId, sequence="<Button-1>", func=self.nextOprClick)

    def preOprClick(self, event):
        lenStackLines = len(self.stackPreLines)
        if lenStackLines == 0:
            showerror("error", "No previous!!!")
            return
        elif lenStackLines == 1:
            self.firstEdge = True

        self.stackNextLines.append(copy.deepcopy(self.lines))
        self.lines = self.stackPreLines.pop()
        self.drawLines()

    def nextOprClick(self, event):
        lenStackLines = len(self.stackNextLines)
        if lenStackLines == 0:
            showerror("error", "No next!!!")
            return
        self.stackPreLines.append(copy.deepcopy(self.lines))
        self.lines = self.stackNextLines.pop()
        self.drawLines()

    def drawLines(self):
        self.canvas.delete("all")
        if (not self.isPlaying) and (not self.initLine):
            self.drawOprNextOrBack()
        self.initLine = False
        for i in range(len(self.lines)):
            line = self.lines[i]
            (startX, startY, endX, endY) = (line.getStartX(), line.getStartY(),
                                            line.getEndX(), line.getEndY())
            idInCanvas = self.canvas.create_line((startX, startY, endX, endY), arrow=tk.BOTH,
                                                 width=5, smooth=True, activefill="blue")
            line.setIdInCanvas(idInCanvas)
            x1,x2,y1,y2 = calXY(startX, startY, endX, endY)
            oprId = self.canvas.create_text(x1, y1,
                                            text=line.getOpr(),
                                            fill="blue",
                                            activefill="yellow",
                                            font=self.myFont)
            line.setIdOprInCanvas(oprId)
            idId = self.canvas.create_text(x2, y2,
                                           text=line.getId(),
                                           fill="blue",
                                           activefill="yellow",
                                           font=self.myFont)
            line.setIdIdInCanvas(idId)
            ovalId = self.canvas.create_oval(startX-self.ovalRadius, startY-self.ovalRadius,
                                             startX+self.ovalRadius, startY+self.ovalRadius,
                                             fill="black")
            numId = self.canvas.create_text(startX, startY,
                                            text=line.getNode1().getNum(),
                                            fill="yellow",
                                            font=self.myFont)
            line.getNode1().setIdInCanvas([ovalId, numId])
            if i == len(self.lines)-1:
                ovalId = self.canvas.create_oval(endX - self.ovalRadius, endY - self.ovalRadius,
                                                 endX + self.ovalRadius, endY + self.ovalRadius,
                                                 fill="black")
                numId = self.canvas.create_text(endX, endY,
                                                text=line.getNode2().getNum(),
                                                fill="yellow",
                                                font=self.myFont)
                line.getNode2().setIdInCanvas([ovalId, numId])
            def handler(event, i = line.getId()):
                return self.lineClick(event, i)
            self.canvas.tag_bind(idInCanvas, sequence="<Button-1>", func=handler)

    def lineClick(self, event, i):
        self.stackPreLines.append(copy.deepcopy(self.lines))         #将当前所有信息压入栈列表中
        self.stackNextLines = []
        self.removeLineIFromCanvas(i)

    def removeLineIFromCanvas(self, i):
        index, line = self.delLine(self.lines, i)  # 将第i条线从列表中删除
        if self.firstEdge:
            self.firstEdge = False
            self.delLineInCanvas(line)
            if not self.isPlaying:
                self.drawOprNextOrBack()
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
                                        fill="yellow",
                                        font=self.myFont)
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
    def resortLines(self, lines, index):
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

    def delNodeInCanvas(self, node):
        idInCanvas = node.getIdInCanvas()
        self.canvas.delete(idInCanvas[0])
        self.canvas.delete(idInCanvas[1])

    def createResultbar(self):
        resultbarWindow = PanedWindow(self.master, relief=RIDGE,
                                      width=self.resultbarWidth, height=self.resultbarHeight,
                                      bg=self.background, orient=VERTICAL)
        resultbarWindow.grid(row=1, column=0)
        # showBestResult = Button(resultbarWindow, width=self.widgetWidth,
        #                         text="Best Result", command=self.showBestResultClick,
        #                         bg=self.widgetColor)
        self.resultCanvas = Canvas(resultbarWindow, bg=self.widgetColor)
        myFont = tkFont.Font(size=11)
        self.resultCanvas.create_text(self.resultbarWidth / 2, 25,
                                      text="\n\n\n\n\n\n  Click the play button\n"
                                           " to show the best result \n"
                                           "   of Polygon Game \n"
                                           "  when the edge is N!!!",
                                      font=myFont)
        self.playX = self.resultbarWidth / 2
        self.playY = 210
        self.resultCanvas.create_oval(self.playX - self.playRadius, self.playY - self.playRadius,
                                      self.playX + self.playRadius, self.playY + self.playRadius,
                                      fill="black")
        self.resultCanvas.create_oval(self.playX - self.playRadius + 5, self.playY - self.playRadius + 5,
                                      self.playX + self.playRadius - 5, self.playY + self.playRadius - 5,
                                      fill=self.widgetColor)
        self.playId = self.resultCanvas.create_polygon(self.playX - self.playRadius / 2.0 + 8, self.playY - self.playRadius / 2.0,
                                                       self.playX - self.playRadius / 2.0 + 8, self.playY + self.playRadius / 2.0,
                                                       self.playX + self.playRadius / 2.0 + 2, self.playY,
                                                       fill="black", activefill="blue")
        self.resultCanvas.tag_bind(self.playId, sequence="<Button-1>", func=self.play)
        resultbarWindow.add(self.resultCanvas)

    def play(self, event):
        if self.isPauseClick:
            self.canvas.after(0, func=self.showBestResultAnimation)
        else:
            if self.showBestResultClick() == self.ERROR:
                return
        self.resultCanvas.delete(self.playId)
        self.pauseId = self.resultCanvas.create_rectangle(self.playX - self.playRadius / 2.0 + 8, self.playY - self.playRadius / 2.0,
                                                          self.playX + self.playRadius / 2.0 - 8, self.playY + self.playRadius / 2.0,
                                                          fill="black", activefill="blue")
        self.resultCanvas.create_rectangle(self.playX - self.playRadius / 2.0 + 22, self.playY - self.playRadius / 2.0,
                                           self.playX + self.playRadius / 2.0 - 22, self.playY + self.playRadius / 2.0,
                                           fill="white", outline="white")
        self.resultCanvas.tag_bind(self.pauseId, sequence="<Button-1>", func=self.pause)
        self.isPauseClick = False
        self.isPlaying = True

    def pause(self, event):
        self.resultCanvas.delete(self.pauseId)
        self.playId = self.resultCanvas.create_polygon(self.playX - self.playRadius / 2.0 + 8,
                                                       self.playY - self.playRadius / 2.0,
                                                       self.playX - self.playRadius / 2.0 + 8,
                                                       self.playY + self.playRadius / 2.0,
                                                       self.playX + self.playRadius / 2.0 + 2, self.playY,
                                                       fill="black", activefill="blue")
        self.isPlaying = False
        self.isPauseClick = True
        self.canvas.after_cancel(self.curAnimationRunId)
        self.resultCanvas.tag_bind(self.playId, sequence="<Button-1>", func=self.play)


    def showBestResultClick(self):
        if (isNum(self.n) == -1):
            self.n = -1
            showerror("error", "Data is not a Number!!!")
            return self.ERROR
        if (isNum(self.n) < 1):
            self.n = -1
            showerror("error", "Number less than 1!!!")
            return self.ERROR
        self.bestRemoveLineOrder = plg.dealBestPath(self.originLines)
        self.lines = copy.deepcopy(self.originLines)
        self.isPlaying = True
        self.initLine = True
        self.drawLines()
        self.firstEdge = True
        self.canvas.after(self.intervalTime, func=lambda: self.showBestResultAnimation())

    def showBestResultAnimation(self):
        if len(self.bestRemoveLineOrder) == 0:
            self.playId = self.resultCanvas.create_polygon(self.playX - self.playRadius / 2.0 + 8,
                                                           self.playY - self.playRadius / 2.0,
                                                           self.playX - self.playRadius / 2.0 + 8,
                                                           self.playY + self.playRadius / 2.0,
                                                           self.playX + self.playRadius / 2.0 + 2, self.playY,
                                                           fill="black", activefill="blue")
            self.resultCanvas.delete(self.pauseId)
            self.resultCanvas.tag_bind(self.playId, sequence="<Button-1>", func=self.play)
            again = askyesno("Animation", "Animation finish,show again?")
            if again:
                self.showBestResultClick()
            else:
                self.isPlaying = False
                return
        else:
            self.isPlaying = True
            i = self.bestRemoveLineOrder.pop(0)
            self.removeLineIFromCanvas(i)
            self.curAnimationRunId = self.canvas.after(self.intervalTime, func=lambda: self.showBestResultAnimation())

    def getData(self):
        linesLen = len(self.lines)
        if linesLen==0:
            showerror("error", "Input N First!")
            return
        getDataFrame = Toplevel()
        
        Label(getDataFrame, text="ID", width=5).grid(row=0, column=0)
        Label(getDataFrame, text="NUM", width=5).grid(row=0, column=1)
        Label(getDataFrame, text="+", width=5).grid(row=0, column=2)
        Label(getDataFrame, text="*", width=5).grid(row=0, column=3)
        global numsEntry, v
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
            Radiobutton(getDataFrame, variable=v[i],
                        value=1, cursor="hand1", activebackground="gray",
                        activeforeground="gray").grid(row=i+1,column=3)
            numsEntry.append(num)
        confirm = Button(getDataFrame, text="confirm",
                         command=lambda: self.inputDataConfirm(getDataFrame))
        random = Button(getDataFrame, text="random",
                         command=lambda: self.generateRandomData(getDataFrame))
        confirm.grid(row=linesLen+1, column=1, padx=5)
        random.grid(row=linesLen+1, column=2)
        getDataFrame.focus_set()
        getDataFrame.grab_set()
        getDataFrame.wait_window()

    def generateRandomData(self, getDataFrame):
        for i in range(len(self.lines)):
            self.lines[i].getNode1().setNum(random.randint(0, 100))
            if random.randint(0, 1) == 0:
                self.lines[i].setOpr("+")
            else:
                self.lines[i].setOpr("*")
        # 更新原始输入数据
        self.originLines = copy.deepcopy(self.lines)
        self.drawLines()
        getDataFrame.destroy()

    def inputDataConfirm(self, getDataFrame):
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
        drawbarWindow = PanedWindow(self.master, relief=RIDGE,
                                    width=self.drawbarWidth, height=self.drawbarHeight,
                                    bg=self.background)
        drawbarWindow.grid(row=0, column=1, rowspan=2)
        
        self.canvas = Canvas(drawbarWindow, width=self.drawbarWidth,
                             height=self.drawbarHeight, bg=self.background)
        myFont = tkFont.Font(size=36, weight="bold")
        self.canvas.create_text(self.drawbarWidth/2, self.drawbarHeight/3,
                                text="Polygon Game", font=myFont)
        self.canvas.create_text(self.drawbarWidth / 2, self.drawbarHeight / 2,
                                text="©2016 Challe, Float, Ivan, Michael. All Rights Reserved")
        drawbarWindow.add(self.canvas)

if __name__=='__main__':
    MainFrame().mainloop()