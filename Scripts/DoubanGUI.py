import os
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox

from Scripts.DoubanSpider import DoubanSpider


class DoubanGUI:

    def __init__(self):
        self.window = Tk()
        self.window.title("DoubanCrawler")
        self.window.tk.call('wm', 'iconphoto', self.window._w, PhotoImage(file='Images/app.gif'))
        self.window.geometry('400x400')
        self.window.resizable(FALSE, FALSE)

        logo_image = PhotoImage(file='Images/logo.gif')
        self.logo = Label(self.window, image=logo_image)
        self.logo.place(x=150, y=30, width=100, height=100)

        self.user_label = Label(self.window, text="Phone / Email:")
        self.user_label.place(x=60, y=150, width=100, height=20)
        self.user_name = Entry(self.window, width=160)
        self.user_name.place(x=170, y=150, width=160, height=20)

        self.pwd_label = Label(self.window, text="Password:")
        self.pwd_label.place(x=73, y=180, width=100, height=20)
        self.password = Entry(self.window, width=160, show="*")
        self.password.place(x=170, y=180, width=160, height=20)
        file = "account/userInfo"
        if not os.path.exists(file):
            os.mknod(file)

        with open(file, 'r+') as f:
            account = f.read().strip().split(' ')
            if len(account) == 2:
                username, pwd = account
                self.user_name.insert(0, username)
                self.password.insert(0, pwd)

        self.keyword_label = Label(self.window, text="请选择关键词：", font=("Arial Bold", 14), fg="red")
        self.keyword_label.place(x=100, y=210, width=200, height=20)

        self.keywords = Entry(self.window, width=160, justify=CENTER)
        self.keywords.place(x=120, y=240, width=160, height=20)
        self.submit_btn = Button(self.window, text="开始搜索", font=("Arial Bold", 16), command=self.on_click)
        self.submit_btn.place(x=150, y=280, width=100, height=30)
        self.window.mainloop()

    def on_click(self):
        if self.keywords.get() == '':
            messagebox.showwarning('输入错误', '关键词不可为空！')
        elif self.user_name.get() == '' or self.password.get() == '':
            messagebox.showwarning('账号错误', '账号名或密码不可为空！')
        else:
            keywords = self.keywords.get()
            username = self.user_name.get()
            password = self.password.get()
            self.deinit_canvas()
            DoubanSpider(username, password, keywords, self.window)

    def deinit_canvas(self):
        self.logo.destroy()
        self.user_label.destroy()
        self.user_name.destroy()
        self.pwd_label.destroy()
        self.password.destroy()
        self.keyword_label.destroy()
        self.keywords.destroy()
        self.submit_btn.destroy()


DoubanGUI()
