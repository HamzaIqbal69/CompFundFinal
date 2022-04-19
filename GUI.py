from tkinter import *
class Gui:
    def __init__(self):
        self.window = Tk()
        self.message_box = Entry(self.window, width=100, bg='white', fg='black')
        self.user_entry = Entry(self.window, width=20, bg='white', fg='black')
        self.output = Text(self.window, width=100, height=30, wrap=WORD, background='white')
        self.window.title('Hamza''s messaging')
        self.window.configure(background='black')
        Label(self.window, text='Enter Username: ', bg='black', fg='white', font='none 16 bold').grid(row=0, column=0, sticky=W)
        self.user_entry.grid(row=0, column=1, sticky=W)
        Button(self.window, text='Enter', width=5, command=self.get_user).grid(row=0, column=2, sticky=W)
        Label(self.window, text='MESSAGES', bg='black', fg='white', font='none 16 bold').grid(row=1, column=0, sticky=W)
        Label(self.window, text='ENTER MESSAGE:', bg = 'black', fg='white', font='none 16 bold').grid(row=2, column=0, sticky=W)
        self.message_box.grid(row=2, column=1, sticky=W)
        Button(self.window, text='Send', width=4, command=self.get_message).grid(row=2, column=2, sticky=W)
        self.output.grid(row=1, column=1, sticky=W)
        self.window.mainloop()

    def get_user(self):
        username = self.user_entry.get()
        return username

    def get_message(self):
        message = self.message_box.get()
        x = message
        self.output.insert(END, x)
        return message

