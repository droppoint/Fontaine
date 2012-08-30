# -*- coding: UTF-8 -*-
'''
Created on 29.08.2012

@author: APartilov
'''
from Tkinter import *
import ttk
import tkFileDialog


class ValidatingEntry(Entry):
    # base class for validating entry widgets

    def __init__(self, master, value="", **kw):
        apply(Entry.__init__, (self, master), kw)
        self.__value = value
        self.__variable = StringVar()
        self.__variable.set(value)
        self.__variable.trace("w", self.__callback)
        self.config(textvariable=self.__variable)

    def __callback(self, *dummy):
        value = self.__variable.get()
        newvalue = self.validate(value)
        if newvalue is None:
            self.__variable.set(self.__value)
        elif newvalue != value:
            self.__value = newvalue
            self.__variable.set(self.newvalue)
        else:
            self.__value = value

    def validate(self, value):
        # override: return value, new value, or None if invalid
        return value


class FloatEntry(ValidatingEntry):

    def validate(self, value):
        try:
            if value:
                v = float(value)
            return value
        except ValueError:
            return None


class ConfigurationWindow(Toplevel):
#    self = Toplevel()
    def __init__(self, root, title=None):
        Toplevel.__init__(self, root)
        self.transient(root)

        if title:
            self.title(title)
        self.root = root
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("180x150")
        self.resizable(False, False)

        #Frame с плотностями
        self.frame = LabelFrame(self, text="Плотность")
        self.frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.6)
        oil_label = ttk.Label(self.frame, text="Нефть")
        water_label = ttk.Label(self.frame, text="Вода")
        oil_spin = FloatEntry(self.frame, width=10)
        oil_spin.insert(0, "800.0")
        water_spin = FloatEntry(self.frame, width=10)
        water_spin.insert(0, "1000.0")
        oil_spin.place(relx=0.5, rely=0.15)
        water_spin.place(relx=0.5, rely=0.65)
        oil_label.place(relx=0.1, rely=0.15)
        water_label.place(relx=0.1, rely=0.65)

        # Кнопки внизу
        ok_button = ttk.Button(self, text="OK")
        cancel_button = ttk.Button(self, text="Отмена")
        ok_button.place(relx=0.05, rely=0.75)
        cancel_button.place(relx=0.5, rely=0.75)
        self.wait_window(self)

    def cancel(self):
        self.root.focus_set()
        self.destroy()


class AboutWindow(Toplevel):

    def __init__(self, root, title=None):
        Toplevel.__init__(self, root)
        self.transient(root)

        if title:
            self.title(title)
        self.root = root
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("320x270")
        self.resizable(False, False)

        frame = Frame(self)
        frame.pack()
        canvas = Canvas(frame, bg="black", width=150, height=150)
        canvas.pack()
        program_label = Label(self, text="Fontaine v0.76", font="Arial 14")
        powered_label = Label(self, text="Powered by Python & TkInter",
                              font="Arial 9")
        author_label = Label(self, text="Автор: Алексей Партилов     @2012",
                             font="Arial 9")
        program_label.pack()
        powered_label.pack()
        author_label.pack()

        ok_button = ttk.Button(self, text="OK",
                               width=10, command=self.cancel)
        ok_button.pack()

#        image = PhotoImage(file="fontaine.png")
#        canvas.create_image(200, 200, image=image)

    def cancel(self):
        self.root.focus_set()
        self.destroy()

if __name__ == '__main__':

    def LoadFile():
        fn = tkFileDialog.Open(root,
                               filetypes=[('*.RSM files', '.rsm')]
                               ).show()
        if fn == '':
            return
        return fn

    def SaveFile():
        fn = tkFileDialog.SaveAs(root,
                                 filetypes=[('Microsoft Excel', '.xls')]
                                 ).show()
        if fn == '':
            return
        if not fn.endswith(".xls"):
            fn += ".xls"
        return fn

    def hello():
        print "say hello"

    # Описание и настройки главного окна
    root = Tk()
#    root.iconbitmap(default='@fontaine_icon.ico')
    root.geometry('320x175')
    root.resizable(False, False)
    root.title("Fontaine")
    menu = Menu(root)
    root.config(menu=menu)
#    config = ConfigurationWindow(root, title="Настройки")
    about = AboutWindow(root, title="О программе")

    # Верхнее меню
    filemenu = Menu(menu, tearoff=0)
    helpmenu = Menu(menu, tearoff=0)
    menu.add_cascade(label="Файл", menu=filemenu)
    filemenu.add_command(label="Открыть файл ограничений")
    filemenu.add_command(label="Настройки", command=hello)
    filemenu.add_separator()
    filemenu.add_command(label="Выход", command=hello)
    filemenu.entryconfig(0, state=DISABLED)
    menu.add_cascade(label="Справка", menu=helpmenu)
    helpmenu.add_command(label="О программе", command=hello)

    # Содержимое главного окна
    lab = ttk.Label(root, text="Выберите файл *.rsm")
    but = ttk.Button(root,
                 text="...", width=2,
                 command=LoadFile)
    but2 = ttk.Button(root,
                text="Преобразовать", width=18,
                command=SaveFile)
    ent = ttk.Entry(width=40)
    prog = ttk.Progressbar()
    prog['value'] = 50
    lab.place(relx=0.07, rely=0.20)
    ent.place(relx=0.07, rely=0.30)
#    prog.pack()
    but.place(relx=0.87, rely=0.30)
    but2.place(anchor="center", relx=0.5, rely=0.7)

    root.mainloop()
