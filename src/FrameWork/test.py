from Tkinter import *
from ImageTk import *
import cv2
import PIL.Image
import PIL.ImageTk
class MainFrame(Frame):
    def __init__(self, master=None, cnf={}, **kw):
        Frame.__init__(self, master, cnf, **kw)
        self.createBar()

    def createBar(self):
        panedWindow = PanedWindow(self.master)
        panedWindow.pack()

        self.label = Label(panedWindow,text="hello")
        self.label.after(1000,func=self.click)
        panedWindow.add(self.label)
        # label.configure(image=tkImage)
    def click(self):
        self.label.update()
        filename = 'D:\Python27\workspace\PolygonGame\src\images\pic.JPG'
        img = cv2.imread(filename=filename)
        print img
        # img = PhotoImage(file=filename)
        pilImage = PIL.Image.fromarray(img)
        print pilImage
        tkImage = PIL.ImageTk.PhotoImage(image=pilImage)
        print tkImage
        self.label.configure(image=tkImage)



def main():
    filename = 'D:\Python27\workspace\PolygonGame\src\images\pic.JPG'
    root = Tk()
    panedWindow = PanedWindow(root)
    img = PhotoImage(file=filename)
    label = Label(panedWindow, image=img)
    panedWindow.grid(column=0, row=0)
    panedWindow.add(label)
    root.mainloop()

root = Tk()
frame = MainFrame(root)
root.mainloop()