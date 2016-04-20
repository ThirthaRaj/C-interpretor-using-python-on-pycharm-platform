from try1 import *
import  tkinter
from tkinter.filedialog import askopenfilename ,asksaveasfilename

#this is the code for the gui
class window_file(tkinter.Tk):
    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
        #self.parent=parent
        self.initialize()

#initialisation
    def initialize(self):
        #code for the frame
        self.geometry("650x600+0+0")
        self.title("FILE")
        self.T=tkinter.Text(self,height=650,width=600)

        #code for adding and configuring scroll bar
        S=tkinter.Scrollbar(self)
        S.pack(side=tkinter.RIGHT,fill=tkinter.Y)
        S.config(command=self.T.yview)
        self.T.config(yscrollcommand=S.set)
        self.bind("<Control-Key>",self.key)

        self.T.pack()
        self.menu()

    def menu(self):
        #code for adding the menu's
        menubar=tkinter.Menu(self)
        file=tkinter.Menu(self)
        menubar.add_cascade(label="File",menu=file)
        file.add_command(label="New File  CTRL+n",command=self.new)
        file.add_command(label="Save       CTRL+s",command=self.save)
        file.add_command(label="Open      CTRL+o",command=self.open1)
        #file.add_command(label="Open Module",command=self.module)
        file.add_command(label="Run        CTRL+r",command=self.run)
        file.add_command(label="Close ",command=self.close)
        file.add_command(label="Exit       CTRL+q",command=self.exit)

        self.config(menu=menubar)

    def new(self):           #code for new file to create a new file
        win1=window_file(None)
        #win1.mainloop()



    def open1(self):          #code to open a file in system
        win2=window_file(None)
        win2.open2()

    def open2(self):
        filename=askopenfilename()
        if (filename == ""):
            self.destroy()
        else:
            myfile=open(filename,"r")
            txt=myfile.read()
            self.T.insert('1.0',txt)
            self.lift()
            myfile.close()


    def save(self):                 #code to save a file onto the system
        try:
            savefile=asksaveasfilename()
            myfile=open(savefile,'w')
            txt=self.T.get("1.0",tkinter.END)
            myfile.write(txt)
            myfile.close()
            #self.title(myfile)
        except FileNotFoundError:
            pass



    def close(self):            #code for close and exit
        self.destroy()

    def exit(self):
        exit()

    def run(self):                  #code to run the code present in the window
        txt=self.T.get("1.0",tkinter.END)
        fun1(txt)



    def key(self,event):

            if event.keysym=='n':
                self.new()
            else:
                if event.keysym=='s':
                    self.save()
                else:
                    if event.keysym=='q':
                        self.exit()
                    else:
                        if event.keysym=='o':
                            self.open1()
                        else:
                            if event.keysym=="r":
                                self.run()






#main  function
if __name__ == "__main__":
    win=window_file(None)
    win.mainloop()







