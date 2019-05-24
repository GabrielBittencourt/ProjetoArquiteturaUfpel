from tkinter import *

def altatensao():
	exec(open("./alta.py").read())

def baixatensao():
	exec(open("./baixa.py").read())


class Application:
    def __init__(self, master=None):
        self.widget1 = Frame(master)
        self.widget1.pack()
        self.widget2 = Frame(master)
        self.widget2.pack()
        self.widget3 = Frame(master)
        self.widget3.pack()
        self.widget4 = Frame(master)
        self.widget4.pack()

        self.msg = Label(self.widget1, text="Leitor de contas")
        self.msg["font"] = ("Verdana", "10", "italic", "bold")
        self.msg.pack ()

        self.baixa = Button(self.widget2)
        self.baixa["text"] = "Baixa Tensão"
        self.baixa["font"] = ("Calibri", "20")
        self.baixa["width"] = 20
        self.baixa["command"] = lambda: baixatensao()
        self.baixa.pack (side=RIGHT)
        
        self.alta = Button(self.widget3)
        self.alta["text"] = "Alta Tensão"
        self.alta["font"] = ("Calibri", "20")
        self.alta["width"] = 20
        self.alta["command"] = lambda: altatensao()
        self.alta.pack (side=TOP)
        

        self.sair = Button(self.widget4)
        self.sair["text"] = "Sair"
        self.sair["font"] = ("Calibri", "20")
        self.sair["width"] = 20
        self.sair["command"] = self.widget4.quit
        self.sair.pack (side=BOTTOM)
  
root = Tk()
Application(root)
root.mainloop()
